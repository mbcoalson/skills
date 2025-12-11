# EnergyPlus Assistant - Python Toolkit Development Plan

**Created:** 2025-11-24
**Status:** Active Development
**Philosophy:** "Let tools handle syntax, let humans handle logic"

---

## Development Tracker

### Phase 1: Foundation & Critical Tools (Week 1-2)
- [x] **qaqc-direct.py** - Pre-simulation validation (COMPLETED)
- [x] **fix-equipment-lists.py** - Repair corrupt equipment lists (COMPLETED)
- [x] **validate-idf-structure.py** - Comprehensive field validation (COMPLETED 2025-11-24)
- [ ] **add-standard-outputs.py** - Inject output variables (NEXT)
- [ ] **extract-results.py** - Parse results for deliverables (NEXT)

### Phase 2: Error Handling & Repair (Week 3-4)
- [ ] **fix-node-connections.py** - Repair HVAC node connections
- [ ] **fix-schedules.py** - Repair schedule references
- [ ] **fix-surface-geometry.py** - Repair degenerate surfaces

### Phase 3: Equipment Manipulation (Week 5-6)
- [ ] **add-ideal-loads.py** - Replace HVAC with ideal loads
- [ ] **clone-hvac-system.py** - Duplicate HVAC to new zones
- [ ] **swap-hvac-type.py** - Replace HVAC system type

### Phase 4: ECM & Parametric Testing (Week 7-8)
- [ ] **apply-ecm-lighting.py** - LPD reduction ECM
- [ ] **apply-ecm-envelope.py** - Insulation/window ECM
- [ ] **apply-ecm-schedules.py** - Schedule modification ECM
- [ ] **run-parametric.py** - Orchestrate parametric studies

### Phase 5: Utilities (Week 9-10)
- [ ] **compare-models.py** - Diff two IDF files
- [ ] **merge-idf-objects.py** - Copy objects between files
- [ ] **clean-unused-objects.py** - Remove orphaned objects

---

## Design Standards

### Common Requirements for ALL Scripts

#### 1. **Dependencies**
- **Required:** `eppy` (IDF parsing and manipulation)
- **Optional:** `pandas` (only if processing tabular data)
- **Optional:** `pyyaml` (only if reading config files)
- **Avoid:** Heavy dependencies (numpy, scipy, etc.) unless absolutely necessary

#### 2. **Command-Line Interface**
```python
# Standard argparse structure
import argparse

def main():
    parser = argparse.ArgumentParser(
        description="Brief description of what script does",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python script_name.py input.idf output.idf
  python script_name.py input.idf --option value --output output.idf
        """
    )

    # Common arguments (use consistently)
    parser.add_argument('input_idf', help='Input IDF file path')
    parser.add_argument('output_idf', nargs='?', help='Output IDF file path (optional)')
    parser.add_argument('--idd', help='Path to Energy+.idd (auto-detected if not provided)')
    parser.add_argument('--dry-run', action='store_true', help='Show changes without saving')
    parser.add_argument('--report', help='Output report file (markdown format)')
    parser.add_argument('--quiet', action='store_true', help='Suppress progress messages')
    parser.add_argument('--output', '-o', dest='output_idf', help='Output IDF file path')

    args = parser.parse_args()
    # ... rest of script
```

#### 3. **File Handling**
```python
# ALWAYS auto-detect IDD
def find_idd():
    """Auto-detect Energy+.idd from common installation locations"""
    common_locations = [
        r'C:/EnergyPlusV25-1-0/Energy+.idd',
        r'C:/EnergyPlusV24-2-0/Energy+.idd',
        r'/usr/local/EnergyPlus-25-1-0/Energy+.idd',
        r'/Applications/EnergyPlus-25-1-0/Energy+.idd'
    ]
    for loc in common_locations:
        if os.path.exists(loc):
            return loc
    return None

# ALWAYS validate input file exists
if not os.path.exists(args.input_idf):
    print(f"ERROR: Input file not found: {args.input_idf}")
    sys.exit(1)

# NEVER overwrite input file
if args.output_idf == args.input_idf:
    print("ERROR: Output file cannot be same as input file")
    sys.exit(1)
```

#### 4. **Output Format**
```python
# Use consistent formatting (no emojis for Windows compatibility)
print("=" * 80)
print("SCRIPT NAME - DESCRIPTION")
print("=" * 80)

# Use clear status indicators
print("[OK] Operation succeeded")
print("[ERROR] Operation failed")
print("[WARNING] Potential issue detected")
print("[INFO] Informational message")

# Progress indicators
print(f"\nProcessing {total} objects...")
print(f"  [1/{total}] Processing object...")
```

#### 5. **Error Handling**
```python
# Wrap main operations in try/except
try:
    IDF.setiddname(idd_path)
    idf = IDF(input_path)
except Exception as e:
    print(f"[ERROR] Failed to load IDF: {e}")
    sys.exit(1)

# Always provide actionable error messages
if len(missing_objects) > 0:
    print(f"[ERROR] Missing {len(missing_objects)} required objects:")
    for obj in missing_objects[:5]:  # Show first 5
        print(f"  - {obj}")
    if len(missing_objects) > 5:
        print(f"  ... and {len(missing_objects) - 5} more")
```

#### 6. **Reporting**
```python
# Generate markdown reports when --report specified
def generate_report(results, output_path):
    """Generate markdown report of changes"""
    with open(output_path, 'w') as f:
        f.write(f"# {SCRIPT_NAME} Report\n\n")
        f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**Input:** {results['input_file']}\n\n")
        f.write(f"**Output:** {results['output_file']}\n\n")
        f.write("## Summary\n\n")
        # ... write summary statistics
        f.write("## Details\n\n")
        # ... write detailed changes
```

#### 7. **Return Codes**
```python
# Use standard exit codes
sys.exit(0)  # Success
sys.exit(1)  # General error
sys.exit(2)  # Invalid arguments
sys.exit(3)  # File not found
```

---

## Script Specifications

---

### **validate-idf-structure.py**

**Priority:** CRITICAL (Phase 1)
**Status:** Not Started
**Estimated Effort:** 2 days

#### Purpose
Pre-flight validation to catch field type errors, missing references, and structural issues before simulation.

#### Key Features
1. Field type validation (numeric vs string)
2. Required field presence check
3. Object reference validation (schedules, materials, constructions exist)
4. Node connection validation (inlet/outlet pairs)
5. Geometry validation (surfaces planar, non-zero area)

#### Command-Line Interface
```bash
# Basic validation
python validate-idf-structure.py model.idf

# With report output
python validate-idf-structure.py model.idf --report validation_report.md

# Specific validation categories
python validate-idf-structure.py model.idf --check fields,references,nodes
```

#### Arguments
- `input_idf` - Input IDF file
- `--idd` - Path to Energy+.idd (auto-detected if not provided)
- `--report` - Output markdown report
- `--check` - Comma-separated validation categories (default: all)
  - `fields` - Field type validation
  - `references` - Object reference validation
  - `nodes` - Node connection validation
  - `geometry` - Surface geometry validation
  - `schedules` - Schedule validation
- `--severity` - Minimum severity to report (info, warning, error, fatal)
- `--quiet` - Suppress console output

#### Algorithm
```python
1. Load IDF with eppy
2. Get IDD schema for field definitions
3. For each object type:
   a. For each field:
      - Check type matches IDD (numeric, alpha, choice)
      - Check required fields not blank
      - Check choice fields have valid values
   b. For reference fields:
      - Build map of available objects (by name)
      - Check references point to existing objects
   c. For nodes:
      - Build node connection graph
      - Check inlet/outlet pairs match
      - Identify orphaned nodes
4. For surfaces:
   a. Check vertex count >= 3
   b. Check vertices not coincident
   c. Check surface planar (optional, expensive)
5. Generate validation report
6. Return exit code based on highest severity found
```

#### Output Format
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
  [ERROR] Node connection validation (12 issues found)
  [OK] Surface geometry validation

================================================================================
VALIDATION SUMMARY
================================================================================
  Total Objects: 1,561
  Errors: 12
  Warnings: 3
  Info: 0

RECOMMENDATION: Fix errors before running simulation

See detailed report: validation_report.md
```

#### Markdown Report Structure
```markdown
# IDF Validation Report

**Date:** 2025-11-24 14:30:00
**Input File:** model.idf
**IDF Version:** 24.2
**IDD Version:** 25.1

## Summary

| Category | Errors | Warnings | Info |
|----------|--------|----------|------|
| Field Types | 0 | 0 | 0 |
| Required Fields | 0 | 0 | 0 |
| Object References | 3 | 5 | 12 |
| Node Connections | 12 | 0 | 0 |
| Surface Geometry | 0 | 4 | 0 |
| **Total** | **15** | **9** | **12** |

## Errors (15)

### Node Connections (12 errors)

1. **AirLoopHVAC: VAV System 1**
   - Missing outlet node connection
   - Expected: Supply Air Outlet Node
   - Found: (blank)

[... detailed list ...]

## Warnings (9)

[... detailed list ...]

## Recommendations

1. Fix all errors before running simulation
2. Review warnings - may cause simulation issues
3. Consider updating IDF version from 24.2 to 25.1
```

#### Implementation Notes
- Use eppy's `idf.idfobjects` to iterate object types
- Use `obj.fieldnames` to get field names
- Use `obj.objls` to get list of field values
- IDD contains field metadata (type, required, reference)
- Build reference maps first, then validate references

#### Dependencies
- `eppy` - IDF parsing
- Standard library only (argparse, os, sys, datetime)

---

### **add-standard-outputs.py**

**Priority:** CRITICAL (Phase 1)
**Status:** Not Started
**Estimated Effort:** 1.5 days

#### Purpose
Inject comprehensive output variables to ensure all necessary data is captured without forgetting variables.

#### Key Features
1. Preset output configurations (LEED, comfort, HVAC, all)
2. Remove existing outputs (optional)
3. Add meter outputs
4. Add variable outputs
5. Set reporting frequency

#### Command-Line Interface
```bash
# Add LEED outputs
python add-standard-outputs.py model.idf --preset leed --output model_with_outputs.idf

# Add comfort outputs, keep existing
python add-standard-outputs.py model.idf --preset comfort --keep-existing

# Add custom variable list
python add-standard-outputs.py model.idf --variables vars.txt --output model_outputs.idf

# Multiple presets
python add-standard-outputs.py model.idf --preset leed,hvac,comfort
```

#### Arguments
- `input_idf` - Input IDF file
- `output_idf` - Output IDF file
- `--preset` - Comma-separated preset names (leed, comfort, hvac, energy, all)
- `--variables` - Text file with variable names (one per line)
- `--meters` - Text file with meter names (one per line)
- `--frequency` - Reporting frequency (hourly, daily, monthly, runperiod, annual)
- `--keep-existing` - Don't remove existing output variables
- `--report` - Output report of variables added

#### Output Presets

**LEED Preset:**
```python
LEED_OUTPUTS = {
    'variables': [
        'Zone Mean Air Temperature',
        'Zone Air System Sensible Heating Energy',
        'Zone Air System Sensible Cooling Energy',
        'Zone Lights Electricity Energy',
        'Zone Electric Equipment Electricity Energy',
    ],
    'meters': [
        'Electricity:Facility',
        'NaturalGas:Facility',
        'Heating:Electricity',
        'Cooling:Electricity',
        'InteriorLights:Electricity',
        'InteriorEquipment:Electricity',
        'Fans:Electricity',
        'Pumps:Electricity',
    ],
    'frequency': 'monthly'
}
```

**Comfort Preset:**
```python
COMFORT_OUTPUTS = {
    'variables': [
        'Zone Mean Air Temperature',
        'Zone Air Relative Humidity',
        'Zone Thermal Comfort Fanger Model PMV',
        'Zone Thermal Comfort Fanger Model PPD',
        'Zone Air System Sensible Heating Rate',
        'Zone Air System Sensible Cooling Rate',
    ],
    'meters': [],
    'frequency': 'hourly'
}
```

**HVAC Preset:**
```python
HVAC_OUTPUTS = {
    'variables': [
        'Air System Total Heating Energy',
        'Air System Total Cooling Energy',
        'Fan Electricity Rate',
        'Cooling Coil Electricity Rate',
        'Heating Coil Electricity Rate',
        'Pump Electricity Rate',
    ],
    'meters': [
        'Fans:Electricity',
        'Cooling:Electricity',
        'Heating:Electricity',
        'Pumps:Electricity',
    ],
    'frequency': 'hourly'
}
```

**Energy Preset (default for deliverables):**
```python
ENERGY_OUTPUTS = {
    'variables': [],
    'meters': [
        'Electricity:Facility',
        'NaturalGas:Facility',
        'DistrictHeating:Facility',
        'DistrictCooling:Facility',
        'Heating:Electricity',
        'Heating:NaturalGas',
        'Cooling:Electricity',
        'InteriorLights:Electricity',
        'ExteriorLights:Electricity',
        'InteriorEquipment:Electricity',
        'ExteriorEquipment:Electricity',
        'Fans:Electricity',
        'Pumps:Electricity',
        'WaterSystems:Electricity',
        'WaterSystems:NaturalGas',
    ],
    'frequency': 'monthly'
}
```

#### Algorithm
```python
1. Load IDF with eppy
2. If not --keep-existing:
   a. Remove all Output:Variable objects
   b. Remove all Output:Meter objects
3. For each preset specified:
   a. Get variable list from preset definition
   b. Get meter list from preset definition
   c. Get frequency from preset (or use --frequency override)
4. For each variable:
   a. Create Output:Variable object
   b. Set Key Value = "*" (all instances)
   c. Set Variable Name
   d. Set Reporting Frequency
5. For each meter:
   a. Create Output:Meter object
   b. Set Key Name
   c. Set Reporting Frequency
6. Add Output:Table:SummaryReports if not present
   a. AllSummary report
7. Save modified IDF
8. Generate report if requested
```

#### Output Format
```
================================================================================
ADD STANDARD OUTPUTS
================================================================================

Input: model.idf
Output: model_with_outputs.idf

Adding outputs for presets: leed, energy

Removing existing outputs...
  Removed 5 Output:Variable objects
  Removed 2 Output:Meter objects

Adding LEED preset outputs...
  [OK] Added 5 variables (monthly)
  [OK] Added 8 meters (monthly)

Adding Energy preset outputs...
  [OK] Added 0 variables
  [OK] Added 15 meters (monthly)

Adding Output:Table:SummaryReports...
  [OK] Added AllSummary report

================================================================================
SUMMARY
================================================================================
  Variables Added: 5
  Meters Added: 23 (15 + 8)
  Reporting Frequency: monthly
  Output File: model_with_outputs.idf
================================================================================
```

#### Implementation Notes
- Use `idf.newidfobject('Output:Variable')` to create new outputs
- Set fields using attribute access: `var.Key_Value = '*'`
- Check if Output:Table:SummaryReports exists before adding
- Allow multiple presets (combine all variables/meters)

#### Dependencies
- `eppy` - IDF manipulation
- Standard library only

---

### **extract-results.py**

**Priority:** CRITICAL (Phase 1)
**Status:** Not Started
**Estimated Effort:** 2 days

#### Purpose
Parse EnergyPlus HTML output tables and extract key metrics (EUI, GHG, costs) for deliverables.

#### Key Features
1. Parse eplustbl.htm HTML tables
2. Extract energy consumption by fuel and end use
3. Calculate EUI (site and source)
4. Calculate GHG emissions (with carbon factors)
5. Extract utility costs
6. Output in multiple formats (CSV, JSON, Markdown, Excel)

#### Command-Line Interface
```bash
# Basic extraction to markdown
python extract-results.py output/eplustbl.htm --format markdown --output results.md

# Extract specific metrics to CSV
python extract-results.py output/eplustbl.htm --metrics eui,ghg,cost --format csv --output results.csv

# With custom carbon factors
python extract-results.py output/eplustbl.htm --carbon-elec 0.42 --carbon-gas 0.18 --format json

# Compare baseline vs proposed
python extract-results.py baseline/eplustbl.htm proposed/eplustbl.htm --compare --output comparison.md
```

#### Arguments
- `html_file` - Path to eplustbl.htm (can specify 2 for comparison)
- `--format` - Output format (markdown, csv, json, excel)
- `--output` - Output file path
- `--metrics` - Comma-separated metrics to extract (eui, ghg, cost, enduse, all)
- `--carbon-elec` - Electric carbon factor (kg CO2/kWh) [default: 0.42]
- `--carbon-gas` - Natural gas carbon factor (kg CO2/kWh) [default: 0.18]
- `--carbon-district-heating` - District heating carbon factor
- `--carbon-district-cooling` - District cooling carbon factor
- `--area-override` - Override building area (sq ft or sq m)
- `--compare` - Compare two HTML files (baseline vs proposed)

#### Metrics to Extract

**EUI (Energy Use Intensity):**
- Total Site Energy (kBtu/sq ft/yr or kWh/sq m/yr)
- Total Source Energy
- By fuel type (electricity, gas, district)
- By end use (heating, cooling, lighting, equipment, etc.)

**GHG (Greenhouse Gas Emissions):**
- Total emissions (kg CO2e or metric tons CO2e)
- By fuel type
- By end use
- Emissions intensity (kg CO2e/sq ft/yr)

**Utility Costs:**
- Total annual cost ($)
- By fuel type
- By end use
- Cost intensity ($/sq ft/yr)

**End Use Breakdown:**
- Heating energy & cost
- Cooling energy & cost
- Interior lighting energy & cost
- Interior equipment energy & cost
- Fans energy & cost
- Pumps energy & cost
- Service water heating energy & cost

**Unmet Hours:**
- Heating unmet hours
- Cooling unmet hours

**Peak Demand:**
- Peak electric demand (kW)
- Peak heating demand (kBtu/hr)
- Peak cooling demand (tons)

#### Algorithm
```python
1. Parse HTML using BeautifulSoup or similar
2. Locate "Annual Building Utility Performance Summary" table
3. Extract total energy by fuel type
4. Locate "End Uses" table
5. Extract energy by end use and fuel
6. Locate "Building Area" from "Building Summary" table
7. Calculate EUI = Total Energy / Building Area
8. Calculate GHG:
   a. For each fuel type:
      emissions = energy * carbon_factor
   b. Sum all fuel emissions
9. Extract utility costs from "Economics Results Summary Report"
10. If --compare specified:
    a. Extract metrics from both files
    b. Calculate differences and percent changes
11. Format output according to --format
12. Write to file or stdout
```

#### Output Format - Markdown Example
```markdown
# EnergyPlus Simulation Results

**Date:** 2025-11-24
**Model:** SECC_WSHP_ProposedModel_v3
**HTML File:** output_fixed_v3/eplustbl.htm

## Building Summary

| Metric | Value |
|--------|-------|
| Total Building Area | 50,000 sq ft |
| Conditioned Area | 48,500 sq ft |
| Climate Zone | 5B |

## Energy Use Intensity (EUI)

| Fuel Type | Annual Energy | EUI |
|-----------|---------------|-----|
| Electricity | 1,250,000 kWh | 25.0 kWh/sq ft/yr |
| Natural Gas | 2,500 MMBtu | 50.0 kBtu/sq ft/yr |
| **Total Site** | **7,768 MMBtu** | **155.4 kBtu/sq ft/yr** |
| **Total Source** | **12,450 MMBtu** | **249.0 kBtu/sq ft/yr** |

## End Use Breakdown

| End Use | Electricity (kWh) | Natural Gas (MMBtu) | Total (MMBtu) |
|---------|-------------------|---------------------|---------------|
| Heating | 50,000 | 2,000 | 2,171 |
| Cooling | 450,000 | 0 | 1,535 |
| Interior Lighting | 350,000 | 0 | 1,195 |
| Interior Equipment | 200,000 | 0 | 682 |
| Fans | 150,000 | 0 | 512 |
| Pumps | 50,000 | 0 | 171 |
| **Total** | **1,250,000** | **2,500** | **7,768** |

## GHG Emissions

| Source | Annual Emissions (kg CO2e) | Emissions Intensity |
|--------|----------------------------|---------------------|
| Electricity | 525,000 | 10.5 kg/sq ft/yr |
| Natural Gas | 132,000 | 2.6 kg/sq ft/yr |
| **Total** | **657,000 kg (657 metric tons)** | **13.1 kg/sq ft/yr** |

**Carbon Factors Used:**
- Electricity: 0.42 kg CO2/kWh
- Natural Gas: 0.18 kg CO2/kWh

## Utility Costs

| Fuel | Annual Cost | Cost Intensity |
|------|-------------|----------------|
| Electricity | $125,000 | $2.50/sq ft/yr |
| Natural Gas | $25,000 | $0.50/sq ft/yr |
| **Total** | **$150,000** | **$3.00/sq ft/yr** |

## Unmet Hours

| Type | Hours |
|------|-------|
| Heating Setpoint Not Met | 45 |
| Cooling Setpoint Not Met | 23 |

## Peak Demand

| Type | Peak |
|------|------|
| Electric Demand | 450 kW |
| Heating Demand | 2,500 kBtu/hr |
| Cooling Demand | 350 tons |
```

#### CSV Output Example
```csv
Metric,Value,Units
Total Building Area,50000,sq ft
Total Site Energy,7768,MMBtu
Total Source Energy,12450,MMBtu
Site EUI,155.4,kBtu/sq ft/yr
Source EUI,249.0,kBtu/sq ft/yr
Electricity,1250000,kWh
Natural Gas,2500,MMBtu
Total GHG Emissions,657000,kg CO2e
GHG Intensity,13.1,kg CO2e/sq ft/yr
Total Utility Cost,150000,USD
Cost Intensity,3.00,USD/sq ft/yr
Heating Unmet Hours,45,hours
Cooling Unmet Hours,23,hours
```

#### JSON Output Example
```json
{
  "metadata": {
    "date": "2025-11-24",
    "model": "SECC_WSHP_ProposedModel_v3",
    "html_file": "output_fixed_v3/eplustbl.htm"
  },
  "building": {
    "total_area": {
      "value": 50000,
      "units": "sq ft"
    },
    "conditioned_area": {
      "value": 48500,
      "units": "sq ft"
    }
  },
  "eui": {
    "site": {
      "value": 155.4,
      "units": "kBtu/sq ft/yr"
    },
    "source": {
      "value": 249.0,
      "units": "kBtu/sq ft/yr"
    }
  },
  "energy": {
    "electricity": {
      "value": 1250000,
      "units": "kWh"
    },
    "natural_gas": {
      "value": 2500,
      "units": "MMBtu"
    }
  },
  "ghg": {
    "total": {
      "value": 657000,
      "units": "kg CO2e"
    },
    "intensity": {
      "value": 13.1,
      "units": "kg CO2e/sq ft/yr"
    }
  },
  "cost": {
    "total": {
      "value": 150000,
      "units": "USD"
    },
    "intensity": {
      "value": 3.00,
      "units": "USD/sq ft/yr"
    }
  }
}
```

#### Implementation Notes
- Use `beautifulsoup4` for HTML parsing
- Look for tables by caption text (e.g., "Annual Building Utility Performance Summary")
- Handle missing tables gracefully (some outputs may not be present)
- Unit conversion: 1 kWh = 3.412 kBtu, 1 MMBtu = 1000 kBtu
- For comparison mode, calculate: `delta = proposed - baseline`, `percent = (delta / baseline) * 100`

#### Dependencies
- `beautifulsoup4` - HTML parsing
- `pandas` - Table manipulation (optional, for Excel output)
- `openpyxl` - Excel file writing (optional, only if --format excel)
- Standard library (json, csv, argparse)

---

### **fix-node-connections.py**

**Priority:** HIGH (Phase 2)
**Status:** Not Started
**Estimated Effort:** 3 days

#### Purpose
Automatically repair broken HVAC node connections (missing nodes, mismatched inlet/outlet pairs).

#### Key Features
1. Build node connection graph
2. Identify missing nodes
3. Create missing nodes with proper naming
4. Fix inlet/outlet mismatches
5. Remove orphaned nodes (optional)

#### Command-Line Interface
```bash
# Fix node connections
python fix-node-connections.py model.idf --output fixed.idf

# Dry run to see what would be fixed
python fix-node-connections.py model.idf --dry-run --report node_issues.md

# Remove orphaned nodes
python fix-node-connections.py model.idf --remove-orphans --output cleaned.idf
```

#### Arguments
- `input_idf` - Input IDF file
- `output_idf` - Output IDF file
- `--dry-run` - Show issues without fixing
- `--report` - Output markdown report
- `--remove-orphans` - Remove unused node definitions
- `--create-missing` - Create missing NodeList objects (default: True)

#### Algorithm
```python
1. Load IDF with eppy
2. Build node inventory:
   a. Scan all objects for node fields (inlet, outlet, etc.)
   b. Create node connection graph:
      - nodes[name] = {'outlets': [], 'inlets': [], 'defined': False}
3. Scan NodeList objects:
   a. Mark nodes as 'defined' if in NodeList
4. Identify issues:
   a. Nodes used but not defined
   b. Nodes defined but never used (orphans)
   c. Inlet without matching outlet
   d. Outlet without matching inlet
5. Fix issues:
   a. Create NodeList entries for undefined nodes
   b. If --remove-orphans, remove unused NodeList entries
   c. For mismatches, attempt to infer correct connection
6. Save fixed IDF
7. Generate report
```

#### Output Format
```
================================================================================
FIX NODE CONNECTIONS
================================================================================

Input: model.idf
Output: fixed.idf

Building node connection graph...
  Found 245 node references
  Found 12 NodeList objects
  Found 180 defined nodes

Analyzing node connections...
  [ERROR] 15 nodes used but not defined
  [WARNING] 5 orphaned nodes (defined but unused)
  [INFO] 230 nodes properly connected

Fixing issues...
  [OK] Created NodeList entries for 15 missing nodes
  [OK] Removed 5 orphaned NodeList entries (--remove-orphans)

================================================================================
SUMMARY
================================================================================
  Total Nodes: 245
  Issues Fixed: 20
  Nodes Created: 15
  Orphans Removed: 5
  Output File: fixed.idf
================================================================================
```

#### Implementation Notes
- Node fields typically contain "Node" in field name
- Look for: Inlet Node, Outlet Node, Supply Node, Demand Node, etc.
- Use eppy's IDD info to identify node fields
- NodeList objects may have multiple nodes per object
- Some node fields are optional (may be blank)

#### Dependencies
- `eppy` - IDF manipulation
- Standard library only

---

### **fix-schedules.py**

**Priority:** HIGH (Phase 2)
**Status:** Not Started
**Estimated Effort:** 2 days

#### Purpose
Repair schedule references (create missing schedules, fix type limits, validate values).

#### Key Features
1. Identify objects referencing schedules
2. Check if schedule exists
3. Create default schedules if missing
4. Validate schedule type limits
5. Check schedule values in valid range

#### Command-Line Interface
```bash
# Fix schedule issues
python fix-schedules.py model.idf --output fixed.idf

# Create specific default schedule types
python fix-schedules.py model.idf --create-defaults on-off,fractional --output fixed.idf

# Dry run
python fix-schedules.py model.idf --dry-run --report schedule_issues.md
```

#### Arguments
- `input_idf` - Input IDF file
- `output_idf` - Output IDF file
- `--dry-run` - Show issues without fixing
- `--report` - Output markdown report
- `--create-defaults` - Comma-separated default schedule types to create
  - `on-off` - Always On (1.0) and Always Off (0.0)
  - `fractional` - Fraction schedules (0.0-1.0)
  - `temperature` - Temperature schedules
  - `occupancy` - Typical occupancy patterns

#### Default Schedules to Create

**Always On (Fraction):**
```
Schedule:Constant,
  Always On Discrete,    !- Name
  On/Off,                !- Schedule Type Limits Name
  1.0;                   !- Hourly Value
```

**Always Off (Fraction):**
```
Schedule:Constant,
  Always Off Discrete,   !- Name
  On/Off,                !- Schedule Type Limits Name
  0.0;                   !- Hourly Value
```

**Typical Occupancy:**
```
Schedule:Compact,
  Typical Occupancy,     !- Name
  Fraction,              !- Schedule Type Limits Name
  Through: 12/31,        !- Field 1
  For: Weekdays,         !- Field 2
  Until: 08:00, 0.0,     !- Field 3
  Until: 17:00, 1.0,     !- Field 5
  Until: 24:00, 0.0,     !- Field 7
  For: AllOtherDays,     !- Field 9
  Until: 24:00, 0.0;     !- Field 10
```

#### Algorithm
```python
1. Load IDF with eppy
2. Build schedule inventory:
   a. Get all Schedule:* objects
   b. Create map: schedule_name -> schedule_object
3. Build schedule type limits inventory
4. Scan all objects for schedule references:
   a. Look for fields with "Schedule" in name
   b. Check if referenced schedule exists
   c. Track missing schedules
5. For each missing schedule:
   a. Determine expected type from field name
   b. Create appropriate default schedule
6. Validate existing schedules:
   a. Check type limits exist
   b. Check values in valid range
7. Save fixed IDF
8. Generate report
```

#### Output Format
```
================================================================================
FIX SCHEDULES
================================================================================

Input: model.idf
Output: fixed.idf

Building schedule inventory...
  Found 45 Schedule objects
  Found 8 ScheduleTypeLimits objects

Scanning schedule references...
  Found 120 schedule references in 85 objects
  [ERROR] 12 missing schedule references
  [WARNING] 3 schedules with invalid type limits

Creating missing schedules...
  [OK] Created "Always On Discrete" (Fraction)
  [OK] Created "Always Off Discrete" (Fraction)
  [OK] Created "Typical Occupancy" (Fraction)
  [OK] Created 9 other default schedules

Fixing type limits...
  [OK] Created missing "On/Off" type limits
  [OK] Created missing "Fraction" type limits

================================================================================
SUMMARY
================================================================================
  Total Schedules: 57 (45 existing + 12 created)
  Missing References Fixed: 12
  Type Limits Created: 2
  Output File: fixed.idf
================================================================================
```

#### Implementation Notes
- Schedule references typically have "Schedule" in field name
- Common schedule types: Fraction, On/Off, Temperature, Activity Level
- ScheduleTypeLimits define valid range and unit type
- Some schedules are optional (blank is valid)

#### Dependencies
- `eppy` - IDF manipulation
- Standard library only

---

### **add-ideal-loads.py**

**Priority:** MEDIUM (Phase 3)
**Status:** Not Started
**Estimated Effort:** 1.5 days

#### Purpose
Replace complex HVAC systems with ideal loads air systems for envelope/load testing.

#### Key Features
1. Remove all HVAC equipment
2. Remove air loops, plant loops
3. Add ZoneHVAC:IdealLoadsAirSystem to each zone
4. Preserve zone definitions
5. Optionally preserve sizing objects

#### Command-Line Interface
```bash
# Replace HVAC with ideal loads
python add-ideal-loads.py proposed.idf --output baseline_ideal.idf

# Keep sizing objects
python add-ideal-loads.py proposed.idf --keep-sizing --output baseline.idf

# Configure ideal loads parameters
python add-ideal-loads.py proposed.idf --heating-limit 100000 --cooling-limit 100000 --output baseline.idf
```

#### Arguments
- `input_idf` - Input IDF file
- `output_idf` - Output IDF file
- `--keep-sizing` - Preserve Sizing:Zone and Sizing:System objects
- `--heating-limit` - Max heating capacity (W) [default: autosize]
- `--cooling-limit` - Max cooling capacity (W) [default: autosize]
- `--dehumidification-type` - Dehumidification control (None, ConstantSupplyHumidityRatio, Humidistat, ConstantSensibleHeatRatio)
- `--report` - Output markdown report

#### Algorithm
```python
1. Load IDF with eppy
2. Get list of all zones
3. Remove HVAC objects:
   a. Remove all AirLoopHVAC:* objects
   b. Remove all PlantLoop objects
   c. Remove all ZoneHVAC:* objects (except EquipmentList)
   d. Remove all Coil:* objects
   e. Remove all Fan:* objects
   f. Remove all Pump:* objects
   g. If not --keep-sizing, remove Sizing:* objects
4. For each zone:
   a. Create ZoneHVAC:IdealLoadsAirSystem
      - Name: "{zone_name} Ideal Loads"
      - Zone Name: {zone_name}
      - Heating Limit: {--heating-limit}
      - Cooling Limit: {--cooling-limit}
   b. Create/update ZoneHVAC:EquipmentList
      - Equipment 1: Ideal Loads Air System
      - Cooling/Heating Sequence: 1
5. Save modified IDF
6. Generate report
```

#### Output Format
```
================================================================================
ADD IDEAL LOADS AIR SYSTEMS
================================================================================

Input: proposed.idf
Output: baseline_ideal.idf

Removing existing HVAC systems...
  Removed 3 AirLoopHVAC objects
  Removed 2 PlantLoop objects
  Removed 24 ZoneHVAC objects
  Removed 15 Coil objects
  Removed 8 Fan objects
  Removed 4 Pump objects
  Preserved 12 Sizing:Zone objects (--keep-sizing)

Adding ideal loads air systems...
  [OK] Zone: Thermal Zone: Cardio 1
  [OK] Zone: Thermal Zone: Classrooms
  [... 10 more zones ...]

Created 12 ZoneHVAC:IdealLoadsAirSystem objects

================================================================================
SUMMARY
================================================================================
  Zones: 12
  HVAC Objects Removed: 56
  Ideal Loads Added: 12
  Output File: baseline_ideal.idf
================================================================================
```

#### Implementation Notes
- ZoneHVAC:IdealLoadsAirSystem is simple HVAC for load testing
- Each zone needs exactly one ideal loads system
- No ductwork, fans, or coils required
- Useful for testing envelope ECMs without HVAC complexity

#### Dependencies
- `eppy` - IDF manipulation
- Standard library only

---

### **apply-ecm-lighting.py**

**Priority:** MEDIUM (Phase 4)
**Status:** Not Started
**Estimated Effort:** 1 day

#### Purpose
Apply lighting power density (LPD) reduction ECM.

#### Key Features
1. Reduce LPD by percentage or to target W/sq ft
2. Apply to all zones or specific zones
3. Preserve schedules and other lighting properties

#### Command-Line Interface
```bash
# 20% LPD reduction
python apply-ecm-lighting.py baseline.idf --reduction 0.20 --output ecm_lighting.idf

# Target LPD
python apply-ecm-lighting.py baseline.idf --target-lpd 0.8 --output ecm_lighting.idf

# Specific zones only
python apply-ecm-lighting.py baseline.idf --reduction 0.20 --zones "Zone 1,Zone 2" --output ecm.idf
```

#### Arguments
- `input_idf` - Input IDF file
- `output_idf` - Output IDF file
- `--reduction` - Fractional reduction (0.0-1.0) e.g., 0.20 = 20% reduction
- `--target-lpd` - Target LPD (W/sq ft)
- `--zones` - Comma-separated zone names (default: all zones)
- `--report` - Output markdown report with before/after LPD

#### Algorithm
```python
1. Load IDF with eppy
2. Get all Lights objects
3. Get zone areas from Zone objects
4. For each Lights object:
   a. If --zones specified, skip if not in list
   b. Calculate current LPD = watts / zone_area
   c. If --reduction specified:
      new_watts = current_watts * (1 - reduction)
   d. If --target-lpd specified:
      new_watts = target_lpd * zone_area
   e. Update watts field
5. Save modified IDF
6. Generate report with before/after comparison
```

#### Output Format
```
================================================================================
APPLY ECM: LIGHTING POWER DENSITY REDUCTION
================================================================================

Input: baseline.idf
Output: ecm_lighting.idf
Reduction: 20%

Modifying lighting objects...
  Zone: Thermal Zone: Cardio 1
    Before: 2.5 W/sq ft (5,000 W)
    After:  2.0 W/sq ft (4,000 W)

  Zone: Thermal Zone: Classrooms
    Before: 1.2 W/sq ft (8,400 W)
    After:  0.96 W/sq ft (6,720 W)

  [... 10 more zones ...]

================================================================================
SUMMARY
================================================================================
  Zones Modified: 12
  Total Before: 85,000 W (1.7 W/sq ft average)
  Total After:  68,000 W (1.36 W/sq ft average)
  Reduction: 20% (17,000 W saved)
  Output File: ecm_lighting.idf
================================================================================
```

#### Implementation Notes
- Lights objects have Design Level (W) or Watts per Zone Floor Area
- Need to get zone area from Zone object
- Preserve all other fields (schedule, fraction radiant, etc.)
- Some Lights may use Watts/Person method (handle separately)

#### Dependencies
- `eppy` - IDF manipulation
- Standard library only

---

### **apply-ecm-envelope.py**

**Priority:** MEDIUM (Phase 4)
**Status:** Not Started
**Estimated Effort:** 2 days

#### Purpose
Modify envelope properties (insulation, windows) for ECM testing.

#### Key Features
1. Modify wall/roof R-values
2. Modify window U-factor and SHGC
3. Modify infiltration rates
4. Apply to all or specific surfaces/constructions

#### Command-Line Interface
```bash
# Increase wall insulation
python apply-ecm-envelope.py baseline.idf --wall-r-value 30 --output ecm_env1.idf

# Better windows
python apply-ecm-envelope.py baseline.idf --window-u 0.25 --window-shgc 0.25 --output ecm_env2.idf

# Reduce infiltration
python apply-ecm-envelope.py baseline.idf --infiltration-reduction 0.50 --output ecm_env3.idf

# Combined ECM
python apply-ecm-envelope.py baseline.idf --wall-r-value 30 --window-u 0.25 --infiltration-reduction 0.50 --output ecm_env_all.idf
```

#### Arguments
- `input_idf` - Input IDF file
- `output_idf` - Output IDF file
- `--wall-r-value` - Target wall R-value (hr·ft²·°F/Btu)
- `--roof-r-value` - Target roof R-value
- `--window-u` - Target window U-factor (Btu/hr·ft²·°F)
- `--window-shgc` - Target window SHGC (0.0-1.0)
- `--infiltration-reduction` - Fractional reduction in infiltration (0.0-1.0)
- `--constructions` - Comma-separated construction names to modify (default: all)
- `--report` - Output markdown report

#### Algorithm
```python
1. Load IDF with eppy
2. If --wall-r-value or --roof-r-value:
   a. Get all Construction objects for walls/roofs
   b. For each construction:
      - Get material layers
      - Calculate current R-value
      - Adjust insulation layer thickness to achieve target R
      - Update material thickness
3. If --window-u or --window-shgc:
   a. Get all WindowMaterial:SimpleGlazingSystem or WindowMaterial:Glazing
   b. Update U-Factor and/or SHGC fields
4. If --infiltration-reduction:
   a. Get all ZoneInfiltration:* objects
   b. Reduce flow rate by specified fraction
5. Save modified IDF
6. Generate report
```

#### Output Format
```
================================================================================
APPLY ECM: ENVELOPE IMPROVEMENTS
================================================================================

Input: baseline.idf
Output: ecm_env_all.idf

Wall R-Value Target: R-30
Window U-Factor Target: 0.25 Btu/hr·ft²·°F
Infiltration Reduction: 50%

Modifying wall constructions...
  Construction: Ext Wall Mass
    Before: R-15.2
    After:  R-30.0
    Insulation thickness: 2.5" -> 5.2"

Modifying window materials...
  Material: DblClrLowE
    Before: U=0.35, SHGC=0.45
    After:  U=0.25, SHGC=0.45

Modifying infiltration...
  Reduced 12 ZoneInfiltration objects by 50%
  Total ACH: 0.5 -> 0.25

================================================================================
SUMMARY
================================================================================
  Constructions Modified: 3
  Window Materials Modified: 2
  Infiltration Objects Modified: 12
  Output File: ecm_env_all.idf
================================================================================
```

#### Implementation Notes
- R-value calculation: R = sum(thickness / conductivity) for each layer
- Insulation typically in Material or Material:NoMass objects
- Windows may use SimpleGlazingSystem or detailed Glazing objects
- Infiltration in ZoneInfiltration:DesignFlowRate or ZoneInfiltration:EffectiveLeakageArea

#### Dependencies
- `eppy` - IDF manipulation
- Standard library only

---

### **extract-results.py** (continued - Comparison Mode)

#### Comparison Mode Output

When two HTML files provided (baseline vs proposed):

```markdown
# EnergyPlus Simulation Comparison

**Date:** 2025-11-24
**Baseline:** baseline/eplustbl.htm
**Proposed:** proposed/eplustbl.htm

## Energy Use Intensity Comparison

| Metric | Baseline | Proposed | Savings | % Reduction |
|--------|----------|----------|---------|-------------|
| Total Site EUI | 155.4 kBtu/sf/yr | 124.3 kBtu/sf/yr | 31.1 kBtu/sf/yr | 20.0% |
| Total Source EUI | 249.0 kBtu/sf/yr | 199.2 kBtu/sf/yr | 49.8 kBtu/sf/yr | 20.0% |

## Energy Savings by Fuel

| Fuel Type | Baseline | Proposed | Savings | % Reduction |
|-----------|----------|----------|---------|-------------|
| Electricity | 1,250,000 kWh | 1,000,000 kWh | 250,000 kWh | 20.0% |
| Natural Gas | 2,500 MMBtu | 2,000 MMBtu | 500 MMBtu | 20.0% |

## GHG Emissions Comparison

| Metric | Baseline | Proposed | Reduction | % Reduction |
|--------|----------|----------|-----------|-------------|
| Total Emissions | 657 metric tons | 526 metric tons | 131 metric tons | 20.0% |
| Emissions Intensity | 13.1 kg/sf/yr | 10.5 kg/sf/yr | 2.6 kg/sf/yr | 20.0% |

## Cost Comparison

| Metric | Baseline | Proposed | Savings | % Reduction |
|--------|----------|----------|---------|-------------|
| Total Annual Cost | $150,000 | $120,000 | $30,000 | 20.0% |
| Cost Intensity | $3.00/sf/yr | $2.40/sf/yr | $0.60/sf/yr | 20.0% |

## End Use Savings

| End Use | Baseline (MMBtu) | Proposed (MMBtu) | Savings (MMBtu) | % Reduction |
|---------|------------------|------------------|-----------------|-------------|
| Heating | 2,171 | 1,737 | 434 | 20.0% |
| Cooling | 1,535 | 1,228 | 307 | 20.0% |
| Interior Lighting | 1,195 | 956 | 239 | 20.0% |
| Interior Equipment | 682 | 682 | 0 | 0.0% |
| Fans | 512 | 410 | 102 | 20.0% |
| Pumps | 171 | 137 | 34 | 20.0% |
```

---

## Common Libraries & Imports Template

All scripts should use this template for consistency:

```python
#!/usr/bin/env python3
"""
Script Name: {script_name}.py
Purpose: {brief description}
Usage: python {script_name}.py [arguments]

Part of: EnergyPlus Assistant Toolkit
Philosophy: "Let tools handle syntax, let humans handle logic"
"""

import os
import sys
import argparse
from datetime import datetime
from eppy.modeleditor import IDF

# Optional imports (only if needed)
# from bs4 import BeautifulSoup  # For HTML parsing (extract-results.py)
# import pandas as pd            # For tabular data (extract-results.py with Excel)
# import yaml                    # For config files (run-parametric.py)
# import json                    # For JSON output

# Script metadata
SCRIPT_VERSION = "1.0.0"
SCRIPT_NAME = "{Script Name}"
SCRIPT_DESCRIPTION = "{One-line description}"

def find_idd():
    """Auto-detect Energy+.idd from common installation locations"""
    common_locations = [
        r'C:/EnergyPlusV25-1-0/Energy+.idd',
        r'C:/EnergyPlusV24-2-0/Energy+.idd',
        r'C:/EnergyPlusV23-2-0/Energy+.idd',
        r'/usr/local/EnergyPlus-25-1-0/Energy+.idd',
        r'/usr/local/EnergyPlus-24-2-0/Energy+.idd',
        r'/Applications/EnergyPlus-25-1-0/Energy+.idd',
        r'/Applications/EnergyPlus-24-2-0/Energy+.idd',
    ]

    for loc in common_locations:
        if os.path.exists(loc):
            return loc

    return None

def print_header(title):
    """Print formatted header"""
    print("=" * 80)
    print(title)
    print("=" * 80)

def print_summary(title, items):
    """Print formatted summary section"""
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)
    for key, value in items.items():
        print(f"  {key}: {value}")
    print("=" * 80)

def main():
    """Main script logic"""
    parser = argparse.ArgumentParser(
        description=SCRIPT_DESCRIPTION,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python {script_name}.py input.idf output.idf
  python {script_name}.py input.idf --option value --output output.idf
        """
    )

    # Common arguments
    parser.add_argument('input_idf', help='Input IDF file path')
    parser.add_argument('output_idf', nargs='?', help='Output IDF file path')
    parser.add_argument('--idd', help='Path to Energy+.idd (auto-detected if not provided)')
    parser.add_argument('--dry-run', action='store_true', help='Show changes without saving')
    parser.add_argument('--report', help='Output report file (markdown format)')
    parser.add_argument('--quiet', action='store_true', help='Suppress progress messages')
    parser.add_argument('--output', '-o', dest='output_idf', help='Output IDF file path')
    parser.add_argument('--version', action='version', version=f'{SCRIPT_NAME} {SCRIPT_VERSION}')

    # Script-specific arguments here
    # parser.add_argument('--option', help='Description')

    args = parser.parse_args()

    # Validate input file
    if not os.path.exists(args.input_idf):
        print(f"[ERROR] Input file not found: {args.input_idf}")
        sys.exit(3)

    # Validate output file (if not dry-run)
    if not args.dry_run:
        if not args.output_idf:
            print("[ERROR] Output file required (use --output or positional argument)")
            sys.exit(2)

        if args.output_idf == args.input_idf:
            print("[ERROR] Output file cannot be same as input file")
            sys.exit(2)

    # Auto-detect IDD
    idd_path = args.idd
    if not idd_path:
        if not args.quiet:
            print("\nAuto-detecting Energy+.idd...")
        idd_path = find_idd()
        if not idd_path:
            print("[ERROR] Could not find Energy+.idd. Please specify with --idd")
            sys.exit(3)
        if not args.quiet:
            print(f"  Found: {idd_path}")

    # Print header
    if not args.quiet:
        print_header(SCRIPT_NAME)
        print(f"\nInput: {args.input_idf}")
        if args.output_idf:
            print(f"Output: {args.output_idf}")
        if args.dry_run:
            print("Mode: DRY RUN (no changes will be saved)")

    # Load IDF
    try:
        IDF.setiddname(idd_path)
        idf = IDF(args.input_idf)
        if not args.quiet:
            print(f"\n[OK] Loaded IDF ({len(idf.idfobjects)} object types)")
    except Exception as e:
        print(f"[ERROR] Failed to load IDF: {e}")
        sys.exit(1)

    # ==========================================
    # MAIN SCRIPT LOGIC HERE
    # ==========================================

    results = {
        'input_file': args.input_idf,
        'output_file': args.output_idf,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        # ... other results
    }

    # ==========================================

    # Save modified IDF (unless dry-run)
    if not args.dry_run:
        try:
            idf.saveas(args.output_idf)
            if not args.quiet:
                print(f"\n[OK] Saved: {args.output_idf}")
        except Exception as e:
            print(f"[ERROR] Failed to save IDF: {e}")
            sys.exit(1)

    # Generate report if requested
    if args.report:
        try:
            generate_report(results, args.report)
            if not args.quiet:
                print(f"[OK] Report saved: {args.report}")
        except Exception as e:
            print(f"[ERROR] Failed to generate report: {e}")
            sys.exit(1)

    # Print summary
    if not args.quiet:
        print_summary("SUMMARY", {
            "Status": "Success",
            "Output File": args.output_idf if not args.dry_run else "N/A (dry run)",
            # ... other summary items
        })

    sys.exit(0)

def generate_report(results, output_path):
    """Generate markdown report"""
    with open(output_path, 'w') as f:
        f.write(f"# {SCRIPT_NAME} Report\n\n")
        f.write(f"**Date:** {results['timestamp']}\n\n")
        f.write(f"**Input:** {results['input_file']}\n\n")
        f.write(f"**Output:** {results['output_file']}\n\n")
        f.write("## Summary\n\n")
        # ... write summary
        f.write("\n## Details\n\n")
        # ... write details

if __name__ == '__main__':
    main()
```

---

## Testing Requirements

Each script must include:

1. **Unit Tests** (optional but recommended)
   - Test with sample IDF files
   - Test edge cases (empty file, missing objects, etc.)

2. **Example Files**
   - `examples/{script_name}/` directory
   - Include sample input.idf
   - Include expected output.idf
   - Include README.md with test cases

3. **Documentation**
   - Docstrings for all functions
   - Usage examples in --help
   - Section in main SKILL.md

---

## Quality Checklist

Before marking script as complete:

- [ ] Follows command-line interface standards
- [ ] Auto-detects IDD location
- [ ] Validates input file exists
- [ ] Never overwrites input file
- [ ] Provides --dry-run option
- [ ] Provides --report option
- [ ] Uses consistent output formatting ([OK], [ERROR], etc.)
- [ ] Handles errors gracefully with actionable messages
- [ ] Generates markdown reports
- [ ] Uses only necessary dependencies
- [ ] Includes docstrings
- [ ] Tested on Windows
- [ ] Added to SKILL.md documentation
- [ ] Added usage example to scripts/README.md

---

## Next Steps

1. **Immediate Priority:** Complete Phase 1 scripts
   - [ ] validate-idf-structure.py
   - [ ] add-standard-outputs.py
   - [ ] extract-results.py

2. **Update SKILL.md** after each script completion
   - Add to scripts list
   - Add usage example
   - Update decision tree if needed

3. **Create Examples** for each script
   - Sample input files
   - Expected outputs
   - Test cases

4. **Build Integration** - Consider wrapper script:
   - `energyplus-workflow.py` - Run multiple scripts in sequence
   - Config file driven (YAML)
   - Example: QA/QC → Fix issues → Add outputs → Run simulation → Extract results

---

## Long-term Vision

**Ultimate Goal:** Complete hands-off workflow

```bash
# Single command to go from broken IDF to deliverable results
python energyplus-workflow.py config.yaml

# config.yaml specifies:
# - Input IDF
# - Fixes to apply (nodes, schedules, equipment lists)
# - Outputs to add (LEED, comfort, HVAC)
# - ECMs to test (lighting, envelope, etc.)
# - Results to extract (EUI, GHG, cost)
# - Output format (markdown, Excel, JSON)
```

This toolkit will transform EnergyPlus modeling from **hours of manual editing** to **minutes of automated processing** while ensuring **syntactically correct** IDF files every time.

---

**End of Development Plan**
