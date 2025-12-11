# EnergyPlus Assistant - Quick Start Guide

**Status:** Skill created, MCP server installation in progress
**Created:** 2025-11-23

---

## What is This?

The **energyplus-assistant** skill gives you AI-powered access to 35 EnergyPlus tools for:
1. **Pre-Simulation QA/QC** - Validate models before running
2. **HVAC Topology Analysis** - Understand system configurations
3. **Parametric ECM Testing** - Test energy conservation measures

## How to Use

### From Work Command Center

```
User: Validate my SECC energy model before simulation
```

Work Command Center will automatically invoke energyplus-assistant and run the QA/QC workflow.

### Direct Skill Invocation

```
/energyplus-assistant
```

Then describe what you need:
- "Run QA/QC on my SECC model"
- "Analyze HVAC topology"
- "Test lighting reduction ECM scenarios"

---

## Common Workflows

### 1. Pre-Simulation QA/QC

**When:** Before every simulation run

**What it checks:**
- IDF syntax valid
- Simulation settings correct
- All zones/surfaces/materials defined
- Schedules referenced correctly
- Output variables configured
- HVAC systems properly connected

**Output:** QA/QC checklist report with critical issues, warnings, and recommended actions

---

### 2. HVAC System Understanding

**When:** Inheriting a model or before modifications

**What you get:**
- List of all HVAC loops (plant, condenser, air)
- Equipment on each loop
- Topology diagrams
- Control sequences

**Output:** HVAC topology report with visual diagrams

---

### 3. Parametric ECM Testing

**When:** Testing multiple energy conservation measures

**What it does:**
- Runs baseline simulation
- Modifies equipment (lights, plugs, infiltration, etc.)
- Runs ECM scenarios
- Compares energy/cost/GHG savings

**Output:** ECM comparison report with rankings

---

## SECC Project Quick Reference

**Model Path:**
```
C:\Users\mcoalson\Documents\WorkPath\User-Files\work-tracking\secc-fort-collins\energy-model\SECC_WSHP_ProposedModel_v3_WaterLoop_RTUHP_DOAS_Pool\run\in.idf
```

**Container Path (for MCP tools):**
```
/workspace/models/SECC_WSHP_ProposedModel_v3_WaterLoop_RTUHP_DOAS_Pool/run/in.idf
```

**Weather File Needed:**
```
USA_CO_Fort.Collins-Loveland.Muni.AP.724769_TMY3.epw
```

**Deliverables (Due Nov 27):**
- EUI (Energy Use Intensity)
- GHG (Greenhouse Gas Emissions)
- Utility Cost

---

## MCP Tools Available

### Model Loading & Validation
- `load_idf_model` - Load IDF file
- `validate_idf` - Check syntax
- `get_model_summary` - High-level overview
- `check_simulation_settings` - Review run settings

### Inspection
- `list_zones` - Get all thermal zones
- `get_surfaces` - Surface information
- `get_materials` - Construction materials
- `inspect_schedules` - Schedule definitions
- `inspect_people` - Occupancy
- `inspect_lights` - Lighting loads
- `inspect_electric_equipment` - Plug loads

### Modification
- `modify_lights` - Adjust lighting
- `modify_electric_equipment` - Change plug loads
- `modify_people` - Update occupancy
- `change_infiltration_by_mult` - Scale infiltration
- `add_output_variables` - Request outputs
- `add_output_meters` - Request meters

### HVAC Analysis
- `discover_hvac_loops` - Find all loops
- `get_loop_topology` - Get loop details
- `visualize_loop_diagram` - Create diagrams

### Simulation
- `run_energyplus_simulation` - Execute simulation
- `create_interactive_plot` - Visualize results

### Server Management
- `get_server_status` - Check health
- `get_error_logs` - View errors
- `get_server_logs` - View logs

---

## Example Session

```
User: I need to validate my SECC model before rebuilding the HVAC

Assistant (work-command-center): I'll invoke energyplus-assistant to run QA/QC

[energyplus-assistant activated]