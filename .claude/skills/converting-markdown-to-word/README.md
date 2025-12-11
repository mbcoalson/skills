# Converting Markdown to Word

A Claude Code skill for converting Markdown (.md) files to Microsoft Word (.docx) format. Perfect for sharing meeting notes, documentation, and reports with colleagues who prefer Word.

## Quick Start

### Installation

1. Navigate to the skill directory:
```bash
cd "c:\Users\mcoalson\Documents\WorkPath\Claude-Skills\converting-markdown-to-word"
```

2. Install dependencies:
```bash
npm install
```

3. Verify installation:
```bash
npm test
```

## Usage

### Convert a Single File

```bash
node scripts/convert-md-to-docx.js "path/to/file.md"
```

**Example:**
```bash
node scripts/convert-md-to-docx.js "c:\Users\mcoalson\Documents\WorkPath\User-Files\work-tracking\secc-fort-collins\meeting-notes\2025-11-18_Zone_Mapping_Analysis.md"
```

**Output:** Creates `2025-11-18_Zone_Mapping_Analysis.docx` in the same directory.

### Convert with Custom Output Directory

```bash
node scripts/convert-md-to-docx.js "input.md" --output "c:\exports"
```

**Example:**
```bash
node scripts/convert-md-to-docx.js "meeting-notes.md" -o "c:\Users\mcoalson\Documents\Word-Exports"
```

### Batch Convert All Files in a Directory

```bash
node scripts/convert-md-to-docx.js --batch "path/to/directory"
```

**Example:**
```bash
node scripts/convert-md-to-docx.js --batch "c:\Users\mcoalson\Documents\WorkPath\User-Files\work-tracking\secc-fort-collins\meeting-notes"
```

**Output:** Converts all .md files in the directory to .docx in the same location.

### Batch Convert with Custom Output

```bash
node scripts/convert-md-to-docx.js --batch "path/to/input" --output "path/to/output"
```

### Verbose Mode

```bash
node scripts/convert-md-to-docx.js "file.md" --verbose
```

Shows detailed progress and debugging information.

## Supported Markdown Features

The converter handles all standard Markdown syntax:

- ✅ **Headings** (H1-H6) → Word Heading styles
- ✅ **Bold** (`**text**`) → Word bold formatting
- ✅ **Italic** (`*text*`) → Word italic formatting
- ✅ **Lists** (ordered and unordered) → Word list styles
- ✅ **Code blocks** → Monospace font with gray background
- ✅ **Inline code** → Monospace with light gray background
- ✅ **Blockquotes** → Indented with left border
- ✅ **Horizontal rules** → Centered separator line
- ✅ **Links** → Word hyperlinks (basic support)
- ⚠️ **Images** → Referenced (not embedded yet)
- ⚠️ **Tables** → Converted to paragraphs (full table support coming)

## Command-Line Options

| Option | Short | Description |
|--------|-------|-------------|
| `--batch <dir>` | | Convert all .md files in directory |
| `--output <dir>` | `-o` | Specify output directory |
| `--verbose` | `-v` | Show detailed output |
| `--help` | `-h` | Show help message |

## Examples

### Example 1: Convert Meeting Notes

```bash
# Convert today's meeting notes
node scripts/convert-md-to-docx.js "c:\Users\mcoalson\Documents\WorkPath\User-Files\work-tracking\secc-fort-collins\meeting-notes\2025-11-18_Zone_Mapping_Analysis.md"
```

### Example 2: Export All Meeting Notes for a Project

```bash
# Convert all meeting notes to a shared folder
node scripts/convert-md-to-docx.js --batch "c:\Users\mcoalson\Documents\WorkPath\User-Files\work-tracking\secc-fort-collins\meeting-notes" --output "c:\SharePoint\SECC-FortCollins\MeetingNotes"
```

### Example 3: Daily Standup Logs

```bash
# Convert this week's standup logs
node scripts/convert-md-to-docx.js --batch "c:\Users\mcoalson\Documents\WorkPath\User-Files\work-tracking\daily-logs"
```

### Example 4: Deliverables Report

```bash
# Convert deliverables tracker for client
node scripts/convert-md-to-docx.js "c:\Users\mcoalson\Documents\WorkPath\User-Files\work-tracking\deliverables.md" -o "c:\Reports"
```

## Integration with work-command-center

When using the work-command-center skill, you can ask:

- "Convert my meeting notes to Word"
- "Export the deliverables tracker as a Word file"
- "Convert all daily logs to Word documents"

The work-command-center will automatically delegate to this skill.

## File Naming

- **Single file:** Output matches input name with `.docx` extension
  - Input: `meeting-notes.md` → Output: `meeting-notes.docx`

- **Batch mode:** Each file converted individually with same naming pattern
  - Input: `notes-1.md`, `notes-2.md` → Output: `notes-1.docx`, `notes-2.docx`

- **Existing files:** By default, existing .docx files are overwritten

## Troubleshooting

### "Cannot find module 'docx'" or "Cannot find module 'markdown-it'"

**Solution:** Install dependencies:
```bash
cd "c:\Users\mcoalson\Documents\WorkPath\Claude-Skills\converting-markdown-to-word"
npm install
```

### "ENOENT: no such file or directory"

**Solution:** Verify the file path exists and use absolute paths:
```bash
node scripts/convert-md-to-docx.js "c:\full\path\to\file.md"
```

### "Permission denied"

**Solution:** Check file permissions and ensure the output directory is writable.

### Formatting looks wrong in Word

**Considerations:**
- Ensure you're using standard CommonMark markdown syntax
- Complex nested formatting may not convert perfectly
- Custom HTML in markdown is not currently supported

## Technical Details

### Dependencies

- **docx** (v8.5.0+) - Generates Word documents
- **markdown-it** (v14.1.0+) - Parses markdown syntax

### Requirements

- Node.js v18.0.0 or higher
- Windows, macOS, or Linux

### Output Format

- **File format:** Office Open XML (.docx)
- **Compatible with:** Microsoft Word 2007+, Google Docs, LibreOffice Writer
- **Encoding:** UTF-8

## Future Enhancements

Planned features:

- ✨ Full table support with proper formatting
- ✨ Image embedding (not just references)
- ✨ Custom Word templates/styles
- ✨ Front-matter metadata → Document properties
- ✨ Table of contents generation
- ✨ PDF export option
- ✨ Direct email/SharePoint upload

## Contributing

This is a personal Claude Code skill. To modify:

1. Edit [SKILL.md](SKILL.md) for skill behavior
2. Edit [scripts/convert-md-to-docx.js](scripts/convert-md-to-docx.js) for conversion logic
3. Update this README for documentation changes

## License

MIT

---

**Last Updated:** 2025-11-17
**Version:** 1.0.0
**Maintained by:** Matt Coalson
