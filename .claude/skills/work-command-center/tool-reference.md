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

## Time Tracking System

**Location:**
- Data: `User-Files/work-tracking/time-log.jsonl`
- Logger: `tools/log-time.js`
- Reporter: `tools/weekly-timesheet.js`

**Purpose:** Track time spent on tasks and generate weekly timesheet summaries for billing

**Data Format:** JSONL with entries: `{date, time, session_start, duration_minutes, task, project, notes}`

### Logging Time Entries

```bash
node .claude/skills/work-command-center/tools/log-time.js \
  --duration 60 \
  --task "SECC energy model QA-QC" \
  --project "Fort Collins SECC" \
  --notes "Optional additional context"
```

**Parameters:**
- `--duration` (required): Time spent in minutes
- `--task` (required): Brief task description
- `--project` (required): Project name or "Internal/Admin" for overhead
- `--notes` (optional): Additional context

### Generating Weekly Timesheets

```bash
# Current week summary
node .claude/skills/work-command-center/tools/weekly-timesheet.js

# Specific week (Monday date)
node .claude/skills/work-command-center/tools/weekly-timesheet.js --week 2025-11-18

# JSON output for processing
node .claude/skills/work-command-center/tools/weekly-timesheet.js --json
```

### Session End Protocol

At the end of EVERY Work Command Center session:

1. Estimate session duration in minutes
2. Identify primary task/activity
3. Assign to project (or "Internal/Admin" for overhead)
4. Run `log-time.js` with appropriate parameters
5. This ensures accurate weekly timesheet generation

**Example:**

```bash
node .claude/skills/work-command-center/tools/log-time.js \
  --duration 15 \
  --task "Daily standup and priority coaching" \
  --project "Internal/Admin"
```

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

**Documentation:** [`docs/TOOL_SECC_NPV_Email_Generator.md`](../../docs/TOOL_SECC_NPV_Email_Generator.md)

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
| `input_file` | Path to NPV analysis Excel file | `User-Files/work-tracking/secc/NPV.xlsx` |
| `--output, -o` | Custom output Excel path | `User-Files/work-tracking/secc/Summary.xlsx` |
| `--project-name, -p` | Project name for headers | `"SECC Recreation Center"` |
| `--email` | Also generate email text | (flag, no value) |

### Spreadsheet Requirements

The input Excel file must have these sheets:
- **Assumptions** - Contains discount rate, term, gross SF, annual energy costs
- **Upfront_Costs** - Contains first costs for each alternative
- **Cashflows_XNPV** - Contains NPV calculations and cashflow projections

See [documentation](../../docs/TOOL_SECC_NPV_Email_Generator.md) for detailed structure requirements.

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
