#!/usr/bin/env python
"""
Fix ZoneHVAC:EquipmentList Objects with Misaligned Fields

This script repairs IDF files where ZoneHVAC:EquipmentList objects have:
- Equipment names in numeric sequence fields
- Missing or blank required fields
- Shifted field positions

Common symptom:
    ** Severe ** <root>[ZoneHVAC:EquipmentList][...][zone_equipment_cooling_sequence]
                 - Value type "string" for input "..." not permitted by 'type' constraint.

Usage:
    python fix-equipment-lists.py input.idf output.idf [--idd-path PATH]

Arguments:
    input.idf    Path to corrupted IDF file
    output.idf   Path for fixed IDF file
    --idd-path   Path to Energy+.idd (optional, auto-detected)

Example:
    python fix-equipment-lists.py in_cleaned.idf in_fixed.idf

Author: EnergyPlus Assistant Skill
Date: 2025-11-24
"""

import sys
import os
import argparse
from pathlib import Path

# Check if eppy is installed
try:
    from eppy.modeleditor import IDF
    from eppy import modeleditor
except ImportError:
    print("ERROR: eppy library not found")
    print("Install with: pip install eppy")
    sys.exit(1)


def find_energyplus_idd():
    """Auto-detect EnergyPlus IDD file location"""

    # Common EnergyPlus installation locations (Windows)
    possible_paths = [
        "C:/EnergyPlusV25-1-0/Energy+.idd",
        "C:/EnergyPlusV24-2-0/Energy+.idd",
        "C:/EnergyPlusV23-2-0/Energy+.idd",
        "C:/EnergyPlus/Energy+.idd",
    ]

    for path in possible_paths:
        if os.path.exists(path):
            return path

    # Check environment variable
    eplus_dir = os.environ.get('ENERGYPLUS_DIR')
    if eplus_dir:
        idd_path = os.path.join(eplus_dir, 'Energy+.idd')
        if os.path.exists(idd_path):
            return idd_path

    return None


def analyze_equipment_list(eq_list):
    """
    Analyze a ZoneHVAC:EquipmentList object to detect corruption

    Returns:
        dict: Analysis results with corruption indicators
    """

    name = eq_list.Name
    scheme = eq_list.Load_Distribution_Scheme

    # Get all field names from the eppy object
    # eq_list.fieldnames contains all field names for this object type
    fieldnames = eq_list.fieldnames

    # Equipment lists have repeating groups of fields:
    # - Zone_Equipment_N_Object_Type
    # - Zone_Equipment_N_Name
    # - Zone_Equipment_N_Cooling_Sequence
    # - Zone_Equipment_N_Heating_or_NoLoad_Sequence
    # - Zone_Equipment_N_Sequential_Cooling_Fraction_Schedule_Name
    # - Zone_Equipment_N_Sequential_Heating_Fraction_Schedule_Name

    equipment = []
    issues = []

    # Parse equipment entries
    idx = 1
    while True:
        # Field name patterns
        obj_type_field = f"Zone_Equipment_{idx}_Object_Type"
        name_field = f"Zone_Equipment_{idx}_Name"
        cooling_seq_field = f"Zone_Equipment_{idx}_Cooling_Sequence"
        heating_seq_field = f"Zone_Equipment_{idx}_Heating_or_NoLoad_Sequence"

        # Check if these fields exist
        if obj_type_field not in fieldnames:
            break

        # Get field values using eppy's getattr
        obj_type = getattr(eq_list, obj_type_field, "")
        eq_name = getattr(eq_list, name_field, "")
        cooling_seq = getattr(eq_list, cooling_seq_field, "")
        heating_seq = getattr(eq_list, heating_seq_field, "")

        # Convert to strings and handle None
        obj_type = str(obj_type) if obj_type else ""
        eq_name = str(eq_name) if eq_name else ""
        cooling_seq = str(cooling_seq) if cooling_seq else ""
        heating_seq = str(heating_seq) if heating_seq else ""

        # Detect corruption patterns

        # Pattern 1: Object type is blank but name is present (shifted fields)
        if obj_type == "" and eq_name != "":
            issues.append(f"Equipment {idx}: Object type blank, name present (field shift detected)")

        # Pattern 2: Cooling sequence contains a name instead of number
        if cooling_seq != "" and not cooling_seq.replace('.', '').replace('-', '').isdigit():
            issues.append(f"Equipment {idx}: Cooling sequence contains non-numeric value: '{cooling_seq}'")

        # Pattern 3: Heating sequence contains a name instead of number
        if heating_seq != "" and not heating_seq.replace('.', '').replace('-', '').isdigit():
            issues.append(f"Equipment {idx}: Heating sequence contains non-numeric value: '{heating_seq}'")

        # Store equipment data
        if obj_type != "" or eq_name != "":
            equipment.append({
                'index': idx,
                'object_type': obj_type,
                'name': eq_name,
                'cooling_seq': cooling_seq,
                'heating_seq': heating_seq
            })

        idx += 1

    return {
        'name': name,
        'scheme': scheme,
        'equipment': equipment,
        'issues': issues,
        'is_corrupted': len(issues) > 0
    }


def reconstruct_equipment_list(idf, analysis):
    """
    Reconstruct a ZoneHVAC:EquipmentList object with correct field order

    Args:
        idf: IDF object
        analysis: Analysis dict from analyze_equipment_list()

    Returns:
        New equipment list object with correct structure
    """

    # Parse corrupted data to extract actual equipment
    # Common corruption pattern:
    # Equipment 1: Type=blank, Name=Type, CoolingSeq=Name, HeatingSeq=Number
    # Equipment 2: Type=Type, Name=Name, CoolingSeq=Number, HeatingSeq=Number

    corrected_equipment = []

    for eq in analysis['equipment']:
        idx = eq['index']
        obj_type = eq['object_type']
        name = eq['name']
        cooling_seq = eq['cooling_seq']
        heating_seq = eq['heating_seq']

        # Detect and fix shifted fields
        if obj_type == "" and name != "":
            # Fields are shifted left
            # Actual structure: name=ObjType, cooling_seq=Name, heating_seq=unknown number
            # For single equipment lists, sequences should both be 1
            actual_type = name
            actual_name = cooling_seq
            actual_cooling = str(idx)
            actual_heating = str(idx)

            corrected_equipment.append({
                'object_type': actual_type,
                'name': actual_name,
                'cooling_seq': actual_cooling,
                'heating_seq': actual_heating
            })

        elif obj_type != "" and not cooling_seq.replace('.', '').isdigit():
            # Cooling sequence has a name (wrong data type)
            # Assume it's part of continued corruption
            # Assign sequential numbers
            corrected_equipment.append({
                'object_type': obj_type,
                'name': name,
                'cooling_seq': str(idx),
                'heating_seq': str(idx)
            })

        else:
            # Appears correct, keep as-is
            corrected_equipment.append({
                'object_type': obj_type if obj_type else "",
                'name': name if name else "",
                'cooling_seq': cooling_seq if cooling_seq.replace('.', '').isdigit() else str(idx),
                'heating_seq': heating_seq if heating_seq.replace('.', '').isdigit() else str(idx)
            })

    # Create new equipment list object
    new_eq_list = idf.newidfobject('ZoneHVAC:EquipmentList')
    new_eq_list.Name = analysis['name']
    new_eq_list.Load_Distribution_Scheme = analysis['scheme']

    # Add corrected equipment
    for idx, eq in enumerate(corrected_equipment, start=1):
        setattr(new_eq_list, f'Zone_Equipment_{idx}_Object_Type', eq['object_type'])
        setattr(new_eq_list, f'Zone_Equipment_{idx}_Name', eq['name'])
        setattr(new_eq_list, f'Zone_Equipment_{idx}_Cooling_Sequence', eq['cooling_seq'])
        setattr(new_eq_list, f'Zone_Equipment_{idx}_Heating_or_NoLoad_Sequence', eq['heating_seq'])
        setattr(new_eq_list, f'Zone_Equipment_{idx}_Sequential_Cooling_Fraction_Schedule_Name', '')
        setattr(new_eq_list, f'Zone_Equipment_{idx}_Sequential_Heating_Fraction_Schedule_Name', '')

    return new_eq_list


def update_idf_version(idf, target_version="25.1"):
    """
    Update IDF Version object to target version

    Args:
        idf: IDF object
        target_version: Target EnergyPlus version (default: "25.1")

    Returns:
        bool: True if version was updated, False if already correct
    """
    try:
        version_objs = idf.idfobjects['Version']
        if len(version_objs) == 0:
            # No version object, create one
            version_obj = idf.newidfobject('Version')
            version_obj.Version_Identifier = target_version
            return True

        # Get current version
        current_version = version_objs[0].Version_Identifier

        if current_version != target_version:
            # Update version
            version_objs[0].Version_Identifier = target_version
            return True

        return False
    except Exception as e:
        print(f"    WARNING: Could not update version: {e}")
        return False


def fix_equipment_lists(input_path, output_path, idd_path=None):
    """
    Main function to fix all ZoneHVAC:EquipmentList objects in an IDF file

    Args:
        input_path: Path to input IDF file
        output_path: Path to output fixed IDF file
        idd_path: Path to Energy+.idd (optional)

    Returns:
        dict: Summary of fixes applied
    """

    print("=" * 80)
    print("FIX ZONEHVAC:EQUIPMENTLIST OBJECTS")
    print("=" * 80)

    # Auto-detect IDD if not provided
    if idd_path is None:
        print("\nAuto-detecting Energy+.idd...")
        idd_path = find_energyplus_idd()
        if idd_path is None:
            print("ERROR: Could not find Energy+.idd")
            print("Specify with --idd-path or set ENERGYPLUS_DIR environment variable")
            return None
        print(f"  Found: {idd_path}")

    # Set IDD
    try:
        IDF.setiddname(idd_path)
    except Exception as e:
        print(f"ERROR: Failed to load IDD file: {e}")
        return None

    # Load IDF
    print(f"\nLoading IDF: {input_path}")
    try:
        idf = IDF(input_path)
    except Exception as e:
        print(f"ERROR: Failed to load IDF file: {e}")
        return None

    print(f"  Loaded {len(idf.idfobjects)} object types")

    # Update IDF version to match IDD
    print("\nUpdating IDF version...")
    version_updated = update_idf_version(idf, target_version="25.1")
    if version_updated:
        print("  [OK] Updated version to 25.1")
    else:
        print("  [OK] Version already correct")

    # Get all equipment lists
    try:
        equipment_lists = idf.idfobjects['ZoneHVAC:EquipmentList']
    except KeyError:
        print("WARNING: No ZoneHVAC:EquipmentList objects found")
        equipment_lists = []

    print(f"\nFound {len(equipment_lists)} ZoneHVAC:EquipmentList objects")

    if len(equipment_lists) == 0:
        print("Nothing to fix. Exiting.")
        return {'fixed': 0, 'total': 0}

    # Analyze each equipment list
    print("\nAnalyzing equipment lists...")
    analyses = []
    corrupted_count = 0

    for eq_list in equipment_lists:
        analysis = analyze_equipment_list(eq_list)
        analyses.append(analysis)

        if analysis['is_corrupted']:
            corrupted_count += 1
            print(f"\n  [CORRUPTED] {analysis['name']}")
            for issue in analysis['issues']:
                print(f"    - {issue}")
        else:
            print(f"  [OK] {analysis['name']}")

    print(f"\n  Total corrupted: {corrupted_count} / {len(equipment_lists)}")

    if corrupted_count == 0:
        print("\nNo corrupted equipment lists found. No fixes needed.")
        print(f"Saving unchanged file to: {output_path}")
        idf.saveas(output_path)
        return {'fixed': 0, 'total': len(equipment_lists)}

    # Fix corrupted equipment lists
    print(f"\nFixing {corrupted_count} corrupted equipment lists...")

    # Remove all existing equipment lists (clear list completely to avoid duplicates)
    print("  Removing all existing ZoneHVAC:EquipmentList objects...")
    while len(idf.idfobjects['ZoneHVAC:EquipmentList']) > 0:
        idf.popidfobject('ZoneHVAC:EquipmentList', 0)
    print(f"    [OK] Removed {len(equipment_lists)} equipment lists")

    # Reconstruct all equipment lists (corrupted and clean)
    fixed_count = 0
    print("  Reconstructing equipment lists with correct structure...")
    for analysis in analyses:
        new_eq_list = reconstruct_equipment_list(idf, analysis)

        if analysis['is_corrupted']:
            fixed_count += 1
            print(f"  [FIXED] {analysis['name']}")
            print(f"    Equipment count: {len(analysis['equipment'])}")

    # Save fixed IDF
    print(f"\nSaving fixed IDF to: {output_path}")
    try:
        idf.saveas(output_path)
        print("  [OK] File saved successfully")
    except Exception as e:
        print(f"  ERROR: Failed to save file: {e}")
        return None

    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"  Total equipment lists: {len(equipment_lists)}")
    print(f"  Corrupted: {corrupted_count}")
    print(f"  Fixed: {fixed_count}")
    print(f"  Output file: {output_path}")
    print("\nNext steps:")
    print("  1. Run EnergyPlus on the fixed IDF file")
    print("  2. Check eplusout.err for any remaining errors")
    print("=" * 80)

    return {
        'fixed': fixed_count,
        'total': len(equipment_lists),
        'output_file': output_path
    }


def main():
    """Main entry point"""

    parser = argparse.ArgumentParser(
        description='Fix ZoneHVAC:EquipmentList objects with misaligned fields',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python fix-equipment-lists.py in_cleaned.idf in_fixed.idf
  python fix-equipment-lists.py model.idf model_fixed.idf --idd-path C:/EnergyPlusV25-1-0/Energy+.idd

Common Issues Fixed:
  - Equipment names in numeric sequence fields
  - Shifted field positions (missing first equipment entry)
  - Blank required fields
  - Non-numeric values in sequence fields
        """
    )

    parser.add_argument('input_idf', help='Path to input IDF file')
    parser.add_argument('output_idf', help='Path to output fixed IDF file')
    parser.add_argument('--idd-path', help='Path to Energy+.idd file (optional, auto-detected)')

    args = parser.parse_args()

    # Validate input file exists
    if not os.path.exists(args.input_idf):
        print(f"ERROR: Input file not found: {args.input_idf}")
        sys.exit(1)

    # Run fix
    result = fix_equipment_lists(args.input_idf, args.output_idf, args.idd_path)

    if result is None:
        sys.exit(1)

    # Exit with appropriate code
    if result['fixed'] > 0:
        print(f"\n[OK] Successfully fixed {result['fixed']} equipment lists")
        sys.exit(0)
    else:
        print("\n[OK] No fixes needed")
        sys.exit(0)


if __name__ == '__main__':
    main()
