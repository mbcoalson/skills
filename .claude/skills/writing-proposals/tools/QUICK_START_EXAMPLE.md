# Quick Start Example - Word Template Automation

## Example: Create Mytikas Industries Proposal

This example shows how to use COM automation to create the Mytikas Industries proposal from earlier.

### Step 1: Install Dependencies

```bash
pip install pywin32
```

### Step 2: Prepare Your Template

Your Word template should have placeholders like:

```
Client: {{CLIENT_NAME}}
Address: {{FACILITY_ADDRESS}}
Project: {{PROJECT_DESCRIPTION}}
Fee: {{TOTAL_FEE}}
```

### Step 3: Create Mapping File

Create `mytikas-mapping.json`:

```json
{
  "{{CLIENT_NAME}}": "Mytikas Industries",
  "{{FACILITY_ADDRESS}}": "1173 State Highway 120, Florence, CO 81226",
  "{{FACILITY_SIZE}}": "150,000 sf",
  "{{PROJECT_DESCRIPTION}}": "Industrial Energy Feasibility Study for CITCO grant compliance",
  "{{SERVICE_TYPE}}": "Industrial Energy Feasibility Study",
  "{{TOTAL_FEE}}": "$19,000",
  "{{TIMELINE}}": "January 2026 - April 2026",
  "{{COMPLETION_DATE}}": "April 2026",
  "{{GRANT_PROGRAM}}": "Colorado Industrial Tax Credit Offering (CITCO)",
  "{{PE_NAME}}": "Matthew Coalson, PE",
  "{{CONTACT_NAME}}": "Matt Coalson",
  "{{CONTACT_EMAIL}}": "mcoalson@iconergy.com",
  "{{DATE}}": "December 19, 2025"
}
```

### Step 4: Process Template

```bash
cd .claude/skills/writing-proposals

python tools/word-template-automation.py \
  templates/proposal-template.docx \
  Mytikas_Industries_Proposal.docx \
  --mapping mytikas-mapping.json
```

### Expected Output

```
================================================================================
WORD TEMPLATE AUTOMATION
================================================================================
Template: templates/proposal-template.docx
Output: Mytikas_Industries_Proposal.docx
Replacements: 13
================================================================================

[COM] Starting Microsoft Word...
[COM] Word application started successfully
[COM] Opening template: proposal-template.docx
[COM] Template opened successfully

[COM] Replacing 13 placeholders...
  Replacing '{{CLIENT_NAME}}' -> 'Mytikas Industries'
  Replacing '{{FACILITY_ADDRESS}}' -> '1173 State Highway 120, Florence, CO 81226'
  Replacing '{{FACILITY_SIZE}}' -> '150,000 sf'
  ...

================================================================================
REPLACEMENT SUMMARY
================================================================================
  ✓ {{CLIENT_NAME}}: 1 replacements
  ✓ {{FACILITY_ADDRESS}}: 1 replacements
  ✓ {{FACILITY_SIZE}}: 1 replacements
  ...

[COM] Saving document: Mytikas_Industries_Proposal.docx
[COM] Document saved successfully
[COM] Closing document...
[COM] Document closed
[COM] Quitting Word application...
[COM] Word application closed

================================================================================
[SUCCESS] TEMPLATE PROCESSING COMPLETE
================================================================================
Output file: C:\...\Mytikas_Industries_Proposal.docx
================================================================================
```

### Step 5: Review Output

Open `Mytikas_Industries_Proposal.docx` in Word and verify:

- All placeholders replaced
- Formatting preserved perfectly
- Headers/footers updated
- Tables intact
- Images/logos still present

---

## Alternative: Interactive Mode

For a guided workflow:

```bash
python tools/word-template-automation.py --interactive
```

Follow the prompts:

1. Select template from list
2. Tool will find all placeholders
3. Enter replacement values for each
4. Specify output filename
5. Done!

---

## Alternative: Quick Command-Line

For simple replacements without a mapping file:

```bash
python tools/word-template-automation.py \
  templates/proposal-template.docx \
  Quick_Proposal.docx \
  --replace "{{CLIENT_NAME}}" "Quick Client Inc" \
  --replace "{{FEE}}" "$10,000" \
  --replace "{{DATE}}" "2025-12-19"
```

---

## Troubleshooting

### Can't find template

If you get "Template not found", make sure you're running from the skill directory:

```bash
cd c:\Users\mcoalson\Documents\WorkPath\.claude\skills\writing-proposals
python tools/word-template-automation.py --interactive
```

Or use full paths:

```bash
python tools/word-template-automation.py \
  "c:\Users\mcoalson\Documents\WorkPath\.claude\skills\writing-proposals\templates\proposal-template.docx" \
  "c:\Users\mcoalson\Documents\output\proposal.docx" \
  --mapping mapping.json
```

### pywin32 not installed

```bash
pip install pywin32
```

If you get DLL errors after installing, try:

```bash
python Scripts/pywin32_postinstall.py -install
```

### Word hangs or crashes

- Close all Word windows before running
- Try `--visible` mode to see what's happening
- Check if Word is asking for permission (macro security, etc.)
- Restart computer if Word process is stuck

---

## Best Practices

1. **Test first**: Always test with a copy of your template
2. **Use mapping files**: Better for complex proposals than command-line args
3. **Consistent placeholders**: Use {{UPPERCASE_WITH_UNDERSCORES}} format
4. **Document placeholders**: Add reference section to template
5. **Version control**: Keep templates and mapping files in git

---

## Next Steps

- Read full documentation: [README_COM_AUTOMATION.md](./README_COM_AUTOMATION.md)
- Explore example mapping: [../templates/example-mapping.json](../templates/example-mapping.json)
- Create your own templates with placeholders
- Build reusable mapping files for common proposal types
