# Iterative Feedback System for Template Corrections

## Overview

The feedback system learns from your manual corrections and automatically applies them in future conversions. This creates a continuous improvement loop where each proposal conversion gets better.

## How It Works

```
┌─────────────────┐
│ Convert Proposal│
│   to Word      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Manual Review  │
│ & Corrections  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Provide Feedback│
│ on Corrections │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ System Analyzes │
│ if Automatable │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Future Converts │
│ Apply Learned  │
│  Corrections   │
└─────────────────┘
```

## Quick Start

### 1. Convert with Feedback Enabled

```bash
python tools/convert-proposal-to-docx.py proposal.md --feedback
```

This will:
1. Convert the markdown to Word
2. Wait for you to review the document
3. Collect feedback on manual corrections needed
4. Store automatable corrections for future use

### 2. Or Provide Feedback Later

```bash
# Convert without feedback
python tools/convert-proposal-to-docx.py proposal.md

# Later, after reviewing the document
python tools/collect-feedback.py output.docx
```

### 3. Check Template Status

See what corrections have been learned for a template:

```bash
python tools/collect-feedback.py --status proposal-template.docx
```

## What Gets Automated?

The system can automatically fix:

| Issue Type | Example | Automated? |
|------------|---------|------------|
| **Style corrections** | "Normal" → "Body Text" | ✓ Yes |
| **List styles** | Bullets need "Body List" style | ✓ Yes |
| **Find/replace** | "Icon Energy" → "Iconergy" | ✓ Yes |
| **Spacing issues** | Paragraphs too close together | ✓ Yes |
| **Table formatting** | Tables need different style | ✓ Yes |
| **Header/footer** | Template-specific elements | ✗ No (requires template update) |
| **Images** | Logo placement | ✗ No (manual) |
| **Content edits** | Wording changes | ✗ No (requires judgment) |

## Template-Specific Learning

Corrections are stored **per template** in `template-corrections.json`:

```json
{
  "proposal-template.docx": {
    "style_corrections": {
      "Normal": "Body Text",
      "List Paragraph": "Body List"
    },
    "find_replace": [
      {
        "find": "Icon Energy",
        "replace": "Iconergy",
        "reason": "Company name consistency"
      }
    ],
    "formatting_fixes": [
      {
        "issue": "Table borders too thick",
        "fix": "Apply Table Grid Light style",
        "automated": true
      }
    ],
    "manual_steps_remaining": [
      "Verify contact info on cover page"
    ]
  }
}
```

## Example Workflow

### First Time: Mytikas Proposal

```bash
# Convert proposal
python tools/convert-proposal-to-docx.py Mytikas.md --feedback

# Tool outputs:
#   ✓ Conversion complete
#   >> Press Enter when you're ready to provide feedback...

# [You review the Word doc and notice:]
#   - Had to change "Normal" style to "Body Text" in 50 places
#   - Had to fix bullet point spacing
#   - Had to manually update contact info on cover page

# [You provide feedback:]
#   1. Normal style should be Body Text
#   2. Bullet points need more spacing
#   3. Cover page contact info needs updating

# Tool analyzes:
#   ✓ CAN AUTOMATE: Add to style_corrections mapping
#   ✓ CAN AUTOMATE: Can automate with paragraph formatting
#   ✗ REQUIRES MANUAL: Template-specific - may need template update
```

### Second Time: Next Proposal

```bash
# Convert another proposal
python tools/convert-proposal-to-docx.py NextProposal.md

# Tool outputs:
#   Found 2 automated corrections for this template
#   Style remapping complete:
#     - Normal -> Body Text: 50 paragraphs
#     - Bullets remapped: 32 items
#   Learned corrections applied:
#     - Style corrections: 5

# [You review the Word doc:]
#   ✓ Normal → Body Text: ALREADY DONE!
#   ✓ Bullet spacing: ALREADY FIXED!
#   - Cover page contact: Still need to update manually
```

Much better! Only one manual step instead of three.

## Feedback Collection Interface

### Interactive Mode (Default)

```
CONVERSION FEEDBACK COLLECTION
======================================================================
Document: Mytikas_Proposal.docx
Template: proposal-template.docx
======================================================================

What manual corrections did you need to make? (Enter one per line)
Type 'done' when finished, or 'skip' to skip feedback.

  1. Changed Normal style to Body Text in all body paragraphs
  2. Fixed bullet point spacing
  3. Updated contact info on cover page
  4. done

ANALYZING CORRECTIONS FOR AUTOMATION
======================================================================

[1] Changed Normal style to Body Text in all body paragraphs
    ✓ CAN AUTOMATE: Add to style_corrections mapping

[2] Fixed bullet point spacing
    ✓ CAN AUTOMATE: Can automate with paragraph formatting

[3] Updated contact info on cover page
    ✗ REQUIRES MANUAL: Template-specific - may need template update

✓ Added 2 issues for automation
✓ Added 1 manual steps to tracking
```

### Batch Mode

Create a text file with corrections (one per line):

```
# corrections.txt
Changed Normal style to Body Text
Fixed bullet spacing
Updated contact info
```

Then run:

```bash
python tools/collect-feedback.py output.docx --batch corrections.txt
```

## Viewing Current Status

See what's been learned for a template:

```bash
python tools/collect-feedback.py --status proposal-template.docx
```

Output:
```
TEMPLATE CORRECTIONS STATUS: proposal-template.docx
======================================================================

✓ Style Corrections (AUTOMATED):
    Normal -> Body Text
    List Paragraph -> Body List

✓ Find/Replace Rules (AUTOMATED):
    'Icon Energy' -> 'Iconergy'

✓ Formatting Fixes (AUTOMATED):
    Normal style used instead of Body Text

⚠ Formatting Fixes (PENDING AUTOMATION):
    Table borders need adjustment
      -> Can automate with table styling

✗ Manual Steps (NOT AUTOMATABLE):
    Verify contact info on cover page
    Update project-specific images
```

## Advanced Usage

### Add Custom Corrections Manually

Edit `template-corrections.json` directly:

```json
{
  "proposal-template.docx": {
    "find_replace": [
      {
        "find": "CITCO",
        "replace": "Colorado Industrial Tax Credit Offering (CITCO)",
        "reason": "Spell out acronym on first use"
      }
    ]
  }
}
```

### Multiple Templates

The system tracks corrections separately for each template:

```json
{
  "proposal-template.docx": { ... },
  "audit-template.docx": { ... },
  "custom-template.docx": { ... }
}
```

Each template learns independently based on its specific requirements.

## Tips for Effective Feedback

### Be Specific

**Bad:**
```
"Formatting was wrong"
```

**Good:**
```
"Normal style paragraphs should use Body Text style"
"Bullet points need Body List style instead of List Paragraph"
```

### One Issue Per Line

**Bad:**
```
"Fixed styles, spacing, and tables"
```

**Good:**
```
"Changed Normal to Body Text"
"Fixed paragraph spacing after headings"
"Applied Table Grid Light to all tables"
```

### Distinguish Automation vs. Manual

**Automatable:**
- Style changes
- Find/replace text
- Spacing adjustments
- Table formatting

**Manual (template-specific):**
- Contact info updates
- Project-specific images
- Client-specific branding
- Cover page layout changes

## Benefits

### 1. Continuous Improvement
Each conversion teaches the system, making future conversions better.

### 2. Template-Specific Learning
Corrections apply only to the relevant template, so you don't get unwanted changes.

### 3. Transparency
Always see what corrections are being applied:
```
Learned corrections applied:
  - Style corrections: 50
  - Find/replace: 3
```

### 4. Reduced Manual Work
Over time, fewer manual corrections needed:
- **First proposal:** 20 minutes of manual fixes
- **Fifth proposal:** 5 minutes of manual fixes
- **Tenth proposal:** 2 minutes of manual fixes

## Troubleshooting

### Feedback Not Being Applied

Check template corrections status:
```bash
python tools/collect-feedback.py --status proposal-template.docx
```

Look for issues marked "PENDING AUTOMATION" - these need tool updates to implement.

### Wrong Corrections Applied

Edit `template-corrections.json` and remove the incorrect rule.

### Feedback Script Not Found

Make sure you're running from the skill directory:
```bash
cd .claude/skills/writing-proposals
python tools/collect-feedback.py output.docx
```

## Files

- **`template-corrections.json`** - Database of learned corrections per template
- **`collect-feedback.py`** - Interactive feedback collection tool
- **`convert-proposal-to-docx.py`** - Main conversion tool (now loads and applies corrections)

## Summary

The feedback system creates a **virtuous cycle** where:

1. You convert a proposal
2. Note what manual fixes were needed
3. System learns which can be automated
4. Future conversions automatically apply those fixes
5. Repeat with new corrections

**Result:** Each proposal gets easier to produce, with less manual cleanup required.

---

**Next Steps:**

1. Convert your next proposal with `--feedback` flag
2. Provide detailed feedback on manual corrections
3. Watch as future conversions get progressively cleaner
4. Enjoy the time saved! ⏱️
