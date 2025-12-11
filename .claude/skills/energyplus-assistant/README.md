# EnergyPlus Assistant Skill

**Created:** 2025-11-23 (Sunday)
**Status:** Active Development - MCP Server Installation In Progress
**Purpose:** Workflow-focused EnergyPlus automation using LBNL's MCP server
**Replaces:** diagnosing-energy-models skill

---

## What Was Built Today

### 1. Skill Structure ✅
```
.claude/skills/energyplus-assistant/
├── SKILL.md                    # Main skill definition with 3 priority workflows
├── SETUP.md                    # Installation guide for MCP server
├── QUICK-START.md              # Quick reference for using the skill
├── README.md                   # This file - project overview
└── templates/
    ├── qa-qc-checklist.md      # Pre-simulation validation template
    ├── hvac-topology-report.md # HVAC analysis template
    └── ecm-comparison-report.md # ECM testing template
```

### 2. Integration with Work Command Center ✅
Updated `work-command-center` skill to invoke `energyplus-assistant` when:
- User mentions SECC energy model
- User requests energy model QA/QC
- User asks to validate EnergyPlus model
- User needs HVAC topology analysis
- User wants ECM testing

### 3. MCP Server Installation 🔄
- Downloaded LBNL EnergyPlus-MCP repository
- Docker build in progress (Step 2/6)
- Will provide 35 EnergyPlus tools when complete

---

## Core Workflows (Priority Order)

### 1. Pre-Simulation QA/QC (Highest Priority)
**Purpose:** Catch errors before investing time in simulations

**What it checks:**
- IDF syntax and structure
- Simulation settings (run period, timestep, etc.)
- Zones, surfaces, materials defined
- Schedules referenced correctly
- HVAC systems connected properly
- Output variables configured

**Template:** `templates/qa-qc-checklist.md`

---

### 2. HVAC System Understanding (High Priority)
**Purpose:** Understand HVAC topology before modifications

**What you get:**
- All HVAC loops (plant, condenser, air)
- Equipment on each loop
- Visual topology diagrams
- Control sequences

**Template:** `templates/hvac-topology-report.md`

**Key for SECC:** Understand condenser loop + WSHP systems before rebuild

---

### 3. Rapid Parametric ECM Testing (Medium Priority)
**Purpose:** Test multiple energy conservation measures quickly

**What it does:**
- Baseline simulation
- Modify equipment (lights, plugs, infiltration, etc.)
- Run ECM scenarios
- Compare energy/cost/GHG savings

**Template:** `templates/ecm-comparison-report.md`

---

## Available MCP Tools (35 Total)

### Model Loading & Validation (9 tools)
- `load_idf_model` - Load IDF file
- `validate_idf` - Check syntax
- `get_model_summary` - High-level overview
- `check_simulation_settings` - Review settings
- `modify_simulation_control` - Update settings
- `modify_run_period` - Change run period
- `get_server_configuration` - View config
- `list_available_files` - List samples
- `copy_file` - File management

### Model Inspection (9 tools)
- `list_zones` - All thermal zones
- `get_surfaces` - Surface info
- `get_materials` - Materials
- `inspect_schedules` - Schedules
- `inspect_people` - Occupancy
- `inspect_lights` - Lighting
- `inspect_electric_equipment` - Plug loads
- `get_output_variables` - Available outputs
- `get_output_meters` - Available meters

### Model Modification (8 tools)
- `modify_lights` - Adjust lighting
- `modify_electric_equipment` - Change plug loads
- `modify_people` - Update occupancy
- `change_infiltration_by_mult` - Scale infiltration
- `add_window_film_outside` - Window films
- `add_coating_outside` - Surface coatings
- `add_output_variables` - Request outputs
- `add_output_meters` - Request meters

### HVAC Analysis (4 tools)
- `discover_hvac_loops` - Find all loops
- `get_loop_topology` - Loop details
- `visualize_loop_diagram` - Create diagrams
- `run_energyplus_simulation` - Execute simulation

### Visualization & Results (1 tool)
- `create_interactive_plot` - Interactive charts

### Server Management (4 tools)
- `get_server_status` - Health check
- `get_error_logs` - View errors
- `get_server_logs` - View logs
- `clear_logs` - Clear logs

---

## SECC Project Context

**Model:** `C:\Users\mcoalson\Documents\WorkPath\User-Files\work-tracking\secc-fort-collins\energy-model\SECC_WSHP_ProposedModel_v3_WaterLoop_RTUHP_DOAS_Pool\run\in.idf`

**Deadline:** Nov 27, 2025 (Pre-Thanksgiving) - 4 days away

**Deliverables:**
- EUI (Energy Use Intensity)
- GHG (Greenhouse Gas Emissions)
- Utility Cost

**Planned HVAC Rebuild:**
- Condenser loop
- 4-5 major WSHP air systems
- DOAS for ventilation
- Pool heating system

**How This Skill Helps:**
1. **Before rebuild:** QA/QC v3 model, understand existing HVAC
2. **During rebuild:** Validate new HVAC topology
3. **After rebuild:** Run simulation and extract EUI/GHG/Cost

---

## Next Steps to Complete Installation

### Step 1: Wait for Docker Build ⏳
Currently running (Step 2/6 - installing system packages)
Expected completion: 5-10 minutes total

### Step 2: Configure VS Code MCP Settings
Add to `.vscode/settings.json`:
```json
{
  "mcp.servers": {
    "energyplus": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "--mount", "type=bind,source=C:\\Users\\mcoalson\\Documents\\WorkPath\\User-Files\\work-tracking\\secc-fort-collins\\energy-model,target=/workspace/models",
        "--mount", "type=bind,source=C:\\Users\\mcoalson\\Documents\\WorkPath\\EnergyPlus-MCP-main\\energyplus-mcp-server\\sample_files,target=/workspace/sample_files",
        "energyplus-mcp-dev"
      ]
    }
  }
}
```

### Step 3: Reload VS Code
`Ctrl+Shift+P` → "Developer: Reload Window"

### Step 4: Test MCP Server
In Claude Code:
```
Can you list the available MCP tools for EnergyPlus?
```

### Step 5: Test with SECC Model
```
Validate my SECC energy model using the energyplus-assistant skill
```

---

## Design Philosophy

**Why Workflow-Focused?**
- Gets immediate value for SECC deadline (Nov 27)
- Reusable for future projects
- Complements existing skills (energy-efficiency, writing-openstudio-model-measures)

**Why Replace diagnosing-energy-models?**
- MCP server provides programmatic access to EnergyPlus
- More reliable than screen scraping or file parsing
- Supports advanced workflows (ECM testing, HVAC visualization)
- Better integration with AI workflows

**Integration Strategy:**
- Standalone skill for direct invocation
- Called by work-command-center for coordinated workflows
- Complements (not duplicates) other energy modeling skills

---

## Future Enhancements

Potential additions after initial deployment:
- ASHRAE 90.1 baseline auto-generation
- LEED compliance checking
- Custom ECM libraries
- Integration with OpenStudio Measure workflow
- Automated report generation (Word/PDF)
- Cost database for NPV calculations
- Integration with converting-markdown-to-word skill

---

## Technology Stack

- **MCP Server:** LBNL EnergyPlus-MCP v0.1.0
- **EnergyPlus:** 25.1.0 (included in Docker container)
- **Docker:** 28.3.2 (for containerized deployment)
- **Python:** 3.12 (MCP server runtime)
- **Claude Code:** VS Code extension for AI integration

---

## Credits

- **MCP Server:** LBNL-ETA (Lawrence Berkeley National Lab)
- **GitHub:** https://github.com/LBNL-ETA/EnergyPlus-MCP
- **Research Paper:** SoftwareX (2025), DOI: 10.1016/j.softx.2025.102367
- **Skill Design:** Matt Coalson + Claude (2025-11-23)

---

## Documentation Files

- **SKILL.md** - Main skill instructions for Claude
- **SETUP.md** - Installation guide
- **QUICK-START.md** - Quick reference guide
- **README.md** - This overview (for you)
- **templates/** - Report templates for outputs

---

**Last Updated:** 2025-11-23
**Version:** 1.0
**Status:** Active Development - MCP Server Build In Progress
