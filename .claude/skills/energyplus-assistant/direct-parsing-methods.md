# Direct IDF Parsing Methods

Fast QA/QC validation without Docker/MCP dependencies. Use these methods for:
- Pre-simulation validation
- Object counting and verification
- Basic structure checks
- Zone and surface validation

**Advantages:**
- Fast execution (< 5 seconds)
- No Docker required
- Works on all platforms
- Sufficient for 80% of QA/QC needs

---

## Method 1: Python + eppy (Recommended)

### Installation

```bash
pip install eppy
```

### Usage

The skill includes a complete QA/QC script at `./scripts/qaqc-direct.py`:

```bash
python ./scripts/qaqc-direct.py path/to/model.idf
```

### What It Checks

- **File structure**: Loads and validates IDF can be read
- **Core building objects**: Building, zones, surfaces, fenestration
- **Constructions & materials**: Verifies envelope definitions
- **Loads & schedules**: People, lights, equipment, infiltration
- **HVAC systems**: Air loops, plant loops, zone equipment
- **Simulation settings**: RunPeriod, SimulationControl
- **Outputs**: Output variables and meters

### Sample Output

```
================================================================================
ENERGYPLUS IDF QA/QC REPORT
================================================================================
Model: in_cleaned.idf
================================================================================

[1/8] Loading IDF file...
  File size: 1,143,113 characters
  [OK] File loaded successfully

[2/8] Analyzing object structure...
  Total objects: 1,561

[3/8] Object Count Summary:
  CORE BUILDING OBJECTS:
    [OK] Building                                      1
    [OK] Zone                                         24
    [OK] BuildingSurface:Detailed                    295
    [OK] FenestrationSurface:Detailed                 51
    ...

[OK] NO CRITICAL ISSUES FOUND
  STATUS: [OK] MODEL APPEARS READY FOR SIMULATION
```

### Script Details

The script performs text-based parsing:
- No IDD file required
- Counts object types by searching for patterns
- Validates presence of critical objects
- Generates actionable report

**When to use:**
- Pre-simulation QA/QC (every time)
- Quick model validation
- Object count verification
- Before committing model changes

**When NOT to use:**
- Need detailed HVAC connectivity analysis → Use MCP
- Want to discover available output variables → Use MCP
- Need to run simulations → Use EnergyPlus CLI or MCP

---

## Method 2: Node.js + Text Parsing

For users who prefer Node.js over Python.

### Installation

```bash
# No external packages required - uses Node.js built-ins
node --version  # Requires Node 18+
```

### Usage

```bash
node ./scripts/qaqc-direct.js path/to/model.idf
```

### Implementation

See `./scripts/qaqc-direct.js` for complete implementation. Key approach:

```javascript
import { readFile } from 'fs/promises';

const analyzeIDF = async (idfPath) => {
  // Read file
  const content = await readFile(idfPath, 'utf-8');

  // Parse objects (IDF uses semicolons as object delimiters)
  const objects = content.split(';')
    .map(obj => obj.trim())
    .filter(obj => obj.length > 0);

  // Count object types
  const counts = {};
  objects.forEach(obj => {
    const match = obj.match(/^\s*([\w:]+),/);
    if (match) {
      const type = match[1];
      counts[type] = (counts[type] || 0) + 1;
    }
  });

  // Generate report
  console.log(`Total Objects: ${objects.length}`);
  console.log('\nObject Counts:');
  Object.entries(counts)
    .sort(([,a], [,b]) => b - a)
    .forEach(([type, count]) => {
      console.log(`  ${type}: ${count}`);
    });
};
```

---

## Method 3: Bash + grep/awk (Quick Checks)

For rapid spot-checks without any dependencies.

### Count Specific Objects

```bash
# Count thermal zones
grep -c "^\s*Zone," model.idf

# Count building surfaces
grep -c "BuildingSurface:Detailed," model.idf

# Count windows
grep -c "FenestrationSurface:Detailed," model.idf

# Count HVAC air loops
grep -c "AirLoopHVAC," model.idf

# Count plant loops
grep -c "PlantLoop," model.idf
```

### Check for Specific Objects

```bash
# Check if RunPeriod exists
grep -q "RunPeriod," model.idf && echo "Has RunPeriod" || echo "No RunPeriod"

# Check if SimulationControl exists
grep -q "SimulationControl," model.idf && echo "Has SimulationControl" || echo "No SimulationControl"
```

### Extract Object Names

```bash
# List all zone names
grep "^\s*Zone," model.idf | sed 's/.*Zone,\s*//' | sed 's/,.*$//'

# List all air loop names
grep "^\s*AirLoopHVAC," model.idf | sed 's/.*AirLoopHVAC,\s*//' | sed 's/,.*$//'
```

---

## Comparison: When to Use Each Method

| Feature | Python+eppy | Node.js | Bash+grep |
|---------|-------------|---------|-----------|
| **Speed** | < 5 sec | < 3 sec | < 1 sec |
| **Setup** | pip install | None | None |
| **Completeness** | High | Medium | Low |
| **Portability** | Requires Python | Requires Node | Unix/Git Bash |
| **Best For** | Complete QA/QC | Simple QA/QC | Quick checks |

---

## Environment Setup

### Windows

**Python:**
```bash
# Check Python version (need 3.10+)
python --version

# Install eppy
pip install eppy

# If encoding errors occur
set PYTHONIOENCODING=utf-8
python ./scripts/qaqc-direct.py model.idf
```

**Node.js:**
```bash
# Check Node version (need 18+)
node --version

# Run script
node ./scripts/qaqc-direct.js model.idf
```

**Bash (Git Bash):**
```bash
# Most commands work in Git Bash
grep -c "Zone," model.idf
```

### macOS/Linux

**Python:**
```bash
python3 --version
pip3 install eppy
python3 ./scripts/qaqc-direct.py model.idf
```

**Node.js:**
```bash
node --version
node ./scripts/qaqc-direct.js model.idf
```

**Bash:**
```bash
# Native bash available
grep -c "Zone," model.idf
```

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'eppy'"

```bash
pip install eppy
# or
python -m pip install eppy
```

### "UnicodeEncodeError" (Windows)

```bash
# PowerShell
$env:PYTHONIOENCODING = "utf-8"
python script.py

# Git Bash
export PYTHONIOENCODING=utf-8
python script.py
```

### Node.js "Cannot find module"

```bash
# Ensure using ESM imports in package.json or .mjs extension
node ./scripts/qaqc-direct.mjs model.idf
```

---

## Next Steps After QA/QC

**If validation passes:**
1. Run 1-day test simulation (design day or Jan 1-2)
2. Review .err file for warnings
3. Run full annual simulation

**If issues found:**
- Missing objects → Add in IDF Editor or OpenStudio
- HVAC errors → Use MCP for topology analysis (see [./hvac-topology-analysis.md](./hvac-topology-analysis.md))
- Geometry errors → May need OpenStudio for surface fixing

**For detailed analysis:**
- HVAC topology → See [./mcp-server-usage.md](./mcp-server-usage.md)
- Simulation testing → Use EnergyPlus CLI directly
- ECM parametrics → See [./ecm-testing-workflows.md](./ecm-testing-workflows.md)

---

*Fast, reliable, no-Docker-required QA/QC validation*
