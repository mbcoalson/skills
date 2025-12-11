# Building Component Library (BCL) & Measure Management

Guide to finding, downloading, and managing OpenStudio measures from the BCL and other sources.

## Building Component Library (BCL)

**URL**: https://bcl.nrel.gov/

The BCL is NREL's official repository of OpenStudio measures, components, and weather files.

### Browsing the BCL

**Categories**:
- **Envelope** - Construction, fenestration, infiltration measures
- **HVAC** - System replacement, equipment sizing, controls
- **Service Water Heating** - DHW system measures
- **Internal Gains** - Lighting, plug loads, occupancy
- **Whole Building** - Space types, standards, templates
- **Reporting** - Output variables, custom reports
- **Calibration** - Model calibration utilities

**Search Tips**:
- Use specific keywords: "thermostat", "boiler", "LED lighting"
- Filter by measure type: ModelMeasure, EnergyPlusMeasure, ReportingMeasure
- Check "Updated" date for recent measures
- Read "Description" and "Modeler Description" carefully

### Downloading Measures from BCL

**Manual Download**:
1. Find measure on https://bcl.nrel.gov/
2. Click "Download" button
3. Save `.tar.gz` or `.zip` file
4. Extract to project `measures/` directory

**Example**:
```bash
# Download measure from BCL (manual browser download)
# Save to: C:\Users\mcoalson\Downloads\set_thermostat_schedules.tar.gz

# Create measures directory if needed
mkdir measures

# Extract measure (using tar on Windows with Git Bash or WSL)
tar -xzf C:\Users\mcoalson\Downloads\set_thermostat_schedules.tar.gz -C measures\

# Or use 7-Zip on Windows
"C:\Program Files\7-Zip\7z.exe" x C:\Users\mcoalson\Downloads\set_thermostat_schedules.tar.gz -omeasures\

# Update measure metadata
C:\openstudio-3.10.0\bin\openstudio.exe measure --update measures\SetThermostatSchedules\
```

### BCL Measure Types

**1. ModelMeasure**
- Modifies OpenStudio model (.osm)
- Runs before EnergyPlus translation
- Examples: Add HVAC systems, change constructions, modify schedules

**2. EnergyPlusMeasure**
- Modifies EnergyPlus IDF file
- Runs after translation, before simulation
- Examples: Add output variables, modify simulation controls

**3. ReportingMeasure**
- Generates reports from simulation results
- Runs after simulation completes
- Examples: Custom result tables, energy breakdowns, charts

## Common Useful Measures

### HVAC Measures

**Replace HVAC System**:
- `Replace HVAC with DOAS` - Dedicated outdoor air system
- `Replace HVAC with VRF` - Variable refrigerant flow
- `Replace HVAC with Ground Source Heat Pumps` - GSHP system
- `Replace HVAC with Ideal Air Loads` - Remove HVAC for testing

**HVAC Controls**:
- `Add Thermostat Setpoint Schedules` - Set heating/cooling schedules
- `Enable Demand Control Ventilation` - CO2-based ventilation control
- `Add Night Cycle HVAC Operation` - After-hours HVAC control

**Equipment Efficiency**:
- `Improve Fan Efficiency` - Reduce fan power
- `Improve Cooling Coil COP` - Increase cooling efficiency
- `Improve Boiler Efficiency` - Increase heating efficiency

### Envelope Measures

**Insulation**:
- `Increase Insulation R-Value for Exterior Walls` - Add wall insulation
- `Increase Roof R-Value` - Add roof insulation
- `Improve Ground Slab Insulation` - Add slab edge insulation

**Fenestration**:
- `Replace Exterior Windows` - Change window U-value and SHGC
- `Reduce Window to Wall Ratio` - Decrease glazing area
- `Add Window Overhangs` - Add shading devices

**Air Tightness**:
- `Reduce Infiltration by Percentage` - Improve envelope airtightness

### Lighting & Equipment Measures

**Lighting**:
- `Reduce Lighting Loads by Percentage` - LPD reduction
- `Replace Lighting with LED` - LED retrofit
- `Add Daylighting Controls` - Photosensor controls

**Plug Loads**:
- `Reduce Electric Equipment Loads` - Plug load reduction
- `Add Advanced Power Strips` - Reduce phantom loads

### Schedule Measures

**Occupancy**:
- `Assign Typical Schedules from Standard` - Apply ASHRAE standard schedules
- `Modify Occupancy Schedules` - Adjust occupied hours
- `Create Typical Building Schedules` - Generate schedule set

**Setpoints**:
- `Set Thermostat Schedules` - Define heating/cooling setpoints
- `Add Night Setback/Setup` - Reduce energy during unoccupied periods
- `Optimize HVAC Schedule` - Align HVAC with occupancy

### Reporting Measures

**Energy Analysis**:
- `Add Monthly Output Table` - Monthly energy summary
- `Add Detailed HVAC Output` - System-level results
- `Create Baseline Comparison Report` - Compare to baseline

**Utility Bills**:
- `Add Utility Rate Calculations` - Calculate utility costs
- `Create Simple Payback Analysis` - Economics report

## NREL GitHub Measure Repositories

### OpenStudio Common Measures

**Repository**: https://github.com/NREL/openstudio-common-measures-gem

**Clone and use**:
```bash
# Clone repository
git clone https://github.com/NREL/openstudio-common-measures-gem.git

# Update all measures
C:\openstudio-3.10.0\bin\openstudio.exe measure --update_all openstudio-common-measures-gem\lib\measures\

# Reference in OSW
{
  "measure_paths": [
    "measures",
    "openstudio-common-measures-gem/lib/measures"
  ]
}
```

### OpenStudio Model Articulation

**Repository**: https://github.com/NREL/openstudio-model-articulation-gem

Measures for creating and modifying building models:
- Space type assignment
- Construction set application
- Whole building templates

**Clone and use**:
```bash
git clone https://github.com/NREL/openstudio-model-articulation-gem.git

C:\openstudio-3.10.0\bin\openstudio.exe measure --update_all openstudio-model-articulation-gem\lib\measures\
```

### OpenStudio EE Gem

**Repository**: https://github.com/NREL/openstudio-ee-gem

Energy efficiency measures for commercial buildings:
- High-performance HVAC
- Advanced envelope strategies
- Renewable energy integration

## Organizing Measures in Your Project

### Recommended Structure

```
project/
├── measures/
│   ├── local/                    # Project-specific custom measures
│   │   └── CustomMeasure/
│   ├── bcl/                      # Downloaded from BCL
│   │   ├── SetThermostatSchedules/
│   │   └── ReduceLightingLoads/
│   └── shared/                   # Shared across multiple projects
│       └── StandardReports/
└── workflows/
    └── workflow.osw
```

### OSW Measure Path Configuration

```json
{
  "measure_paths": [
    "measures/local",
    "measures/bcl",
    "measures/shared",
    "../company_measures"
  ],
  "steps": [
    {
      "measure_dir_name": "SetThermostatSchedules"
    }
  ]
}
```

## Inspecting Measure Details

### View Measure Information

**Measure metadata** (`measure.xml`):
```bash
# View measure.xml
type measures\SetThermostatSchedules\measure.xml
```

**Measure source code** (`measure.rb`):
```bash
# View measure.rb
type measures\SetThermostatSchedules\measure.rb
```

### Extract Measure Arguments

**Use `--compute_arguments`**:
```bash
C:\openstudio-3.10.0\bin\openstudio.exe measure --compute_arguments model.osm measures\SetThermostatSchedules\
```

**Parse with Node.js**:
```javascript
#!/usr/bin/env node
import { readFile } from 'fs/promises';
import { parseStringPromise } from 'xml2js';

// Read measure.xml
const xml = await readFile('measures/SetThermostatSchedules/measure.xml', 'utf-8');
const measure = await parseStringPromise(xml);

console.log('Measure:', measure.measure.name[0]);
console.log('Description:', measure.measure.description[0]);

measure.measure.arguments[0].argument.forEach(arg => {
  console.log(`\nArgument: ${arg.name[0]}`);
  console.log(`  Type: ${arg.type[0]}`);
  console.log(`  Required: ${arg.required[0]}`);
  if (arg.default_value) {
    console.log(`  Default: ${arg.default_value[0]}`);
  }
});
```

## Updating Measures

### When to Update

Update measures when:
- After downloading from BCL
- After modifying measure code
- After upgrading OpenStudio version
- When `measure.xml` is missing or outdated

### Update Commands

**Single measure**:
```bash
C:\openstudio-3.10.0\bin\openstudio.exe measure --update measures\SetThermostatSchedules\
```

**All measures in directory**:
```bash
C:\openstudio-3.10.0\bin\openstudio.exe measure --update_all measures\
```

**Update script** (Node.js):
```javascript
#!/usr/bin/env node
import { readdir } from 'fs/promises';
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

const measureDirs = await readdir('measures', { withFileTypes: true });

for (const dir of measureDirs) {
  if (dir.isDirectory()) {
    console.log(`Updating: ${dir.name}`);
    await execAsync(`C:\\openstudio-3.10.0\\bin\\openstudio.exe measure --update measures\\${dir.name}\\`);
  }
}

console.log('All measures updated!');
```

## Creating Custom Measures

When existing BCL measures don't meet your needs, **delegate to `writing-openstudio-model-measures` skill**.

**Indicators you need a custom measure**:
- Specific HVAC configuration not available in BCL
- Complex logic combining multiple modifications
- Project-specific calculation or reporting
- Iterative or parametric operations

**Hand off to measure writing skill with**:
- Desired functionality description
- Example model context
- Required arguments
- Expected outputs

## Measure Troubleshooting

### Issue: Measure Not Found

**Error**: `Measure 'SetThermostatSchedules' not found`

**Solutions**:
```bash
# Check measure exists
cmd /c "dir measures /b"

# Verify directory name matches OSW
# OSW has "measure_dir_name": "SetThermostatSchedules"
# Directory must be exactly: measures\SetThermostatSchedules\

# Update measure metadata
C:\openstudio-3.10.0\bin\openstudio.exe measure --update measures\SetThermostatSchedules\
```

### Issue: Argument Type Mismatch

**Error**: `Argument 'heating_setpoint' expected Double, got String`

**Solutions**:
```json
// WRONG - string value
{
  "arguments": {
    "heating_setpoint": "20"
  }
}

// CORRECT - numeric value
{
  "arguments": {
    "heating_setpoint": 20
  }
}
```

### Issue: Measure Fails to Run

**Check `out.osw` for errors**:
```bash
type out.osw | findstr "step_errors"
```

**Debug with Node.js**:
```javascript
#!/usr/bin/env node
import { readFile } from 'fs/promises';

const osw = JSON.parse(await readFile('out.osw', 'utf-8'));

osw.steps.forEach((step, i) => {
  if (step.result.step_errors.length > 0) {
    console.log(`\nStep ${i + 1}: ${step.measure_dir_name} FAILED`);
    step.result.step_errors.forEach(err => console.log(`  - ${err}`));
  }
});
```

## Best Practices

### Measure Selection

1. **Search BCL first** - Don't reinvent existing measures
2. **Check update date** - Prefer recently updated measures
3. **Read descriptions carefully** - Ensure measure matches your need
4. **Test incrementally** - Apply one measure at a time
5. **Verify compatibility** - Check OpenStudio version requirements

### Measure Organization

1. **Separate by source** - BCL vs. custom vs. shared
2. **Version control custom measures** - Track changes with Git
3. **Document measure purpose** - README in measure directories
4. **Keep measures updated** - Run `--update_all` regularly
5. **Share useful measures** - Contribute back to BCL

### Workflow Design

1. **Order matters** - Measures run sequentially
2. **Dependencies** - Some measures depend on others (e.g., HVAC sizing after envelope changes)
3. **Modularize** - One logical change per measure
4. **Parameterize** - Use arguments for flexibility
5. **Document workflow** - Comment OSW files with measure purpose

## Quick Reference Commands

```bash
# Search BCL (browser)
start https://bcl.nrel.gov/

# Download and install measure
tar -xzf measure.tar.gz -C measures\
C:\openstudio-3.10.0\bin\openstudio.exe measure --update measures\MeasureName\

# List available measures
cmd /c "dir measures /b"

# Inspect measure arguments
C:\openstudio-3.10.0\bin\openstudio.exe measure --compute_arguments model.osm measures\MeasureName\

# Update all measures
C:\openstudio-3.10.0\bin\openstudio.exe measure --update_all measures\

# Test measure without simulation
C:\openstudio-3.10.0\bin\openstudio.exe run --measures_only --workflow workflow.osw
```

## Additional Resources

- **BCL Website**: https://bcl.nrel.gov/
- **BCL API Documentation**: https://bcl.nrel.gov/api
- **Measure Writing Guide**: https://nrel.github.io/OpenStudio-user-documentation/reference/measure_writing_guide/
- **OpenStudio Measures GitHub**: https://github.com/NREL?q=openstudio+measures
- **Unmet Hours Measures**: https://unmethours.com/search?q=measures
