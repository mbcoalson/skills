# Work Command Center Tools

This directory contains utility tools that the Work Command Center skill can use for various operations.

## Available Tools

### get-datetime.js
**Purpose:** Provides current date/time context for accurate deadline tracking and priority management

**Usage:**
```bash
# Standard output
node get-datetime.js

# JSON output (for programmatic use)
node get-datetime.js --json
```

**Output Fields:**
- **current**: Full date, time, ISO formats, day of week, week number, day of year
- **formatted**: Pre-formatted strings for display, filenames, and logs
- **timestamps**: Unix timestamp and milliseconds since epoch

**Use Cases:**
- Skill startup to establish temporal context
- Deadline calculations
- Generating daily log filenames
- Timestamp tracking in deliverables

### convert-to-markdown.py
**Purpose:** Convert various file types to LLM-ready Markdown using Microsoft's markitdown library

**Supported File Types:**
- **Documents**: PDF, DOCX, PPTX, XLSX, XLS
- **Media**: JPG, PNG, WAV, MP3
- **Web**: HTML
- **Archives**: ZIP

**Usage:**
```bash
# Convert to markdown file (auto-generates output name)
python convert-to-markdown.py input.pdf

# Convert with custom output name
python convert-to-markdown.py input.pdf output.md

# Print to stdout
python convert-to-markdown.py input.docx --stdout

# Get JSON output with metadata
python convert-to-markdown.py input.xlsx --json
```

**Use Cases:**
- Convert EOR documents (PDFs) to markdown for analysis
- Extract text from presentations and spreadsheets
- Prepare engineering documents for LLM processing
- Batch convert project documentation to markdown format

## Future Tool Ideas

### budget-checker.js
Calculate remaining hours and budget status for projects

### deadline-calculator.js
Calculate days until deadlines, flag urgent items

### team-workload.js
Analyze team member workload distribution

### priority-scorer.js
Score deliverables based on urgency, importance, budget status

---

Last Updated: 2025-11-20
