# EnergyPlus Assistant Skill - Optimization Analysis

**Date:** 2025-11-24
**Session:** SECC in_cleaned.idf QA/QC
**Analyst:** skill-builder (via Claude Code)

---

## Executive Summary

The energyplus-assistant skill successfully completed the QA/QC task but encountered **10+ minutes of inefficiency** due to environment assumptions and lack of fallback strategies. This analysis identifies critical optimizations to make the skill more robust, faster, and environment-aware.

**Key Findings:**
- ❌ **MCP Server Accessibility**: Assumed MCP tools directly available (not true in VSCode)
- ❌ **No Fallback Strategy**: No alternative when MCP unavailable/slow
- ❌ **Windows Environment**: Path format issues not documented
- ✅ **Successful Workaround**: Python + eppy delivered fast results
- ✅ **Output Quality**: Generated excellent QA/QC report despite inefficiencies

---

## Critical Issues Identified

### 1. MCP Server Access Assumption (CRITICAL - P0)

**Problem:**
The skill assumes MCP tools are directly accessible as native functions, like:
```python
load_idf_model(idf_path="/workspace/models/...")
```

**Reality in VSCode Claude Code:**
- MCP tools are NOT exposed as direct function calls
- Must use Docker with complex stdio communication
- Requires proper JSON-RPC protocol
- Container startup time: 30+ seconds for dependency installation

**Impact:**
- 10+ minutes wasted on failed MCP access attempts
- Multiple Docker command pattern failures
- Path format troubleshooting (Windows paths vs container paths)

**Evidence from Session:**
```bash
# Failed Attempt 1: Tried to call MCP as bash command
mcp__energyplus-mcp_load_idf_model '{"idf_path": "..."}'
# Result: command not found

# Failed Attempt 2: Docker with wrong working directory
docker run ... --workdir /workspace/repo/energyplus-mcp-server
# Result: Git Bash path translation error

# Failed Attempt 3: Docker with correct paths but long startup
docker run ... uv run python -m energyplus_mcp_server.server
# Result: 30+ seconds installing dependencies, never completed
```

**Root Cause:**
Skill documentation doesn't acknowledge environment differences:
- Claude Desktop: MCP tools exposed natively
- VSCode: MCP requires Docker stdio protocol
- Cursor: MCP configuration different

---

### 2. No Fallback Strategy (CRITICAL - P0)

**Problem:**
Skill has no documented alternative when MCP is unavailable, slow, or fails.

**What Actually Worked:**
```python
# Improvised solution using Python + eppy
pip install eppy
python qaqc_analysis.py in_cleaned.idf
# Result: Complete analysis in < 5 seconds
```

**Recommendation:**
Skill should have tiered approach:

```
PRIORITY 1 (FASTEST): Direct IDF Parsing
├─ Python + eppy (installed: < 1 min, analysis: < 5 sec)
├─ Node.js + idf-parser (if exists)
└─ Direct text parsing for simple checks

PRIORITY 2 (IF NEEDED): MCP Server Tools
├─ Check if Docker running
├─ Check if MCP container exists
├─ Use for complex operations (HVAC topology, simulations)
└─ Fall back to Priority 1 if fails

PRIORITY 3 (SPECIAL CASES): Manual inspection
└─ Open in IDF Editor for visual review
```

**Why This Matters:**
- QA/QC is **pre-simulation** validation → should be FAST
- Most QA/QC checks (object counts, zone validation) don't need MCP
- MCP valuable for: HVAC topology, simulations, complex modifications
- Not valuable for: Counting objects, checking file structure

---

### 3. Windows Environment Not Considered (HIGH - P1)

**Problem:**
All examples use Unix-style paths with no Windows guidance.

**Issues Encountered:**
1. **Path Format Confusion:**
   ```
   C:\Users\... → Windows path (doesn't work in Docker)
   C:/Users/... → Docker Windows path (works)
   //workspace/... → Container path (but Git Bash translates!)
   /workspace/... → Correct container path
   ```

2. **Working Directory Flag:**
   ```bash
   # Failed in Git Bash due to path translation
   docker run -w /workspace/repo/...

   # Also failed
   docker run --workdir /workspace/repo/...

   # Needed double slashes
   docker run --workdir //workspace//repo//...
   ```

3. **No Docker Desktop Check:**
   - Tried Docker commands before checking if Docker Desktop running
   - Should check: `docker ps` works before proceeding

**Recommendation:**
Add OS-specific guidance:
```markdown
## Environment Setup

### Windows (VSCode)
1. Ensure Docker Desktop is running: `docker ps`
2. Path format for mounts: Use forward slashes `C:/Users/...`
3. Git Bash users: Use double slashes for workdir `//workspace//...`

### macOS/Linux (VSCode)
1. Ensure Docker daemon running: `docker ps`
2. Path format: Use native Unix paths

### All Platforms
- First attempt: Direct parsing (eppy/Node.js)
- If MCP needed: Validate Docker before attempting
```

---

### 4. Missing Decision Tree (HIGH - P1)

**Problem:**
Skill launches into MCP workflow without assessing what's actually needed.

**What Should Have Happened:**

```
User Request: "Run QA/QC on in_cleaned.idf"
    ↓
Question 1: What type of QA/QC is needed?
├─ Basic validation (object counts, zones, surfaces)
│   → Use: Direct parsing (Python/Node.js) - FAST
│
├─ HVAC topology analysis (loops, connections)
│   → Use: MCP tools (if available) OR text search patterns
│
├─ Simulation test (1-day run)
│   → Use: EnergyPlus directly OR MCP
│
└─ Full validation + simulation + results
    → Use: MCP server for comprehensive workflow

Question 2: Is MCP accessible?
├─ Yes (Docker running, container available)
│   → Proceed with MCP
│
└─ No (Docker not running, or slow startup)
    → Use fallback: Direct parsing
```

**Implementation:**
Add at top of SKILL.md:
```markdown
## Workflow Selection

BEFORE starting, determine the best approach:

1. **For QA/QC (object counts, validation):**
   - Use: Direct IDF parsing (Python + eppy)
   - Speed: < 5 seconds
   - Requirements: `pip install eppy`

2. **For HVAC topology (loop analysis):**
   - Use: MCP tools OR text pattern matching
   - Speed: 30+ seconds (MCP startup)
   - Requirements: Docker Desktop running

3. **For simulations (test runs):**
   - Use: Native EnergyPlus OR MCP
   - Speed: Minutes to hours
   - Requirements: EnergyPlus installed
```

---

### 5. Overly Detailed Tool List (MEDIUM - P2)

**Problem:**
Lists 35 MCP tools but:
- Doesn't validate they're accessible
- Doesn't prioritize which to use when
- Creates false expectation of availability

**Better Approach:**
```markdown
## Available Analysis Methods

### Method 1: Direct IDF Parsing (Recommended for QA/QC)
**Tools:** Python (eppy), Node.js (idf-parser)
**Best for:** Object counts, zone validation, surface checks
**Speed:** < 5 seconds
**Always available:** Yes (after package install)

### Method 2: MCP Server Tools (For Complex Operations)
**Tools:** 35 specialized tools via Docker
**Best for:** HVAC topology, simulations, modifications
**Speed:** 30+ seconds startup, then fast
**Availability:** Requires Docker Desktop

### Method 3: Native EnergyPlus (For Simulations)
**Tools:** energyplus CLI
**Best for:** Test runs, full simulations
**Speed:** Minutes to hours
**Availability:** If EnergyPlus installed locally
```

---

### 6. No Environment Detection (HIGH - P1)

**Problem:**
Skill doesn't check environment before attempting operations.

**Should Start With:**
```markdown
## Environment Check

Run these checks before proceeding:

1. **Operating System:**
   ```bash
   # Detect OS for path handling
   if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
     echo "Windows detected - use forward slashes for Docker paths"
   fi
   ```

2. **Docker Availability:**
   ```bash
   # Check if Docker is running
   docker ps > /dev/null 2>&1
   if [ $? -eq 0 ]; then
     echo "Docker available"
   else
     echo "Docker not available - use direct parsing"
   fi
   ```

3. **Python Availability:**
   ```bash
   python --version && pip list | grep eppy
   ```

4. **File Location:**
   ```bash
   # Verify IDF file exists before attempting analysis
   test -f "$IDF_PATH" && echo "File found" || echo "File not found"
   ```
```

---

## What Worked Well

### 1. Improvised Python Solution ✅
**Code Created:**
```python
# qaqc_analysis.py - Direct IDF parsing
# - Fast (< 5 seconds)
# - Simple (no Docker required)
# - Comprehensive (counts all major objects)
# - Reusable (saved for future use)
```

**Why It Worked:**
- No Docker dependencies
- No container startup delay
- Direct file access
- Simple text parsing sufficient for QA/QC

### 2. Comprehensive Report Generated ✅
**Output:**
- [QAQC_REPORT_in_cleaned_2025-11-24.md](../../../User-Files/work-tracking/secc-fort-collins/energy-model/QAQC_REPORT_in_cleaned_2025-11-24.md)
- Professional markdown format
- Actionable recommendations
- Clear status (MODEL READY)

### 3. Reusable Script Created ✅
**Artifact:**
- [qaqc_analysis.py](../../../User-Files/work-tracking/secc-fort-collins/energy-model/qaqc_analysis.py)
- Can be used for any IDF file
- No dependencies on MCP
- Fast execution

---

## Recommended Skill Optimizations

### Priority 0 (Critical - Implement Immediately)

#### 1. Add Environment Detection Section
**Location:** Top of SKILL.md, before workflows

```markdown
## Environment Assessment (ALWAYS RUN FIRST)

Before executing any workflow, run these checks:

### 1. Check Docker Status
```bash
docker ps > /dev/null 2>&1 && echo "Docker available" || echo "Docker unavailable - use direct parsing"
```

### 2. Check Python/Eppy
```bash
python -c "import eppy; print('eppy available')" 2>/dev/null || pip install eppy
```

### 3. Detect Operating System
- Windows: Use forward slashes for Docker mounts (`C:/Users/...`)
- Git Bash: Use double slashes for workdir (`//workspace//...`)
- macOS/Linux: Use native paths

### 4. Verify File Exists
```bash
test -f "$IDF_PATH" && echo "File found" || echo "File not found: $IDF_PATH"
```
```

#### 2. Add Decision Tree for Workflow Selection
**Location:** After environment assessment

```markdown
## Workflow Selection Matrix

| Task | Best Method | Speed | Requirements |
|------|-------------|-------|--------------|
| QA/QC object counts | Direct parsing (Python+eppy) | < 5 sec | pip install eppy |
| Zone validation | Direct parsing | < 5 sec | pip install eppy |
| Surface checks | Direct parsing | < 5 sec | pip install eppy |
| HVAC topology | MCP OR text patterns | 30+ sec | Docker (preferred) |
| Simulations | EnergyPlus CLI OR MCP | Minutes | EnergyPlus installed |
| Modifications | MCP (if available) | 30+ sec | Docker |

**Default Strategy:**
1. Start with direct parsing for QA/QC
2. Use MCP only when Docker confirmed available
3. Fall back gracefully if MCP fails
```

#### 3. Create Fallback Scripts Section
**Location:** New file `./direct-parsing-methods.md`

```markdown
# Direct IDF Parsing Methods (No MCP Required)

## Method 1: Python + eppy

### Installation
```bash
pip install eppy
```

### QA/QC Script
See `./scripts/qaqc-direct.py` for complete implementation.

### Usage
```bash
python qaqc-direct.py path/to/model.idf
```

### Output
- Object counts
- Zone validation
- Surface checks
- HVAC equipment summary
- Simulation settings verification

### Advantages
- Fast (< 5 seconds)
- No Docker required
- Works on all platforms
- Sufficient for 80% of QA/QC needs

## Method 2: Node.js + Text Parsing

### Installation
```bash
npm install -g idf-parser  # If available
```

### Usage
```javascript
import { readFile } from 'fs/promises';

const content = await readFile('model.idf', 'utf-8');
const objects = content.split(';').filter(o => o.trim());
// Count objects, validate structure
```

## Method 3: Bash + grep/awk (Quick Checks)

```bash
# Count zones
grep -c "^\\s*Zone," model.idf

# Count surfaces
grep -c "BuildingSurface:Detailed," model.idf

# Check for HVAC systems
grep -c "AirLoopHVAC," model.idf
```
```

---

### Priority 1 (High - Implement Soon)

#### 4. Restructure Workflows with Fallbacks

**Current:**
```markdown
### 1. Pre-Simulation QA/QC
1. Load model: `load_idf_model`
2. Validate syntax: `validate_idf`
3. Check simulation settings: `check_simulation_settings`
...
```

**Improved:**
```markdown
### 1. Pre-Simulation QA/QC

#### Quick Method (Recommended - 5 seconds)
```bash
# Install if needed
pip install eppy

# Run analysis
python ./scripts/qaqc-direct.py "$IDF_PATH"
```

#### Comprehensive Method (If Docker Available - 30+ seconds)
```bash
# Check Docker first
docker ps || { echo "Docker not running"; exit 1; }

# Use MCP tools
load_idf_model idf_path="/workspace/models/..."
validate_idf idf_path="/workspace/models/..."
...
```

#### Manual Method (Fallback)
```bash
# Open in IDF Editor for visual inspection
idf-editor "$IDF_PATH"
```
```

#### 5. Add Windows-Specific Guidance

**New Section:** `./windows-setup.md`

```markdown
# Windows Environment Setup

## Docker Path Formats

### Mount Points
Always use forward slashes:
```bash
# CORRECT
docker run -v C:/Users/mcoalson/Documents/WorkPath:/workspace ...

# WRONG
docker run -v C:\Users\mcoalson\Documents\WorkPath:/workspace ...
```

### Working Directory
In Git Bash, use double slashes:
```bash
# CORRECT (Git Bash)
docker run --workdir //workspace//repo//energyplus-mcp-server ...

# CORRECT (PowerShell)
docker run --workdir /workspace/repo/energyplus-mcp-server ...
```

## Docker Desktop Requirements

1. Ensure Docker Desktop is running
2. Check status: `docker ps`
3. If not running: Start Docker Desktop application

## Python Setup

```bash
# Windows often has both python and python3
python --version
python3 --version

# Use the one that's Python 3.10+
python -m pip install eppy
```

## Unicode Console Issues

If you see encoding errors, set:
```bash
# PowerShell
$env:PYTHONIOENCODING = "utf-8"

# Git Bash
export PYTHONIOENCODING=utf-8

# Or run with flag
python -X utf8 script.py
```
```

---

### Priority 2 (Medium - Nice to Have)

#### 6. Progressive Disclosure

**Current:** 337-line SKILL.md with everything inline

**Target:** < 200 lines in SKILL.md, details in supporting files

**Structure:**
```
energyplus-assistant/
├── SKILL.md (main instructions, < 200 lines)
├── direct-parsing-methods.md (Python/Node.js approaches)
├── mcp-server-usage.md (Docker/MCP when needed)
├── windows-setup.md (Windows-specific guidance)
├── hvac-topology-analysis.md (Complex HVAC workflows)
├── ecm-testing-workflows.md (ECM parametric studies)
└── scripts/
    ├── qaqc-direct.py (Direct IDF parsing)
    ├── qaqc-direct.js (Node.js version)
    └── check-environment.sh (Environment validation)
```

#### 7. Add Node.js Alternatives

Follow skill-builder best practice of preferring Node.js:

```javascript
#!/usr/bin/env node
// scripts/qaqc-direct.js

import { readFile } from 'fs/promises';

const analyzeIDF = async (idfPath) => {
  const content = await readFile(idfPath, 'utf-8');

  // Parse IDF objects
  const objects = content.split(';')
    .map(obj => obj.trim())
    .filter(obj => obj.length > 0);

  // Count object types
  const counts = {};
  objects.forEach(obj => {
    const match = obj.match(/^\\s*([\\w:]+),/);
    if (match) {
      const type = match[1];
      counts[type] = (counts[type] || 0) + 1;
    }
  });

  // Generate report
  console.log('EnergyPlus IDF QA/QC Report');
  console.log('='.repeat(80));
  console.log(`Total Objects: ${objects.length}`);
  console.log(`\\nObject Counts:`);

  Object.entries(counts)
    .sort(([,a], [,b]) => b - a)
    .forEach(([type, count]) => {
      console.log(`  ${type}: ${count}`);
    });
};

// Run
const idfPath = process.argv[2];
if (!idfPath) {
  console.error('Usage: node qaqc-direct.js <idf-path>');
  process.exit(1);
}

analyzeIDF(idfPath).catch(console.error);
```

---

## Revised Skill Structure

### Optimized SKILL.md (Target: < 200 lines)

```markdown
---
name: energyplus-assistant
description: Use this skill when analyzing EnergyPlus IDF building energy models, including QA/QC validation, HVAC topology analysis, ECM testing, or running simulations. Handles model inspection, validation, and basic analysis without requiring Docker/MCP for common tasks. (project)
---

# EnergyPlus Assistant

Specialized assistant for EnergyPlus building energy modeling workflows with intelligent method selection based on environment and task requirements.

## Core Capabilities

1. **Pre-Simulation QA/QC** - Fast validation using direct parsing
2. **HVAC System Analysis** - Topology discovery and visualization
3. **ECM Testing** - Parametric energy conservation measure evaluation

## Workflow Selection (ALWAYS START HERE)

### Environment Check
```bash
# 1. Check if Docker available
docker ps > /dev/null 2>&1 && echo "Docker: Available" || echo "Docker: Unavailable"

# 2. Check if Python/eppy available
python -c "import eppy" 2>/dev/null && echo "Direct parsing: Available" || pip install eppy

# 3. Verify IDF file exists
test -f "$IDF_PATH" && echo "File: Found" || echo "File: Not found"
```

### Task-Based Method Selection

| Your Task | Best Method | See Details |
|-----------|-------------|-------------|
| QA/QC validation | Direct parsing | ./direct-parsing-methods.md |
| Object counts | Direct parsing | ./direct-parsing-methods.md |
| HVAC topology | MCP (if Docker) OR text patterns | ./hvac-topology-analysis.md |
| Simulations | EnergyPlus CLI OR MCP | ./mcp-server-usage.md |
| ECM testing | MCP (preferred) OR scripts | ./ecm-testing-workflows.md |

## Priority Workflows

### 1. Pre-Simulation QA/QC (MOST COMMON)

**Quick Method (< 5 seconds):**
```bash
pip install eppy  # If not installed
python ./scripts/qaqc-direct.py "$IDF_PATH"
```

See [./direct-parsing-methods.md](./direct-parsing-methods.md) for complete implementation.

**When to use MCP instead:**
- Need detailed HVAC loop validation
- Want automated output variable discovery
- Require simulation test runs

See [./mcp-server-usage.md](./mcp-server-usage.md) for MCP workflows.

### 2. HVAC Topology Analysis

See [./hvac-topology-analysis.md](./hvac-topology-analysis.md)

### 3. ECM Testing

See [./ecm-testing-workflows.md](./ecm-testing-workflows.md)

## Windows Users

See [./windows-setup.md](./windows-setup.md) for:
- Docker path format guidance
- Unicode console setup
- Git Bash considerations

## Supporting Files

All scripts available in `./scripts/`:
- `qaqc-direct.py` - Fast Python QA/QC
- `qaqc-direct.js` - Node.js QA/QC alternative
- `check-environment.sh` - Environment validation

## Troubleshooting

**"Docker not available"** → Use direct parsing methods
**"MCP startup slow"** → Use direct parsing for QA/QC, MCP only for complex tasks
**"Unicode errors"** → See ./windows-setup.md for console encoding

---

*For SECC project context, see project-specific notes in User-Files/work-tracking/secc-fort-collins/*
```

---

## Implementation Checklist

- [ ] Create `./direct-parsing-methods.md` with Python+eppy approach
- [ ] Create `./scripts/qaqc-direct.py` (move from User-Files)
- [ ] Create `./scripts/qaqc-direct.js` (Node.js version)
- [ ] Create `./scripts/check-environment.sh` (environment validation)
- [ ] Create `./windows-setup.md` with Windows-specific guidance
- [ ] Create `./mcp-server-usage.md` (move existing MCP documentation)
- [ ] Create `./hvac-topology-analysis.md` (HVAC-specific workflows)
- [ ] Create `./ecm-testing-workflows.md` (ECM parametric studies)
- [ ] Rewrite SKILL.md to < 200 lines with decision trees
- [ ] Update description to mention "without requiring Docker/MCP for common tasks"
- [ ] Test on Windows with Docker unavailable
- [ ] Test on Windows with Docker available
- [ ] Validate all path formats work in Git Bash and PowerShell

---

## Key Takeaways

1. **Environment Awareness is Critical**
   - Always check Docker status before attempting MCP
   - Detect OS for path handling
   - Verify file existence before processing

2. **Fast Fallbacks Beat Slow Primary Methods**
   - Direct parsing (< 5 sec) > MCP startup (30+ sec) for QA/QC
   - Choose method based on task requirements, not tool preference

3. **Windows is a First-Class Citizen**
   - Document path format requirements
   - Handle Git Bash vs PowerShell differences
   - Account for console encoding issues

4. **Progressive Disclosure Improves Usability**
   - SKILL.md should be decision tree, not encyclopedia
   - Move details to intention-revealing supporting files
   - Keep main instructions actionable and brief

5. **Script Once, Reuse Forever**
   - qaqc-direct.py now available for all future projects
   - No Docker dependency for common tasks
   - Fast, reliable, portable

---

**Estimated Time Savings After Optimization:**
- Current: 10+ minutes (failed MCP attempts)
- Optimized: < 1 minute (direct parsing approach selected immediately)
- **Improvement: 10x faster** ✅

---

*Analysis generated 2025-11-24 during SECC QA/QC session review*
