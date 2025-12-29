# Work Command Center - Tool Reference

This document describes all available CLI tools for the Work Command Center skill.

---

## Date/Time Utility

**Location:** `tools/get-datetime.js`

**Purpose:** Provides current date/time context for accurate deadline tracking and priority management

**Usage:**

```bash
# Run on skill startup for temporal context
node .claude/skills/work-command-center/tools/get-datetime.js

# JSON output for programmatic use
node .claude/skills/work-command-center/tools/get-datetime.js --json
```

**Output:** Current date, time, ISO format, day of week, week number, and formatted strings for logs/filenames

**When to Use:**
- At the start of every Work Command Center session
- When calculating deadline urgency
- When creating dated log files

---

## Session State Management (Primary Time Tracking)

**Location:** `tools/session-state.js`

**Purpose:** Automatic session-based time tracking that persists across chat restarts and context limit resets

**Data Files:**
- Active session: `User-Files/work-tracking/active-session.json`
- Time log: `User-Files/work-tracking/time-log.jsonl`

**Key Features:**
- Survives new chat sessions when approaching context limits
- Automatic duration calculation from start to finish
- Activity tracking throughout session
- Checkpoint system for long-running work
- Abandoned session detection and recovery

### Commands

#### Start New Session

```bash
node .claude/skills/work-command-center/tools/session-state.js start \
  --project "Project Name" \
  --project-number "PN-123" \
  --task "Initial task description"
```

**Parameters:**
- `--project` (required): Project name
- `--project-number` (required): Project number for billing/tracking (e.g., "EA-2024-089", "MB-2025-001")
- `--task` (optional): Initial task description

**When to Use:** At the beginning of every Work Command Center session (after checking for existing active sessions)

**Creates:** `active-session.json` with session ID, start time, project, project number, and initial task

**Example:**
```bash
node .claude/skills/work-command-center/tools/session-state.js start \
  --project "Office Building Energy Audit" \
  --project-number "EA-2024-089" \
  --task "Energy model QA/QC review"
```

---

#### Checkpoint Active Session

```bash
# Add checkpoint with new activity
node .claude/skills/work-command-center/tools/session-state.js checkpoint \
  --activity "Completed deliverables review"

# Or just record a checkpoint timestamp
node .claude/skills/work-command-center/tools/session-state.js checkpoint
```

**When to Use:** After completing major activities during the session (e.g., finishing a deliverable, switching focus areas)

**Updates:** Adds activity to list, records timestamp and duration so far

---

#### Resume Session (Check for Active Session)

```bash
node .claude/skills/work-command-center/tools/session-state.js resume
```

**When to Use:** At the start of every new chat to detect if a session was already in progress

**Output:** JSON with session details if active, or "NO_ACTIVE_SESSION" if none exists

**Example Output:**
```json
{
  "exists": true,
  "session_id": "20251229-0828",
  "project": "Office Building Energy Audit",
  "project_number": "EA-2024-089",
  "start_time": "12/29/2025, 8:28:07 AM",
  "duration_minutes": 45,
  "duration_formatted": "45m",
  "activities_count": 3,
  "activities": ["Energy model QA/QC", "HVAC review", "Report generation"]
}
```

---

#### Show Session Status

```bash
node .claude/skills/work-command-center/tools/session-state.js status
```

**When to Use:** To check current session details during work

**Output:** Human-readable summary of active session including duration, activities, and checkpoints

---

#### Finalize Session

```bash
node .claude/skills/work-command-center/tools/session-state.js finalize \
  --notes "Session summary or additional context"
```

**When to Use:** At the end of every Work Command Center session

**Actions:**
1. Calculates total duration from start to now
2. Creates time log entry with all activities
3. Appends to `time-log.jsonl`
4. Deletes `active-session.json`

**Time Log Entry Format:**
```json
{
  "date": "2025-12-29",
  "session_id": "20251229-0828",
  "project": "Office Building Energy Audit",
  "project_number": "EA-2024-089",
  "start_time": "2025-12-29T15:28:07.438Z",
  "end_time": "2025-12-29T16:13:22.751Z",
  "duration_minutes": 45,
  "activities": ["Energy model QA/QC", "HVAC system review"],
  "notes": "Session summary"
}
```

---

## Manual Time Logging (Legacy)

**Location:** `tools/log-time.js`

**Purpose:** Manual time entry for sessions tracked outside Work Command Center

**Note:** This is now LEGACY - prefer `session-state.js` for automatic tracking

### Logging Time Entries

```bash
node .claude/skills/work-command-center/tools/log-time.js \
  --duration 60 \
  --task "Energy model QA-QC" \
  --project "Office Building Energy Audit" \
  --notes "Optional additional context"
```

**Parameters:**
- `--duration` (required): Time spent in minutes
- `--task` (required): Brief task description
- `--project` (required): Project name or "Internal/Admin" for overhead
- `--notes` (optional): Additional context

**When to Use:** Only for manual time entries outside of Work Command Center sessions (e.g., time spent in meetings, phone calls, or work done without Claude)

---

## Weekly Timesheet Generation

**Location:** `tools/weekly-timesheet.js`

**Purpose:** Generate weekly timesheet summaries from time-log.jsonl for billing and reporting

**Works with:** Both session-state.js entries and legacy log-time.js entries

**Usage:**

```bash
# Current week summary
node .claude/skills/work-command-center/tools/weekly-timesheet.js

# Specific week (Monday date)
node .claude/skills/work-command-center/tools/weekly-timesheet.js --week 2025-12-23

# JSON output for processing
node .claude/skills/work-command-center/tools/weekly-timesheet.js --json
```

**Output:** Groups time entries by project, shows total hours per project, and grand total for the week

---

## Generic Counter System

**Location:**
- Tool: `tools/counter.js`
- Data: `User-Files/work-tracking/counters.json`

**Purpose:** Track any metric over time with simple increment/set/reset operations

**Use Cases:**
- Rescued deadlines (taking over others' work)
- Delegation wins
- Deep work interruptions
- Completed deliverables
- Budget overruns caught proactively

### Usage

```bash
# Increment a counter by 1
node .claude/skills/work-command-center/tools/counter.js rescued-deadlines

# Set a counter to specific value
node .claude/skills/work-command-center/tools/counter.js rescued-deadlines --set 5

# Reset a counter to 0
node .claude/skills/work-command-center/tools/counter.js rescued-deadlines --reset

# List all counters with current values
node .claude/skills/work-command-center/tools/counter.js --list
```

### Common Counter Names

| Counter Name | Purpose | When to Increment |
|-------------|---------|-------------------|
| `rescued-deadlines` | Times Matt took over others' work to meet deadlines | When reassigning deliverable from team member to Matt due to deadline risk |
| `delegation-wins` | Successful delegation instances | When deliverable successfully completed by team member without Matt intervention |
| `interrupted-deep-work` | Deep work sessions interrupted | When focused work session is interrupted by meeting/question/emergency |
| `completed-deliverables` | Weekly completion tracking | When marking deliverable as Complete in tracker |
| `budget-overruns-caught` | Proactive budget issue identification | When identifying project approaching budget limit before overrun |

### Example Workflow

```bash
# User takes over Ali's deliverable to meet Friday deadline
node .claude/skills/work-command-center/tools/counter.js rescued-deadlines

# Check current stats
node .claude/skills/work-command-center/tools/counter.js --list
# Output:
# rescued-deadlines: 3 (last updated: 2025-12-02T16:38:39.193Z)
# delegation-wins:   12 (last updated: 2025-11-29T14:22:15.442Z)
```

---

## Tool Maintenance

### Adding New Tools

When adding new CLI tools to Work Command Center:

1. Create tool in `tools/` directory using Node.js v24+ with ESM
2. Document in this file with clear usage examples
3. Add to SKILL.md if it affects core workflow
4. Consider if tool should be its own skill (if reusable beyond work tracking)

### Tool Best Practices

- Use Node.js (not Python) for cross-platform compatibility
- Provide `--help` flag for self-documentation
- Store data in `User-Files/work-tracking/` for consistency
- Use JSON or JSONL for structured data
- Include error handling and clear error messages
- Make tools idempotent where possible

---

## NPV Analysis Email Generator

**Location:** `scripts/npv_analysis_email_generator.py`

**Documentation:** [`docs/TOOL_NPV_Email_Generator.md`](../../docs/TOOL_NPV_Email_Generator.md)

**Purpose:** Extract NPV and first cost data from lifecycle cost analysis spreadsheets and generate professionally formatted Excel summaries for stakeholder distribution

**Use Cases:**
- Building energy model cost comparisons (HVAC systems, envelope options)
- Equipment lifecycle cost studies
- Design alternative evaluations
- Value engineering analysis
- Deliverables: Excel summary reports for client presentations

### Usage

```bash
# Basic usage - generates Excel summary with auto-generated filename
python scripts/npv_analysis_email_generator.py "path/to/NPV_Analysis.xlsx"

# Custom output filename and project name
python scripts/npv_analysis_email_generator.py "input.xlsx" \
  -o "User-Files/work-tracking/project-name/NPV_Summary.xlsx" \
  -p "Project Name"

# Generate Excel AND email text for stakeholder communication
python scripts/npv_analysis_email_generator.py "input.xlsx" --email
```

### Output Files

**Primary Output:**
- Excel summary with formatted comparison table
- Color-coded cost differences (red=higher, green=lower)
- Highlights recommended option (lowest lifecycle cost)
- Default filename: `[InputFile]_Summary_[timestamp].xlsx`

**Optional Output:**
- Email text with formatted table (use `--email` flag)
- Copy-paste ready for stakeholder communication

### Integration with Deliverables Tracking

**When to Use This Tool:**
1. User mentions NPV, lifecycle cost, or first cost comparisons
2. Working with cost analysis spreadsheets for building projects
3. Need to generate stakeholder-ready cost comparison reports
4. Preparing deliverables for project alternatives analysis

**Deliverable Workflow:**
```markdown
**Deliverable:** NPV Analysis Summary - [Project Name]
**Owner:** Matt
**Deadline:** [Date]
**Status:** In Progress
**Tool:** `python scripts/npv_analysis_email_generator.py "User-Files/work-tracking/[project]/NPV.xlsx" -o "User-Files/work-tracking/[project]/Summary.xlsx" -p "[Project Name]"`
```

### Common Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `input_file` | Path to NPV analysis Excel file | `User-Files/work-tracking/project/NPV.xlsx` |
| `--output, -o` | Custom output Excel path | `User-Files/work-tracking/project/Summary.xlsx` |
| `--project-name, -p` | Project name for headers | `"Recreation Center"` |
| `--email` | Also generate email text | (flag, no value) |

### Spreadsheet Requirements

The input Excel file must have these sheets:
- **Assumptions** - Contains discount rate, term, gross SF, annual energy costs
- **Upfront_Costs** - Contains first costs for each alternative
- **Cashflows_XNPV** - Contains NPV calculations and cashflow projections

See [documentation](../../docs/TOOL_NPV_Email_Generator.md) for detailed structure requirements.

### Python API Integration

For programmatic use within skills or scripts:

```python
from scripts.npv_analysis_email_generator import extract_npv_data, export_summary_excel

# Extract data
data = extract_npv_data('path/to/file.xlsx', project_name='My Project')

# Generate Excel summary
output_file = export_summary_excel(data, 'output_summary.xlsx')

# Access specific values
print(f"Baseline NPV: ${data['npv_data']['Baseline']['npv']:,.0f}")
print(f"Package D First Cost: ${data['first_costs']['Package D']['total']:,.0f}")
```

### Related Skills

- **xlsx skill** - For editing/recalculating the source NPV spreadsheet before running tool
- **energy-efficiency skill** - For energy model cost analysis context
- **diagnosing-energy-models skill** - For HVAC alternative cost comparisons

---

## Markdown to Word Converter

**Location:** `tools/convert-md-to-docx-pypandoc.py`

**Purpose:** Convert markdown files to Word (.docx) format with full table support and formatting preservation

**Key Features:**

- ✅ Full table support (pipe, grid, simple tables)
- ✅ Complex formatting (bold, italic, code blocks)
- ✅ Images and links
- ✅ Auto-installs Pandoc if not available
- ✅ Custom Word templates for styling

**Requirements:**

- Python 3.8+
- pypandoc library: `pip install pypandoc`
- Pandoc (auto-downloaded on first use)

### Basic Usage

```bash
# Basic conversion (output to same directory)
python .claude/skills/work-command-center/tools/convert-md-to-docx-pypandoc.py "meeting-notes.md"

# Custom output location
python .claude/skills/work-command-center/tools/convert-md-to-docx-pypandoc.py "meeting-notes.md" "output/notes.docx"

# With custom Word template for branding
python .claude/skills/work-command-center/tools/convert-md-to-docx-pypandoc.py "report.md" --template "company-template.docx"
```

### Converter Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `input_file` | Markdown file to convert (.md) | `"meeting-agenda.md"` |
| `output_file` | Optional output path (.docx) | `"exports/agenda.docx"` |
| `--template, -t` | Word template for styling | `"--template template.docx"` |
| `--version` | Show version information | (flag, no value) |

### When to Use

**Use this tool when:**

- Converting meeting agendas with tables for client distribution
- Preparing markdown documentation for stakeholders who prefer Word
- Creating deliverables from markdown notes
- Sharing formatted reports with external partners

**Example Workflow:**

```bash
# Create meeting agenda in markdown (with tables)
# Convert to Word for client
python .claude/skills/work-command-center/tools/convert-md-to-docx-pypandoc.py \
  "User-Files/work-tracking/reference-docs/Meeting_Agenda.md"
```

### Integration with Work Command Center

The tool automatically:

1. Checks if Pandoc is installed
2. Downloads Pandoc if needed (first run only)
3. Converts markdown to Word with tables intact
4. Outputs to same directory as input by default

**No manual Pandoc installation required!**
