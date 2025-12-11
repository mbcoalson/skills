---
name: converting-markdown-to-word
description: Converting Markdown (.md) files to Microsoft Word (.docx) format for sharing with colleagues. Use when the user needs to convert meeting notes, documentation, or any markdown files into Word documents. Supports single file conversion or batch conversion of multiple files.
---

# Converting Markdown to Word

This skill provides tools to convert Markdown files into Microsoft Word (.docx) format, perfect for sharing documentation with colleagues who prefer Word over Markdown.

## Core Capabilities

1. **Single File Conversion** - Convert one markdown file to Word
2. **Batch Conversion** - Convert entire directories of markdown files
3. **Preserve Formatting** - Maintains headings, lists, tables, code blocks, and links
4. **Customizable Output** - Control output directory and naming conventions

## Quick Actions

### Convert Single File
"Convert [filename.md] to Word"
- Converts specified markdown file to .docx
- Outputs to same directory by default
- Preserves all markdown formatting

### Convert Directory
"Convert all markdown files in [directory] to Word"
- Batch processes all .md files in directory
- Maintains folder structure
- Skips already-converted files (optional)

### Convert with Custom Output
"Convert [filename.md] to Word and save to [directory]"
- Converts to specified output location
- Useful for organizing exports separately

## Implementation

The conversion uses Node.js with the `mammoth` or `docx` npm package to generate properly formatted Word documents. The script is located at:

`c:\Users\mcoalson\Documents\WorkPath\Claude-Skills\converting-markdown-to-word\scripts\convert-md-to-docx.js`

## Usage Examples

### Example 1: Convert Meeting Notes
```bash
node scripts/convert-md-to-docx.js "c:\Users\mcoalson\Documents\WorkPath\User-Files\work-tracking\secc-fort-collins\meeting-notes\2025-11-18_Zone_Mapping_Analysis.md"
```

### Example 2: Convert All Files in Directory
```bash
node scripts/convert-md-to-docx.js --batch "c:\Users\mcoalson\Documents\WorkPath\User-Files\work-tracking\secc-fort-collins\meeting-notes"
```

### Example 3: Convert with Custom Output Directory
```bash
node scripts/convert-md-to-docx.js "input.md" --output "c:\Users\mcoalson\Documents\Word-Exports"
```

## Supported Markdown Features

- **Headings** (H1-H6) → Word heading styles
- **Bold/Italic** → Word text formatting
- **Lists** (ordered/unordered) → Word list styles
- **Tables** → Word tables
- **Code blocks** → Word code style (monospace, shaded)
- **Links** → Word hyperlinks
- **Images** → Embedded images (if paths are accessible)
- **Blockquotes** → Word quote style

## File Organization

```
converting-markdown-to-word/
├── SKILL.md                          (this file)
├── README.md                         (detailed documentation)
├── package.json                      (Node.js dependencies)
└── scripts/
    ├── convert-md-to-docx.js         (main conversion script)
    └── batch-convert.js              (batch processing utility)
```

## Dependencies

- **Node.js** v18+ required
- **markdown-it** - Parse markdown
- **docx** - Generate Word documents
- **fs/promises** - File system operations
- **path** - Path manipulation

## Installation

Navigate to the skill directory and install dependencies:

```bash
cd "c:\Users\mcoalson\Documents\WorkPath\Claude-Skills\converting-markdown-to-word"
npm install
```

## Integration with work-command-center

The work-command-center can delegate markdown-to-Word conversions to this skill when users need to:
- Share meeting notes with team members
- Export deliverables documentation
- Create Word versions of daily logs
- Prepare reports for clients who prefer Word

## Error Handling

The script handles common issues:
- **File not found** - Clear error message with path
- **Invalid markdown** - Converts what it can, warns about issues
- **Permission errors** - Notifies user of access problems
- **Missing dependencies** - Prompts to run `npm install`

## Future Enhancements

Potential additions:
- Custom Word templates/styles
- Front-matter metadata → Word document properties
- Table of contents generation
- PDF export option
- Email integration for direct sharing
- Cloud storage upload (OneDrive, SharePoint)

## Notes

- Output files are named `[original-name].docx` by default
- Existing .docx files are overwritten (with confirmation prompt)
- Relative image paths in markdown should be updated or images placed relatively
- For best results, use standard markdown syntax (CommonMark spec)
