# Windows Environment Setup

Specific guidance for running EnergyPlus workflows on Windows in VSCode.

---

## Python Setup

### Check Python Installation

```bash
# Windows often has multiple Python installations
python --version
python3 --version
py --version

# Use whichever shows Python 3.10+
```

### Install Dependencies

```bash
# Install eppy for IDF parsing
pip install eppy

# Or use Python launcher
py -m pip install eppy
```

### Console Encoding Issues

Windows command prompt and PowerShell sometimes have encoding issues with non-ASCII characters.

**Symptoms:**
- `UnicodeEncodeError: 'charmap' codec can't encode character`
- Special characters not displaying correctly

**Solution:**

```bash
# PowerShell
$env:PYTHONIOENCODING = "utf-8"
python script.py

# Git Bash
export PYTHONIOENCODING=utf-8
python script.py

# Or set globally in PowerShell profile
Add-Content $PROFILE '$env:PYTHONIOENCODING = "utf-8"'
```

**Alternative:** Use Python's `-X utf8` flag:
```bash
python -X utf8 ./scripts/qaqc-direct.py model.idf
```

---

## Docker Desktop (For MCP Tools)

### Prerequisites

1. **Install Docker Desktop**: https://www.docker.com/products/docker-desktop/
2. **Enable WSL 2** (recommended): Faster than Hyper-V
3. **Start Docker Desktop** before attempting MCP operations

### Check Docker Status

```bash
# Verify Docker is running
docker ps

# If error "Cannot connect to Docker daemon"
# → Start Docker Desktop application
```

### Docker Path Formats

Windows paths need special handling when mounting volumes.

#### Mount Points - Always Use Forward Slashes

```bash
# ✅ CORRECT - Forward slashes
docker run -v C:/Users/mcoalson/Documents/WorkPath:/workspace ...

# ❌ WRONG - Backslashes
docker run -v C:\Users\mcoalson\Documents\WorkPath:/workspace ...
```

#### Working Directory - Depends on Shell

**PowerShell:**
```bash
# Use single forward slashes
docker run --workdir /workspace/repo/energyplus-mcp-server ...
```

**Git Bash:**
```bash
# Use DOUBLE forward slashes (prevents path translation)
docker run --workdir //workspace//repo//energyplus-mcp-server ...
```

**Why?** Git Bash automatically translates Unix paths to Windows paths. Double slashes disable this translation.

### Common Docker Issues

**"Error response from daemon: mkdir [path]: Access is denied"**
- Cause: Incorrect path format (backslashes instead of forward slashes)
- Solution: Use `C:/Users/...` format

**"the working directory [path] is invalid"**
- Cause: Git Bash path translation
- Solution: Use `//workspace//...` instead of `/workspace/...`

**"Cannot connect to Docker daemon"**
- Cause: Docker Desktop not running
- Solution: Start Docker Desktop application

**"Container startup very slow"**
- Cause: First-time dependency installation
- Solution: Use direct parsing methods for QA/QC (faster)

---

## File Paths

### Local Paths vs Container Paths

When using MCP Docker container, understand path mapping:

**Your local file:**
```
C:\Users\mcoalson\Documents\WorkPath\User-Files\work-tracking\secc-fort-collins\energy-model\model.idf
```

**Container path (what Docker sees):**
```
/workspace/models/model.idf
```

**Mapping configured in `.vscode/settings.json`:**
```json
{
  "mcp.servers": {
    "energyplus": {
      "command": "docker",
      "args": [
        "--mount",
        "type=bind,source=C:\\Users\\mcoalson\\Documents\\WorkPath\\User-Files\\work-tracking\\secc-fort-collins\\energy-model,target=/workspace/models"
      ]
    }
  }
}
```

### Path Conversion Examples

| Windows Path | Docker Mount | Container Path |
|--------------|--------------|----------------|
| `C:\Users\mcoalson\...\energy-model\run\in.idf` | `source=C:/Users/mcoalson/.../energy-model,target=/workspace/models` | `/workspace/models/run/in.idf` |
| `C:\EnergyPlus\WeatherData\USA_CO_Fort.Collins.epw` | `source=C:/EnergyPlus/WeatherData,target=/workspace/weather` | `/workspace/weather/USA_CO_Fort.Collins.epw` |

---

## Git Bash Considerations

### Path Translation

Git Bash automatically translates Unix-style paths to Windows paths:

```bash
# You type:
cd /c/Users/mcoalson

# Git Bash translates to:
C:\Users\mcoalson
```

**Problem for Docker:** When paths are arguments to Docker, this translation can cause issues.

**Solution:** Use double slashes for Docker container paths:

```bash
# In Git Bash
docker run --workdir //workspace//repo//subdir ...
```

### Alternative: Use PowerShell

For Docker operations, PowerShell often more reliable:

```powershell
# PowerShell handles paths more predictably
docker run --workdir /workspace/repo/subdir ...
```

---

## Node.js Setup

### Check Installation

```bash
node --version  # Should be 18+
npm --version
```

### Running Scripts

```bash
# Node.js scripts work same on Windows as Unix
node ./scripts/qaqc-direct.js model.idf
```

### ESM vs CommonJS

Modern Node.js (18+) supports ESM imports:

```javascript
// ✅ GOOD - ESM (use in .mjs files or with "type": "module" in package.json)
import { readFile } from 'fs/promises';

// ❌ AVOID - CommonJS (old style)
const fs = require('fs');
```

---

## IDE Configuration

### VSCode Terminal

**Recommended:** Use PowerShell or Git Bash terminal in VSCode.

**Change default terminal:**
1. `Ctrl+Shift+P`
2. Search "Terminal: Select Default Profile"
3. Choose "PowerShell" or "Git Bash"

### Character Encoding

If seeing garbled output in terminal:

1. Check terminal encoding: Click encoding in bottom-right of VSCode
2. Select "UTF-8"
3. Restart terminal

---

## Performance Optimization

### Docker vs Direct Methods

**For QA/QC:**
- Docker startup: 30+ seconds (first time dependency install)
- Direct Python: < 5 seconds
- **Recommendation:** Use direct methods

**For HVAC Analysis:**
- Docker may be necessary for complex topology
- Consider if speed worth the wait

**For Simulations:**
- Use native EnergyPlus installation (faster than Docker)
- Docker useful for reproducibility/isolation

### Disk Location

**Faster:**
- Local SSD (C: drive)
- Files in `C:\Users\username\...`

**Slower:**
- Network drives
- External USB drives
- OneDrive/cloud sync folders (disable sync during simulations)

---

## Troubleshooting

### "pip: command not found"

```bash
# Try these alternatives
python -m pip install eppy
py -m pip install eppy
python3 -m pip install eppy
```

### "docker: command not found"

1. Ensure Docker Desktop is installed
2. Restart terminal after installation
3. Check Docker Desktop is running

### "Permission denied" errors

1. Run terminal as Administrator (for system-wide installs)
2. Or use `--user` flag:
   ```bash
   pip install --user eppy
   ```

### Scripts won't execute

**PowerShell execution policy:**
```powershell
# Check current policy
Get-ExecutionPolicy

# Allow scripts (if needed)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**File path spaces:**
```bash
# Use quotes for paths with spaces
python "./scripts/qaqc-direct.py" "C:/Users/First Last/Documents/model.idf"
```

---

## Best Practices for Windows

1. **Use forward slashes** in Docker mount paths
2. **Use double slashes** in Docker workdir (Git Bash)
3. **Set UTF-8 encoding** for Python scripts
4. **Check Docker is running** before MCP operations
5. **Prefer direct parsing** for QA/QC (faster)
6. **Use PowerShell** for Docker operations (more predictable)
7. **Avoid network/cloud drives** for simulations (slow)

---

*Windows-specific guidance for EnergyPlus workflows*
