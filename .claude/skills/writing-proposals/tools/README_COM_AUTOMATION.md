# Word Template Automation via COM

Advanced Word template processing using Windows COM automation (`win32com.client`).

## Why COM Automation vs python-docx?

| Feature | COM Automation | python-docx |
|---------|---------------|-------------|
| **Full Word features** | ✅ Complete object model | ❌ Limited subset |
| **Find/Replace reliability** | ✅ Word's native engine | ⚠️ Manual paragraph iteration |
| **Format preservation** | ✅ Perfect | ⚠️ Sometimes loses formatting |
| **Headers/Footers** | ✅ Automatic | ⚠️ Manual iteration |
| **Text boxes/Shapes** | ✅ Automatic | ⚠️ Manual iteration |
| **Content controls** | ✅ Full support | ❌ Not supported |
| **Complex tables** | ✅ Perfect handling | ⚠️ Can corrupt structure |
| **Platform** | ⚠️ Windows only | ✅ Cross-platform |
| **Requires Word installed** | ⚠️ Yes | ✅ No |

**Bottom line**: Use COM automation when you need reliability and full Word functionality on Windows. Use python-docx for cross-platform or when Word isn't available.

---

## Installation

```bash
pip install pywin32
```

**Note**: Microsoft Word must be installed on your Windows machine.

---

## Quick Start

### 1. List Placeholders in Template

First, see what placeholders exist in your template:

```bash
python word-template-automation.py proposal-template.docx --list-placeholders
```

**Output:**
```
Found 15 unique placeholders:

   1. {{CLIENT_NAME}}
   2. {{PROJECT_ADDRESS}}
   3. {{BUILDING_SIZE}}
   4. {{SERVICE_TYPE}}
   5. {{TOTAL_FEE}}
   ...
```

### 2. Create Mapping Template

Generate a JSON file with all placeholders:

```bash
python word-template-automation.py proposal-template.docx --create-mapping mapping.json
```

This creates `mapping.json`:
```json
{
  "{{CLIENT_NAME}}": "",
  "{{PROJECT_ADDRESS}}": "",
  "{{BUILDING_SIZE}}": "",
  "{{SERVICE_TYPE}}": "",
  "{{TOTAL_FEE}}": ""
}
```

### 3. Fill in Values

Edit `mapping.json`:
```json
{
  "{{CLIENT_NAME}}": "Mytikas Industries",
  "{{PROJECT_ADDRESS}}": "1173 State Highway 120, Florence, CO 81226",
  "{{BUILDING_SIZE}}": "150,000",
  "{{SERVICE_TYPE}}": "Industrial Energy Feasibility Study",
  "{{TOTAL_FEE}}": "$19,000"
}
```

### 4. Process Template

```bash
python word-template-automation.py proposal-template.docx Mytikas_Proposal.docx --mapping mapping.json
```

**Done!** Your proposal is ready with all placeholders replaced.

---

## Usage Modes

### Command-Line Mode with --replace

Quick one-off replacements:

```bash
python word-template-automation.py template.docx output.docx \
  --replace "{{CLIENT}}" "Acme Corp" \
  --replace "{{DATE}}" "2025-12-19" \
  --replace "{{FEE}}" "$25,000"
```

### Mapping File Mode (Recommended)

For complex proposals with many placeholders:

```bash
# 1. Create mapping template
python word-template-automation.py template.docx --create-mapping mapping.json

# 2. Edit mapping.json with your values

# 3. Process template
python word-template-automation.py template.docx output.docx --mapping mapping.json
```

### Interactive Mode

Guided workflow:

```bash
python word-template-automation.py --interactive
```

This will:
1. Show all templates in `templates/` folder
2. Let you select one
3. Find all placeholders
4. Prompt for replacement values
5. Generate output file

---

## Placeholder Formats

### Default Format: `{{NAME}}`

The tool uses `{{PLACEHOLDER}}` format by default (double curly braces, uppercase letters and underscores).

### Custom Formats

You can use any placeholder format by specifying a regex pattern:

**Square brackets: `[NAME]`**
```bash
python word-template-automation.py template.docx --list-placeholders \
  --pattern "\[[A-Z_]+\]"
```

**Triple hash: `###NAME###`**
```bash
python word-template-automation.py template.docx --list-placeholders \
  --pattern "###[A-Z_]+###"
```

**Angle brackets: `<<NAME>>`**
```bash
python word-template-automation.py template.docx --list-placeholders \
  --pattern "<<[A-Z_]+>>"
```

**Mixed case: `{{ClientName}}`**
```bash
python word-template-automation.py template.docx --list-placeholders \
  --pattern "\{\{[A-Za-z_]+\}\}"
```

---

## Advanced Features

### Case-Sensitive Replacement

```bash
python word-template-automation.py template.docx output.docx \
  --mapping mapping.json \
  --match-case
```

### Whole Word Matching

Prevents partial word matches:

```bash
python word-template-automation.py template.docx output.docx \
  --replace "{{FEE}}" "$19,000" \
  --match-whole-word
```

### Visible Mode (Debugging)

See Word working in real-time:

```bash
python word-template-automation.py template.docx output.docx \
  --mapping mapping.json \
  --visible
```

Useful for troubleshooting template issues.

---

## Template Best Practices

### 1. Use Consistent Placeholder Format

**Good:**
```
Client: {{CLIENT_NAME}}
Address: {{PROJECT_ADDRESS}}
Fee: {{TOTAL_FEE}}
```

**Avoid:**
```
Client: [CLIENT_NAME]        # Mixed formats
Address: {{ProjectAddress}}  # Inconsistent casing
Fee: <<TOTAL_FEE>>          # Different delimiters
```

### 2. Use Descriptive Names

**Good:**
```
{{CLIENT_NAME}}
{{BUILDING_SQUARE_FOOTAGE}}
{{SERVICE_TYPE}}
{{ASHRAE_LEVEL}}
```

**Avoid:**
```
{{NAME}}          # Too generic
{{SF}}            # Not descriptive
{{TYPE}}          # Ambiguous
{{LEVEL}}         # Unclear
```

### 3. Document Placeholders

Add a comment section in your template:

```
PLACEHOLDER REFERENCE:
{{CLIENT_NAME}}              - Full legal business name
{{PROJECT_ADDRESS}}          - Complete building address with city, state, ZIP
{{BUILDING_SQUARE_FOOTAGE}}  - Building size (e.g., "150,000")
{{SERVICE_TYPE}}             - Type of service (e.g., "ASHRAE Level 2 Audit")
{{TOTAL_FEE}}                - Total fee with currency (e.g., "$19,000")
{{DATE}}                     - Proposal date (MM/DD/YYYY)
```

### 4. Test Templates

Before using in production:

```bash
# 1. List all placeholders
python word-template-automation.py template.docx --list-placeholders

# 2. Create test mapping with dummy data
python word-template-automation.py template.docx --create-mapping test-mapping.json

# 3. Fill with test values and process
python word-template-automation.py template.docx test-output.docx --mapping test-mapping.json

# 4. Review test-output.docx for formatting issues
```

---

## Troubleshooting

### "pywin32 is not installed"

```bash
pip install pywin32
```

If that doesn't work, try:
```bash
pip install --upgrade pywin32
python -c "import win32com.client"
```

### "Failed to start Word"

**Causes:**
- Word not installed
- Word is already open and locked
- Insufficient permissions

**Solutions:**
- Install Microsoft Word
- Close all Word windows
- Run as administrator (if needed)

### "No placeholders found"

**Causes:**
- Template doesn't use `{{PLACEHOLDER}}` format
- Different placeholder format
- No placeholders in template

**Solutions:**
```bash
# Try listing with custom pattern
python word-template-automation.py template.docx --list-placeholders --pattern "\[PLACEHOLDER\]"

# Check template manually in Word
# Look for: {{NAME}}, [NAME], ###NAME###, <<NAME>>, etc.
```

### Replacements Not Working

**Causes:**
- Typo in placeholder name
- Case sensitivity mismatch
- Placeholder split across formatting runs

**Solutions:**
```bash
# List exact placeholders in template
python word-template-automation.py template.docx --list-placeholders

# Copy-paste exact placeholder names into mapping.json

# Use case-insensitive matching (default)
# Don't use --match-case unless you need it
```

### Format Lost After Replacement

This shouldn't happen with COM automation (that's the main benefit), but if it does:

1. Check template - ensure placeholder has the formatting you want
2. Use `--visible` mode to watch the replacement happen
3. Verify template isn't corrupted (open in Word, save, try again)

---

## Integration with Claude Code Skills

### Calling from Python Scripts

```python
from pathlib import Path
import sys

# Add tool to path
tool_dir = Path(__file__).parent
sys.path.insert(0, str(tool_dir))

from word_template_automation import WordTemplateAutomation, process_template

# Define replacements
replacements = {
    "{{CLIENT_NAME}}": "Mytikas Industries",
    "{{SERVICE_TYPE}}": "Feasibility Study",
    "{{TOTAL_FEE}}": "$19,000"
}

# Process template
template = Path("templates/proposal-template.docx")
output = Path("output/Mytikas_Proposal.docx")

success = process_template(
    template,
    output,
    replacements,
    match_case=False,
    visible=False
)

print(f"Success: {success}")
```

### Context Manager Pattern

```python
from word_template_automation import WordTemplateAutomation

with WordTemplateAutomation(visible=False) as word:
    # Open template
    word.open_template(Path("template.docx"))

    # Find what placeholders exist
    placeholders = word.find_placeholders()
    print(f"Found: {placeholders}")

    # Replace one at a time with custom logic
    word.replace_text("{{CLIENT}}", client_name)
    word.replace_text("{{DATE}}", current_date)

    # Save
    word.save_as(Path("output.docx"))

# Word automatically quits when exiting context
```

---

## Examples

### Example 1: Simple Proposal

**Template:** `templates/simple-proposal.docx`
```
PROPOSAL FOR {{CLIENT_NAME}}

Project: {{PROJECT_DESCRIPTION}}
Fee: {{TOTAL_FEE}}
Date: {{DATE}}
```

**Command:**
```bash
python word-template-automation.py simple-proposal.docx client-proposal.docx \
  --replace "{{CLIENT_NAME}}" "Acme Corporation" \
  --replace "{{PROJECT_DESCRIPTION}}" "Energy Audit" \
  --replace "{{TOTAL_FEE}}" "$25,000" \
  --replace "{{DATE}}" "2025-12-19"
```

### Example 2: CITCO Grant Proposal

**Mapping file:** `citco-mapping.json`
```json
{
  "{{CLIENT_NAME}}": "Mytikas Industries",
  "{{FACILITY_ADDRESS}}": "1173 State Highway 120, Florence, CO 81226",
  "{{FACILITY_SIZE}}": "150,000 sf",
  "{{STUDY_TYPE}}": "Industrial Energy Feasibility Study",
  "{{GRANT_PROGRAM}}": "CITCO Industrial Studies",
  "{{TOTAL_FEE}}": "$19,000",
  "{{COMPLETION_DATE}}": "April 2026",
  "{{PE_NAME}}": "Matthew Coalson, PE",
  "{{PE_LICENSE}}": "CO-12345",
  "{{CONTACT_NAME}}": "Kelly Jones",
  "{{CONTACT_EMAIL}}": "Kelly.Jones@haastechwriting.com"
}
```

**Command:**
```bash
python word-template-automation.py \
  templates/citco-proposal-template.docx \
  Mytikas_CITCO_Proposal.docx \
  --mapping citco-mapping.json
```

### Example 3: Batch Processing Multiple Proposals

**Python script:** `batch-process.py`
```python
from pathlib import Path
from word_template_automation import process_template
import json

# Load template
template = Path("templates/proposal-template.docx")

# Client data
clients = [
    {
        "name": "Client A",
        "file": "ClientA_Proposal.docx",
        "mappings": {
            "{{CLIENT_NAME}}": "Client A Corp",
            "{{SERVICE}}": "Level 2 Audit",
            "{{FEE}}": "$40,000"
        }
    },
    {
        "name": "Client B",
        "file": "ClientB_Proposal.docx",
        "mappings": {
            "{{CLIENT_NAME}}": "Client B Inc",
            "{{SERVICE}}": "Benchmarking",
            "{{FEE}}": "$5,000"
        }
    }
]

# Process each
for client in clients:
    print(f"\nProcessing {client['name']}...")
    output = Path(f"output/{client['file']}")
    success = process_template(template, output, client['mappings'])
    if success:
        print(f"  ✓ {client['file']} created")
    else:
        print(f"  ✗ {client['file']} failed")
```

---

## Performance

COM automation is fast for typical proposals:

| Document Size | Placeholders | Time |
|--------------|--------------|------|
| 5 pages      | 10-20        | ~2 seconds |
| 15 pages     | 30-50        | ~3 seconds |
| 50 pages     | 100+         | ~5-8 seconds |

**Tips for large documents:**
- Use mapping file instead of individual --replace calls
- Avoid `--visible` mode (slower)
- Close other Word documents before running

---

## Security Notes

**COM automation runs actual Word application:**
- Can execute macros in templates (be careful with untrusted templates)
- Has full file system access (same as Word)
- Runs with your user permissions

**Best practices:**
- Only use trusted templates
- Disable macros in templates if not needed
- Don't run as administrator unless necessary
- Review templates before first use

---

## Support

**Issues with this tool:**
- Check this README first
- Try `--visible` mode to debug
- Verify template opens correctly in Word
- Check placeholder format matches pattern

**Questions about Word object model:**
- https://learn.microsoft.com/en-us/office/vba/api/overview/word

**pywin32 documentation:**
- https://github.com/mhammond/pywin32
