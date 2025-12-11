"""
EnergyPlus IDF QA/QC Analysis Script
Performs comprehensive pre-simulation validation on IDF models
"""

import sys
from pathlib import Path
from eppy.modeleditor import IDF

def analyze_idf(idf_path):
    """Perform comprehensive QA/QC on an IDF file"""

    print("=" * 80)
    print(f"ENERGYPLUS IDF QA/QC REPORT")
    print("=" * 80)
    print(f"Model: {Path(idf_path).name}")
    print(f"Path: {idf_path}")
    print("=" * 80)

    try:
        # Try to load IDF without IDD first (faster)
        print("\n[1/8] Loading IDF file...")
        with open(idf_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # Basic file checks
        print(f"  File size: {len(content):,} characters")
        print(f"  [OK] File loaded successfully")

        # Count major object types by simple parsing
        print("\n[2/8] Analyzing object structure...")

        # Split into objects
        objects = content.split(';')
        total_objects = len([obj for obj in objects if obj.strip()])
        print(f"  Total objects: {total_objects:,}")

        # Count key object types
        object_counts = {}
        key_objects = [
            'Building,',
            'Zone,',
            'BuildingSurface:Detailed,',
            'FenestrationSurface:Detailed,',
            'Construction,',
            'Material,',
            'Material:NoMass,',
            'Schedule:',
            'People,',
            'Lights,',
            'ElectricEquipment,',
            'ZoneInfiltration:',
            'ZoneVentilation:',
            'HVACTemplate:',
            'AirLoopHVAC,',
            'PlantLoop,',
            'CondenserLoop,',
            'Boiler:',
            'Chiller:',
            'Coil:',
            'Fan:',
            'Pump:',
            'WaterHeater:',
            'ZoneHVAC:',
            'AirTerminal:',
            'Output:Variable,',
            'Output:Meter,',
            'SimulationControl,',
            'RunPeriod,'
        ]

        for obj_type in key_objects:
            count = content.upper().count(obj_type.upper())
            if count > 0:
                object_counts[obj_type.strip(',')] = count

        # Print object counts
        print("\n[3/8] Object Count Summary:")
        print("  " + "-" * 70)

        # Core building objects
        core_objects = ['Building', 'Zone', 'BuildingSurface:Detailed',
                       'FenestrationSurface:Detailed', 'Construction',
                       'Material', 'Material:NoMass']
        print("  CORE BUILDING OBJECTS:")
        for obj in core_objects:
            count = object_counts.get(obj, 0)
            status = "[OK]" if count > 0 else "[  ]"
            print(f"    {status} {obj:40} {count:6,}")

        # Loads
        loads_objects = ['Schedule', 'People', 'Lights', 'ElectricEquipment',
                        'ZoneInfiltration', 'ZoneVentilation']
        print("\n  LOADS & SCHEDULES:")
        for obj in loads_objects:
            # Count all schedule types
            if obj == 'Schedule':
                count = sum(v for k, v in object_counts.items() if 'Schedule' in k)
            else:
                count = sum(v for k, v in object_counts.items() if obj in k)
            status = "[OK]" if count > 0 else "[  ]"
            print(f"    {status} {obj:40} {count:6,}")

        # HVAC
        hvac_objects = ['HVACTemplate', 'AirLoopHVAC', 'PlantLoop', 'CondenserLoop',
                       'Boiler', 'Chiller', 'Coil', 'Fan', 'Pump', 'WaterHeater',
                       'ZoneHVAC', 'AirTerminal']
        print("\n  HVAC SYSTEMS:")
        for obj in hvac_objects:
            count = sum(v for k, v in object_counts.items() if obj in k)
            status = "[OK]" if count > 0 else "[  ]" if obj in ['AirLoopHVAC', 'ZoneHVAC'] else " -  "
            print(f"    {status} {obj:40} {count:6,}")

        # Simulation settings
        sim_objects = ['SimulationControl', 'RunPeriod']
        print("\n  SIMULATION SETTINGS:")
        for obj in sim_objects:
            count = object_counts.get(obj, 0)
            status = "[OK]" if count > 0 else "[!!]"
            print(f"    {status} {obj:40} {count:6,}")

        # Outputs
        output_objects = ['Output:Variable', 'Output:Meter']
        print("\n  OUTPUTS:")
        for obj in output_objects:
            count = object_counts.get(obj, 0)
            status = "[OK]" if count > 0 else "[!!]"
            print(f"    {status} {obj:40} {count:6,}")

        print("\n[4/8] Checking zones...")
        zone_count = object_counts.get('Zone', 0)
        if zone_count > 0:
            print(f"  [OK] Found {zone_count} thermal zones")
        else:
            print("  [ERROR] No thermal zones found!")

        print("\n[5/8] Checking surfaces...")
        surface_count = object_counts.get('BuildingSurface:Detailed', 0)
        window_count = object_counts.get('FenestrationSurface:Detailed', 0)
        if surface_count > 0:
            print(f"  [OK] Found {surface_count:,} building surfaces")
            print(f"  [OK] Found {window_count:,} fenestration surfaces")
        else:
            print("  [ERROR] No building surfaces found!")

        print("\n[6/8] Checking constructions and materials...")
        construction_count = object_counts.get('Construction', 0)
        material_count = object_counts.get('Material', 0) + object_counts.get('Material:NoMass', 0)
        if construction_count > 0 and material_count > 0:
            print(f"  [OK] Found {construction_count} constructions")
            print(f"  [OK] Found {material_count} materials")
        else:
            print(f"  [!!] WARNING: Low construction/material count")
            print(f"    Constructions: {construction_count}, Materials: {material_count}")

        print("\n[7/8] Checking HVAC systems...")
        airloop_count = object_counts.get('AirLoopHVAC', 0)
        plant_count = object_counts.get('PlantLoop', 0)
        condenser_count = object_counts.get('CondenserLoop', 0)
        zonehvac_count = sum(v for k, v in object_counts.items() if 'ZoneHVAC' in k)

        if airloop_count > 0 or zonehvac_count > 0:
            print(f"  [OK] Found HVAC systems:")
            if airloop_count > 0:
                print(f"    - {airloop_count} air loops")
            if plant_count > 0:
                print(f"    - {plant_count} plant loops")
            if condenser_count > 0:
                print(f"    - {condenser_count} condenser loops")
            if zonehvac_count > 0:
                print(f"    - {zonehvac_count} zone HVAC equipment")
        else:
            print("  [!!] WARNING: No HVAC systems found")
            print("    Model may have HVACTemplate objects or Ideal Loads")

        print("\n[8/8] Checking simulation settings...")
        if object_counts.get('SimulationControl', 0) > 0:
            print("  [OK] SimulationControl object found")
        else:
            print("  [!!] WARNING: No SimulationControl object found")

        if object_counts.get('RunPeriod', 0) > 0:
            print(f"  [OK] RunPeriod object(s) found: {object_counts.get('RunPeriod', 0)}")
        else:
            print("  [!!] WARNING: No RunPeriod object found")

        # Summary
        print("\n" + "=" * 80)
        print("SUMMARY")
        print("=" * 80)

        critical_errors = []
        warnings = []

        # Check for critical issues
        if zone_count == 0:
            critical_errors.append("No thermal zones defined")
        if surface_count == 0:
            critical_errors.append("No building surfaces defined")
        if construction_count == 0:
            critical_errors.append("No constructions defined")
        if material_count == 0:
            critical_errors.append("No materials defined")

        # Check for warnings
        if object_counts.get('SimulationControl', 0) == 0:
            warnings.append("No SimulationControl object - defaults will be used")
        if object_counts.get('RunPeriod', 0) == 0:
            warnings.append("No RunPeriod object - may only run design days")
        if airloop_count == 0 and zonehvac_count == 0:
            warnings.append("No HVAC systems found - verify HVACTemplate or Ideal Loads")
        if object_counts.get('Output:Variable', 0) == 0:
            warnings.append("No output variables requested - limited results")

        if critical_errors:
            print("\n[ERROR] CRITICAL ERRORS FOUND:")
            for i, err in enumerate(critical_errors, 1):
                print(f"  {i}. {err}")
            print("\n  STATUS: [ERROR] MODEL NOT READY FOR SIMULATION")
        elif warnings:
            print("\n[!!] WARNINGS FOUND:")
            for i, warn in enumerate(warnings, 1):
                print(f"  {i}. {warn}")
            print("\n  STATUS: [!!] MODEL MAY SIMULATE BUT REVIEW WARNINGS")
        else:
            print("\n[OK] NO CRITICAL ISSUES FOUND")
            print("  STATUS: [OK] MODEL APPEARS READY FOR SIMULATION")

        print("\n" + "=" * 80)
        print("MODEL STATISTICS:")
        print("=" * 80)
        print(f"  Total objects: {total_objects:,}")
        print(f"  Zones: {zone_count}")
        print(f"  Surfaces: {surface_count:,}")
        print(f"  Windows: {window_count:,}")
        print(f"  Constructions: {construction_count}")
        print(f"  Materials: {material_count}")
        print(f"  HVAC Equipment: {airloop_count + plant_count + condenser_count + zonehvac_count}")
        print("=" * 80)

    except FileNotFoundError:
        print(f"\n[ERROR] File not found: {idf_path}")
        return 1
    except Exception as e:
        print(f"\n[ERROR] Failed to analyze IDF: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

    return 0

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python qaqc_analysis.py <path_to_idf_file>")
        sys.exit(1)

    idf_path = sys.argv[1]
    sys.exit(analyze_idf(idf_path))
