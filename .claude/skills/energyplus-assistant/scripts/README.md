# EnergyPlus Assistant Scripts

Python tools for IDF manipulation and validation following the philosophy: **"Let tools handle syntax, let humans handle logic."**

## Available Scripts

### fix-equipment-lists.py

**Purpose:** Automatically detect and repair corrupted ZoneHVAC:EquipmentList objects + update IDF version

**When to use:**
- Fatal errors from ZoneHVAC:EquipmentList objects
- Field shifting (data in wrong positions)
- IDF version mismatch between file and EnergyPlus installation
- Duplicate object errors

**Usage:**
```bash
python fix-equipment-lists.py input.idf output.idf
```

**What it fixes:**
1. **Corruption Detection:**
   - Blank object types with present names (field shift)
   - Equipment names in numeric sequence fields
   - Non-numeric values in cooling/heating sequence fields

2. **Automatic Repair:**
   - Removes ALL corrupted equipment lists (no duplicates)
   - Reconstructs with correct field structure
   - Sets proper cooling/heating sequences (1, 2, 3...)

3. **Version Update:**
   - Auto-detects IDF version (e.g., 24.2)
   - Updates to match installed EnergyPlus (e.g., 25.1)
   - No separate transition tool needed

**Example Error Fixed:**
```
** Severe ** processZoneEquipmentInput: ZoneHVAC:EquipmentList = "THERMAL ZONE: CARDIO 1 EQUIPMENT LIST".
**   ~~~   ** invalid zone_equipment_cooling_sequence=[2].
**   ~~~   ** equipment sequence must be > 0 and <= number of equipments in the list.
**   ~~~   ** only 1 in the list.
**  Fatal  ** GetZoneEquipmentData: Errors found in getting Zone Equipment input.
```

**Dependencies:**
```bash
pip install eppy
```

**Technical Details:**
- Uses eppy for reliable IDF parsing and manipulation
- Auto-detects Energy+.idd from common installation locations
- Windows-safe (handles console encoding issues)
- No duplicates created (complete removal before reconstruction)
- Validated on EnergyPlus v25.1.0

---

### qaqc-direct.py

**Purpose:** Fast pre-simulation QA/QC validation without Docker

**When to use:**
- Quick validation before running simulation
- Object counting and inventory
- Basic structural checks
- When Docker/MCP not available

**Usage:**
```bash
python qaqc-direct.py model.idf
```

**What it checks:**
- Building, zones, surfaces, fenestration
- Constructions and materials
- HVAC systems (air loops, plant loops, zone equipment)
- Internal loads (people, lights, equipment)
- Simulation settings
- Output variables

**Speed:** < 5 seconds (10x faster than Docker/MCP)

**Dependencies:**
```bash
pip install eppy
```

---

### validate-idf-structure.py

**Purpose:** Pre-flight validation to catch field type errors, missing references, and structural issues before simulation

**When to use:**
- Before running any simulation (catch errors in < 10 seconds)
- After manual IDF edits
- After using OpenStudio or other modeling tools
- When troubleshooting simulation failures

**Usage:**
```bash
# Basic validation (all checks)
python validate-idf-structure.py model.idf

# Generate detailed report
python validate-idf-structure.py model.idf --report validation_report.md

# Specific validation categories only
python validate-idf-structure.py model.idf --check fields,references,nodes

# Filter by severity level
python validate-idf-structure.py model.idf --severity error --report errors_only.md
```

**What it validates:**

1. **Field Types:**
   - Numeric fields contain numbers (not text)
   - String fields are valid
   - Choice fields have valid options from IDD

2. **Required Fields:**
   - All required fields are present (not blank)
   - Validates against IDD schema

3. **Object References:**
   - Schedule references point to existing schedules
   - Material references exist
   - Construction references exist
   - All object name references are valid

4. **Node Connections:**
   - Inlet/outlet node pairs match
   - No orphaned nodes (defined but unused)
   - HVAC node connection graph is complete

5. **Surface Geometry:**
   - Surfaces have >= 3 vertices
   - No coincident vertices (degenerate surfaces)
   - Valid surface normal direction

**Speed:** < 10 seconds (much faster than running 3-minute simulation)

**Output Example:**
```
================================================================================
VALIDATE IDF STRUCTURE
================================================================================

Input: model.idf
IDD Version: 25.1

Running validation checks...
  [OK] Field type validation
  [OK] Required fields check
  [WARNING] Object reference validation (3 issues found)
  [OK] Node connection validation
  [OK] Surface geometry validation

================================================================================
VALIDATION SUMMARY
================================================================================
  Total Objects: 1,561
  Errors: 0
  Warnings: 3
  Info: 0

RECOMMENDATION: Review warnings - may cause simulation issues

See detailed report: validation_report.md
```

**Markdown Report Structure:**
- Summary table with error counts by category
- Detailed list of all errors with object names and field names
- Actionable recommendations for fixing issues
- Reference to related fix scripts (fix-node-connections.py, fix-schedules.py)

**Dependencies:**
```bash
pip install eppy
```

**Technical Details:**
- Uses eppy for IDF parsing
- Leverages IDD schema for field metadata
- Builds object reference maps for validation
- Node validation uses graph analysis
- Geometry checks use vector math (optional)

**Related Scripts:**
- fix-node-connections.py - Automatically fix node issues found
- fix-schedules.py - Automatically fix schedule reference issues
- fix-surface-geometry.py - Automatically fix geometry issues (coming soon)

---

## Philosophy

These tools follow a **tool-based workflow** approach:

1. **Tools handle syntax** - eppy ensures correct IDF format
2. **Humans handle logic** - You specify what fields should contain
3. **Automation ensures consistency** - Scripts guarantee proper structure

This approach minimizes manual editing errors and ensures reliably formatted IDF files.

---

## Coming Soon

- **validate-idf-fields.py** - Pre-flight field validation
- **add-outputs.py** - Automated output variable injection
- **run-energyplus.py** - Simulation orchestration wrapper

---

## Support

For issues or questions, see the main skill documentation:
- [SKILL.md](../SKILL.md) - Main skill reference
- [direct-parsing-methods.md](../direct-parsing-methods.md) - Detailed Python/eppy usage
- [windows-setup.md](../windows-setup.md) - Windows-specific guidance
