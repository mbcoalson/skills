# EnergyPlus-MCP Server Setup Guide

**Status:** Docker build in progress
**Last Updated:** 2025-11-23

---

## Prerequisites

✅ **Python 3.12** - Installed and verified
✅ **Docker 28.3.2** - Installed and verified
✅ **Docker Desktop** - Running
❌ **EnergyPlus 25.1.0** - Not required for Docker setup (included in container)

---

## Installation Steps

### 1. Clone Repository ✅ COMPLETE

Repository cloned to:
```
C:\Users\mcoalson\Documents\WorkPath\EnergyPlus-MCP
```

### 2. Start Docker Desktop ✅ COMPLETE

Docker is running and ready.

### 3. Build Docker Image 🔄 IN PROGRESS

Building Docker image with EnergyPlus 25.1.0...

```bash
cd /c/Users/mcoalson/Documents/WorkPath/EnergyPlus-MCP
docker build -t energyplus-mcp-dev .devcontainer/
```

**Expected Build Time:** 5-10 minutes (downloads EnergyPlus and Python dependencies)

**What this does:**
- Creates Docker container with EnergyPlus 25.1.0
- Installs Python dependencies for MCP server
- Sets up server environment

### 4. Configure MCP Server in VS Code (NEXT STEP)

**Location:** `.vscode/settings.json` (workspace settings)

Add MCP server configuration:

```json
{
  "chatgpt.commentCodeLensEnabled": false,
  "mcp.servers": {
    "energyplus": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "--mount", "type=bind,source=C:\\Users\\mcoalson\\Documents\\WorkPath\\User-Files\\work-tracking\\secc-fort-collins\\energy-model,target=/workspace/models",
        "--mount", "type=bind,source=C:\\Users\\mcoalson\\Documents\\WorkPath\\EnergyPlus-MCP\\sample_files,target=/workspace/sample_files",
        "energyplus-mcp-dev"
      ]
    }
  }
}
```

**What this configuration does:**
- Mounts SECC model directory to `/workspace/models` in container
- Mounts sample files to `/workspace/sample_files`
- Runs server in interactive mode
- Auto-removes container when done

### 5. Restart VS Code / Reload Window

After adding MCP configuration:
1. Press `Ctrl+Shift+P`
2. Type "Reload Window"
3. Select "Developer: Reload Window"

This activates the MCP server.

### 6. Verify MCP Server Connection

In a new Claude Code conversation, test:

```
Can you list the available MCP tools for EnergyPlus?
```

Expected: Should see 35 tools listed (load_idf_model, validate_idf, etc.)

---

## File Paths for SECC Project

### Local Paths (Your Machine)
```
Model Location: C:\Users\mcoalson\Documents\WorkPath\User-Files\work-tracking\secc-fort-collins\energy-model\SECC_WSHP_ProposedModel_v3_WaterLoop_RTUHP_DOAS_Pool\run\in.idf

Weather Files: [Location TBD - need to add Fort Collins TMY3 EPW file]
```

### Container Paths (Inside Docker)
```
Models: /workspace/models/SECC_WSHP_ProposedModel_v3_WaterLoop_RTUHP_DOAS_Pool/run/in.idf

Sample Files: /workspace/sample_files/
```

**When using MCP tools, reference container paths:**
```json
{
  "tool": "load_idf_model",
  "arguments": {
    "idf_path": "/workspace/models/SECC_WSHP_ProposedModel_v3_WaterLoop_RTUHP_DOAS_Pool/run/in.idf"
  }
}
```

---

## Weather File Setup

**Required for SECC:** Fort Collins, CO TMY3 weather file

### Download Location
[climate.onebuilding.org](https://climate.onebuilding.org)

**Search for:** Fort Collins, Colorado, USA

**Expected filename:** `USA_CO_Fort.Collins-Loveland.Muni.AP.724769_TMY3.epw`

**Save to:**
```
C:\Users\mcoalson\Documents\WorkPath\User-Files\work-tracking\secc-fort-collins\energy-model\weather\
```

**Then update VS Code settings.json** to mount weather directory:
```json
"--mount", "type=bind,source=C:\\Users\\mcoalson\\Documents\\WorkPath\\User-Files\\work-tracking\\secc-fort-collins\\energy-model\\weather,target=/workspace/weather"
```

---

## Troubleshooting

### Docker Build Fails
**Error:** `Cannot connect to Docker daemon`
**Solution:** Start Docker Desktop and retry

### MCP Server Not Showing in Claude Code
**Solution:**
1. Check `.vscode/settings.json` syntax (valid JSON)
2. Reload VS Code window
3. Check Docker image built successfully: `docker images | grep energyplus`

### Cannot Access Model Files
**Error:** File not found in container
**Solution:**
1. Verify mount paths in `.vscode/settings.json`
2. Ensure backslashes escaped in Windows paths (`\\`)
3. Use container paths when calling MCP tools (e.g., `/workspace/models/...`)

### Simulation Fails
**Check:**
1. Weather file path correct
2. IDF file valid (use `validate_idf` first)
3. Check error logs: Use `get_error_logs` tool

---

## Alternative Setup: Local Python (No Docker)

If Docker approach has issues, can install locally:

### Requirements
1. Install EnergyPlus 25.1.0 from [energyplus.net](https://energyplus.net/)
2. Clone repo (already done)
3. Install UV package manager: `pip install uv`
4. Install dependencies: `cd EnergyPlus-MCP && uv sync --extra dev`
5. Run server: `uv run mcp-server-energyplus`

**VS Code configuration for local setup:**
```json
{
  "mcp.servers": {
    "energyplus": {
      "command": "uv",
      "args": ["run", "mcp-server-energyplus"],
      "cwd": "C:\\Users\\mcoalson\\Documents\\WorkPath\\EnergyPlus-MCP"
    }
  }
}
```

---

## Next Steps After Installation

Once MCP server is running:

1. **Test with sample file:**
   - Load `1ZoneUncontrolled.idf` from sample_files
   - Validate model
   - Run simple simulation

2. **Test with SECC model:**
   - Load SECC v3 in.idf
   - Run QA/QC workflow
   - Analyze HVAC topology

3. **Invoke energyplus-assistant skill:**
   - Use work-command-center
   - Request: "Validate my SECC energy model"
   - Skill handles MCP tool orchestration

---

## Status Checklist

- [x] Repository cloned
- [x] Python 3.12 installed
- [x] Docker installed
- [x] Docker Desktop running
- [ ] Docker image built (IN PROGRESS)
- [ ] VS Code MCP config added
- [ ] VS Code reloaded
- [ ] MCP server connection verified
- [ ] Weather file downloaded
- [ ] Test simulation successful
- [ ] SECC model loaded and validated

---

**Installation Support:** If issues arise, check [LBNL-ETA/EnergyPlus-MCP Issues](https://github.com/LBNL-ETA/EnergyPlus-MCP/issues)

**Last Updated:** 2025-11-23
