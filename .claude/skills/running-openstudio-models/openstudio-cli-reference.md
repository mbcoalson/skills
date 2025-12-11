# OpenStudio CLI Detailed Reference

Complete command reference and examples for OpenStudio 3.10 CLI operations.

## Installation & Setup

**OpenStudio Location**: `C:\openstudio-3.10.0\bin\openstudio.exe`

**Add to PATH** (optional, for convenience):
```bash
# Add to Windows PATH environment variable
setx PATH "%PATH%;C:\openstudio-3.10.0\bin"
```

**Verify Installation**:
```bash
C:\openstudio-3.10.0\bin\openstudio.exe --version
```

## Command Structure

```
openstudio.exe [switches] <subcommand> [subcommand-options]
```

**Program-Level Switches** (before subcommand):
- `--verbose` - Output debugging information
- `--gem_path /path/` - Load custom Ruby gems
- `--include /path/` - Add directories to Ruby load path

## Core Subcommands

### 1. `run` - Execute Workflows

**Basic simulation**:
```bash
openstudio.exe run --workflow workflow.osw
```

**Measures only** (no simulation):
```bash
openstudio.exe run --measures_only --workflow workflow.osw
```

**Regenerate reports** (from existing results):
```bash
openstudio.exe run --postprocess_only --workflow workflow.osw
```

**Debug mode** (preserve directories, verbose output):
```bash
openstudio.exe --verbose run --debug --workflow workflow.osw
```

**Options**:
- `-w, --workflow PATH` - Path to OSW file (required)
- `-m, --measures_only` - Run measures without simulation
- `-p, --postprocess_only` - Regenerate reports only
- `--debug` - Preserve run directory and add debugging output

### 2. `measure` - Measure Management

**Update single measure**:
```bash
openstudio.exe measure --update /path/to/measure/
```

**Update all measures in directory**:
```bash
openstudio.exe measure --update_all /path/to/measures/
```

**Compute measure arguments for model**:
```bash
openstudio.exe measure --compute_arguments model.osm /path/to/measure/
```

**Options**:
- `-u, --update PATH` - Update measure metadata
- `-t, --update_all PATH` - Update all measures in directory
- `-a, --compute_arguments OSM MEASURE` - Generate arguments for specific model

### 3. `help` - Documentation

**General help**:
```bash
openstudio.exe -h
openstudio.exe --help
```

**Subcommand help**:
```bash
openstudio.exe run -h
openstudio.exe measure -h
```

## OpenStudio Workflow (OSW) File Format

### Minimal OSW

```json
{
  "seed_file": "baseline.osm",
  "weather_file": "weather.epw"
}
```

### Complete OSW Example

```json
{
  "seed_file": "SECC_2025-12-03_v1.osm",
  "weather_file": "USA_CO_Fort_Collins.epw",
  "measure_paths": [
    "measures",
    "../shared_measures"
  ],
  "file_paths": [
    "weather",
    "../shared_weather"
  ],
  "run_directory": "./run",
  "steps": [
    {
      "measure_dir_name": "AddOutputVariable",
      "arguments": {
        "variable_name": "Zone Mean Air Temperature",
        "reporting_frequency": "Hourly"
      }
    },
    {
      "measure_dir_name": "SetThermostatSchedules",
      "arguments": {
        "heating_setpoint": 20,
        "cooling_setpoint": 24
      }
    }
  ]
}
```

### OSW Fields Reference

**Required**:
- `seed_file` - Path to OpenStudio model (.osm)
- `weather_file` - Path to EnergyPlus weather file (.epw)

**Optional**:
- `measure_paths` - Array of directories to search for measures
- `file_paths` - Array of directories to search for seed/weather files
- `run_directory` - Output directory (default: `./run`)
- `steps` - Array of measures to apply sequentially

**Step Object**:
- `measure_dir_name` - Directory name containing measure
- `arguments` - Key-value pairs for measure inputs

## Output Files

After running `openstudio.exe run --workflow workflow.osw`:

### `out.osw` - Workflow Output

JSON file documenting execution results:

```json
{
  "completed_status": "Success",
  "started_at": "2025-12-03T10:30:00Z",
  "completed_at": "2025-12-03T10:35:00Z",
  "steps": [
    {
      "measure_dir_name": "AddOutputVariable",
      "result": {
        "step_result": "Success",
        "step_errors": [],
        "step_warnings": []
      }
    }
  ]
}
```

**Key Fields**:
- `completed_status` - Overall status: `"Success"`, `"Fail"`, `"Cancel"`
- `steps[].result.step_result` - Per-measure status
- `steps[].result.step_errors` - Error messages from measures

### `run/` Directory Contents

**EnergyPlus Files**:
- `eplusout.err` - Error and warning log
- `eplusout.sql` - Simulation results database
- `eplusout.htm` - HTML summary report
- `in.idf` - Translated EnergyPlus input file
- `in.osm` - OpenStudio model after measures applied

**Analysis Files**:
- `pre-preprocess.log` - Measure execution log
- `eplustbl.htm` - EnergyPlus tabular results

## Working with Measures

### Finding Measures

**Building Component Library (BCL)**:
- URL: https://bcl.nrel.gov/
- Search by category: HVAC, Envelope, Schedules, etc.
- Download as `.tar.gz` or `.zip`

**NREL GitHub Repositories**:
- https://github.com/NREL/openstudio-common-measures-gem
- https://github.com/NREL/openstudio-model-articulation-gem

### Measure Directory Structure

```
measures/
└── SetThermostatSchedules/
    ├── measure.rb          # Main measure code
    ├── measure.xml         # Metadata (auto-generated)
    └── tests/
        └── measure_test.rb
```

### Installing Measures

**From BCL Download**:
```bash
# Extract downloaded measure
tar -xzf measure_name.tar.gz -C measures/

# Update metadata
openstudio.exe measure --update measures/SetThermostatSchedules/
```

**From Git Repository**:
```bash
# Clone measure repository
git clone https://github.com/NREL/openstudio-common-measures-gem.git

# Update all measures
openstudio.exe measure --update_all openstudio-common-measures-gem/lib/measures/
```

### Inspecting Measure Arguments

**See available arguments**:
```bash
openstudio.exe measure --compute_arguments model.osm measures/SetThermostatSchedules/
```

**Output**:
```json
{
  "arguments": [
    {
      "name": "heating_setpoint",
      "display_name": "Heating Setpoint",
      "type": "Double",
      "required": true,
      "default_value": 20.0
    },
    {
      "name": "cooling_setpoint",
      "display_name": "Cooling Setpoint",
      "type": "Double",
      "required": true,
      "default_value": 24.0
    }
  ]
}
```

## Error Handling & Debugging

### Checking Simulation Success

**Quick validation**:
```bash
# Check out.osw status
type out.osw | findstr "completed_status"

# Count severe errors in EnergyPlus output
type run\eplusout.err | findstr /C:"** Severe **" | find /c /v ""
```

**Parse out.osw with Node.js**:
```javascript
#!/usr/bin/env node
import { readFile } from 'fs/promises';

const osw = JSON.parse(await readFile('out.osw', 'utf-8'));

console.log(`Status: ${osw.completed_status}`);

osw.steps.forEach((step, i) => {
  console.log(`\nStep ${i + 1}: ${step.measure_dir_name}`);
  console.log(`  Result: ${step.result.step_result}`);

  if (step.result.step_errors.length > 0) {
    console.log(`  Errors:`);
    step.result.step_errors.forEach(err => console.log(`    - ${err}`));
  }
});
```

### Common Error Patterns

**1. Measure Not Found**

Error in `out.osw`:
```json
{
  "step_errors": ["Measure 'AddOutputVariable' not found"]
}
```

**Fix**:
- Verify measure exists in `measures/` or specified `measure_paths`
- Check `measure_dir_name` spelling matches directory name
- Run `openstudio.exe measure --update measures/AddOutputVariable/`

**2. Missing Required Argument**

Error in `out.osw`:
```json
{
  "step_errors": ["Required argument 'variable_name' not provided"]
}
```

**Fix**:
- Add missing argument to OSW step
- Run `--compute_arguments` to see required arguments

**3. Weather File Not Found**

Error: `Weather file not found at path: weather.epw`

**Fix**:
- Verify `.epw` file exists
- Check `weather_file` path in OSW (relative to OSW location)
- Add `file_paths` to OSW to specify search directories

**4. Model Translation Failure**

Error: `Failed to translate OpenStudio Model to EnergyPlus IDF`

**Delegate to**: `diagnosing-energy-models` skill
- Likely geometry or orphaned object issues
- Check `pre-preprocess.log` for translation errors

### Verbose Debugging

**Maximum debug output**:
```bash
openstudio.exe --verbose run --debug --workflow workflow.osw > debug.log 2>&1
```

**Preserve run directory**:
```bash
# --debug prevents cleanup of intermediate files
openstudio.exe run --debug --workflow workflow.osw
```

## Advanced Workflows

### Parametric Runs

Use Node.js to generate multiple OSW files with varying parameters:

```javascript
#!/usr/bin/env node
import { writeFile } from 'fs/promises';
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

const baseWorkflow = {
  seed_file: "baseline.osm",
  weather_file: "weather.epw",
  steps: []
};

// Parametric sweep: heating setpoints from 18-22°C
for (let temp = 18; temp <= 22; temp += 1) {
  const workflow = {
    ...baseWorkflow,
    run_directory: `./runs/heating_${temp}C`,
    steps: [
      {
        measure_dir_name: "SetThermostatSchedules",
        arguments: {
          heating_setpoint: temp,
          cooling_setpoint: 24
        }
      }
    ]
  };

  const filename = `workflow_heating_${temp}.osw`;
  await writeFile(filename, JSON.stringify(workflow, null, 2));

  console.log(`Running: ${filename}`);
  await execAsync(`C:\\openstudio-3.10.0\\bin\\openstudio.exe run --workflow ${filename}`);
}

console.log("Parametric runs complete!");
```

### Measure-Only Workflow

Apply measures without running simulation (faster for model modifications):

```bash
# Apply measures and save modified model
openstudio.exe run --measures_only --workflow workflow.osw

# Modified model saved in run/in.osm
cp run/in.osm modified_model.osm
```

### Custom Measure Paths

Search multiple directories for measures:

```json
{
  "seed_file": "model.osm",
  "weather_file": "weather.epw",
  "measure_paths": [
    "measures",
    "C:/shared_measures",
    "../project_measures"
  ],
  "steps": [
    {
      "measure_dir_name": "CustomMeasure"
    }
  ]
}
```

## Environment Variables

**ENERGYPLUS_DIR**: Override EnergyPlus installation location
```bash
set ENERGYPLUS_DIR=C:\EnergyPlusV25-1-0
openstudio.exe run --workflow workflow.osw
```

**OS_RUNNER_KEEP_RUN_DIR**: Preserve run directory (alternative to `--debug`)
```bash
set OS_RUNNER_KEEP_RUN_DIR=1
openstudio.exe run --workflow workflow.osw
```

## Best Practices

### File Organization

```
project/
├── models/
│   ├── baseline.osm
│   ├── SECC_2025-12-03_v1.osm
│   └── SECC_2025-12-03_v2.osm
├── measures/
│   ├── SetThermostatSchedules/
│   └── AddOutputVariable/
├── weather/
│   └── USA_CO_Fort_Collins.epw
├── workflows/
│   ├── baseline_workflow.osw
│   └── parametric_workflow.osw
└── results/
    ├── run_v1/
    └── run_v2/
```

### Workflow Tips

1. **Always version models**: Use `projectname_YYYY-MM-DD_vX.osm` format
2. **Keep weather files organized**: Separate `weather/` directory
3. **Modularize measures**: One measure per logical modification
4. **Test incrementally**: Apply measures one at a time, validate each
5. **Preserve successful runs**: Save `run/` directory with meaningful names

### Path Handling

- **OSW paths**: Always use forward slashes, even on Windows
- **Relative paths**: Resolved relative to OSW file location
- **No whitespace**: Avoid spaces in filenames and directory names
- **Use `file_paths`**: Specify search directories for portability

### Performance Optimization

- **Use `--measures_only`**: Skip simulation when only modifying model
- **Use `--postprocess_only`**: Regenerate reports without re-simulating
- **Parallel runs**: Run multiple OSW files simultaneously (separate directories)

## Troubleshooting Quick Reference

| Symptom | Likely Cause | Solution |
|---------|--------------|----------|
| "Measure not found" | Incorrect `measure_dir_name` | Verify directory name, run `--update` |
| "Weather file not found" | Incorrect path | Check `.epw` location, update OSW path |
| "Required argument missing" | Missing argument in OSW | Run `--compute_arguments` to see requirements |
| Simulation fails immediately | Syntax error in OSW | Validate JSON syntax |
| Translation failure | Geometry issues | Delegate to `diagnosing-energy-models` |
| Severe EnergyPlus errors | HVAC/zone configuration | Delegate to `diagnosing-energy-models` |

## Additional Resources

- **OpenStudio SDK Documentation**: https://nrel.github.io/OpenStudio-user-documentation/
- **Measure Writing Guide**: https://nrel.github.io/OpenStudio-user-documentation/reference/measure_writing_guide/
- **EnergyPlus Documentation**: https://energyplus.net/documentation
- **Unmet Hours Forum**: https://unmethours.com/
- **OpenStudio Coalition**: https://openstudiocoalition.org/
