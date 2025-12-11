#!/usr/bin/env node

/**
 * Markdown to Word Converter
 * Converts .md files to .docx format with proper formatting
 */

import { readFile, writeFile, access, mkdir, readdir, stat } from 'fs/promises';
import { dirname, join, basename, extname, resolve } from 'path';
import { fileURLToPath } from 'url';
import MarkdownIt from 'markdown-it';
import { Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableCell, TableRow, AlignmentType, UnderlineType, BorderStyle } from 'docx';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Parse command line arguments
const args = process.argv.slice(2);

// Configuration
const config = {
  inputFile: null,
  outputDir: null,
  batch: false,
  batchDir: null,
  overwrite: true,
  verbose: false,
};

// Parse arguments
for (let i = 0; i < args.length; i++) {
  const arg = args[i];

  if (arg === '--batch') {
    config.batch = true;
    config.batchDir = args[++i];
  } else if (arg === '--output' || arg === '-o') {
    config.outputDir = args[++i];
  } else if (arg === '--verbose' || arg === '-v') {
    config.verbose = true;
  } else if (arg === '--help' || arg === '-h') {
    showHelp();
    process.exit(0);
  } else if (!config.inputFile && !config.batch) {
    config.inputFile = arg;
  }
}

// Validate arguments
if (!config.batch && !config.inputFile) {
  console.error('Error: No input file specified');
  showHelp();
  process.exit(1);
}

function showHelp() {
  console.log(`
Markdown to Word Converter

USAGE:
  node convert-md-to-docx.js <input-file.md> [options]
  node convert-md-to-docx.js --batch <directory> [options]

OPTIONS:
  -o, --output <dir>    Output directory (defaults to input file's directory)
  --batch <dir>         Convert all .md files in directory
  -v, --verbose         Show detailed output
  -h, --help            Show this help message

EXAMPLES:
  # Convert single file
  node convert-md-to-docx.js "meeting-notes.md"

  # Convert with custom output directory
  node convert-md-to-docx.js "meeting-notes.md" -o "c:\\exports"

  # Batch convert all files in directory
  node convert-md-to-docx.js --batch "c:\\meeting-notes"
`);
}

// Initialize markdown parser
const md = new MarkdownIt({
  html: true,
  linkify: true,
  typographer: true,
});

/**
 * Parse markdown tokens and convert to docx Document structure
 */
function markdownToDocx(markdownText, sourceFileName) {
  const tokens = md.parse(markdownText, {});
  const children = [];

  let currentListLevel = 0;
  let listItemBuffer = [];

  for (let i = 0; i < tokens.length; i++) {
    const token = tokens[i];

    if (token.type === 'heading_open') {
      const level = parseInt(token.tag.replace('h', ''));
      const contentToken = tokens[i + 1];

      children.push(
        new Paragraph({
          text: contentToken.content,
          heading: getHeadingLevel(level),
          spacing: { before: 240, after: 120 },
        })
      );

      i++; // Skip content token
    } else if (token.type === 'paragraph_open') {
      const contentToken = tokens[i + 1];

      if (contentToken && contentToken.children) {
        const runs = parseInlineTokens(contentToken.children);
        children.push(
          new Paragraph({
            children: runs,
            spacing: { before: 120, after: 120 },
          })
        );
      }

      i++; // Skip content token
    } else if (token.type === 'bullet_list_open' || token.type === 'ordered_list_open') {
      currentListLevel++;
      const listItems = extractListItems(tokens, i);

      listItems.forEach(itemText => {
        const runs = parseInlineContent(itemText);
        children.push(
          new Paragraph({
            children: runs,
            bullet: token.type === 'bullet_list_open' ? { level: currentListLevel - 1 } : undefined,
            numbering: token.type === 'ordered_list_open' ? { reference: 'default-numbering', level: currentListLevel - 1 } : undefined,
            spacing: { before: 60, after: 60 },
          })
        );
      });

      // Skip list tokens
      while (i < tokens.length && tokens[i].type !== 'bullet_list_close' && tokens[i].type !== 'ordered_list_close') {
        i++;
      }

      currentListLevel--;
    } else if (token.type === 'fence' || token.type === 'code_block') {
      // Code block
      children.push(
        new Paragraph({
          children: [
            new TextRun({
              text: token.content.trim(),
              font: 'Consolas',
              size: 20,
            }),
          ],
          shading: {
            fill: 'F5F5F5',
          },
          spacing: { before: 120, after: 120 },
        })
      );
    } else if (token.type === 'blockquote_open') {
      const quoteContent = extractBlockquote(tokens, i);
      children.push(
        new Paragraph({
          children: [
            new TextRun({
              text: quoteContent,
              italics: true,
            }),
          ],
          indent: { left: 720 },
          border: {
            left: {
              color: 'CCCCCC',
              space: 1,
              value: BorderStyle.SINGLE,
              size: 6,
            },
          },
          spacing: { before: 120, after: 120 },
        })
      );

      // Skip blockquote tokens
      while (i < tokens.length && tokens[i].type !== 'blockquote_close') {
        i++;
      }
    } else if (token.type === 'hr') {
      children.push(
        new Paragraph({
          children: [
            new TextRun({
              text: '___________________________________________',
              color: 'CCCCCC',
            }),
          ],
          alignment: AlignmentType.CENTER,
          spacing: { before: 120, after: 120 },
        })
      );
    }
  }

  const doc = new Document({
    sections: [{
      properties: {},
      children: children,
    }],
  });

  return doc;
}

function getHeadingLevel(level) {
  const levels = [
    HeadingLevel.HEADING_1,
    HeadingLevel.HEADING_2,
    HeadingLevel.HEADING_3,
    HeadingLevel.HEADING_4,
    HeadingLevel.HEADING_5,
    HeadingLevel.HEADING_6,
  ];
  return levels[level - 1] || HeadingLevel.HEADING_1;
}

function parseInlineTokens(tokens) {
  const runs = [];

  for (const token of tokens) {
    if (token.type === 'text') {
      runs.push(new TextRun({ text: token.content }));
    } else if (token.type === 'strong_open') {
      // Bold - handled by strong_close
    } else if (token.type === 'em_open') {
      // Italic - handled by em_close
    } else if (token.type === 'code_inline') {
      runs.push(
        new TextRun({
          text: token.content,
          font: 'Consolas',
          shading: { fill: 'F5F5F5' },
        })
      );
    } else if (token.type === 'link_open') {
      // Links are complex - simplified for now
    } else if (token.children) {
      runs.push(...parseInlineTokens(token.children));
    }
  }

  return runs;
}

function parseInlineContent(text) {
  // Simple parser for inline formatting
  const runs = [];
  const tokens = md.parseInline(text, {});

  if (tokens[0] && tokens[0].children) {
    return parseInlineTokens(tokens[0].children);
  }

  return [new TextRun({ text: text })];
}

function extractListItems(tokens, startIndex) {
  const items = [];
  let i = startIndex + 1;

  while (i < tokens.length) {
    const token = tokens[i];

    if (token.type === 'list_item_open') {
      // Find the inline content
      let j = i + 1;
      while (j < tokens.length && tokens[j].type !== 'list_item_close') {
        if (tokens[j].type === 'inline') {
          items.push(tokens[j].content);
        }
        j++;
      }
    } else if (token.type === 'bullet_list_close' || token.type === 'ordered_list_close') {
      break;
    }

    i++;
  }

  return items;
}

function extractBlockquote(tokens, startIndex) {
  let content = '';
  let i = startIndex + 1;

  while (i < tokens.length && tokens[i].type !== 'blockquote_close') {
    if (tokens[i].type === 'inline') {
      content += tokens[i].content + ' ';
    }
    i++;
  }

  return content.trim();
}

/**
 * Convert a single markdown file to docx
 */
async function convertFile(inputPath, outputPath) {
  try {
    if (config.verbose) {
      console.log(`Reading: ${inputPath}`);
    }

    // Read markdown file
    const markdownContent = await readFile(inputPath, 'utf-8');

    // Convert to docx
    const doc = markdownToDocx(markdownContent, basename(inputPath));

    // Generate buffer
    const buffer = await Packer.toBuffer(doc);

    // Ensure output directory exists
    await mkdir(dirname(outputPath), { recursive: true });

    // Write file
    await writeFile(outputPath, buffer);

    console.log(`✓ Converted: ${basename(inputPath)} → ${basename(outputPath)}`);

    return true;
  } catch (error) {
    console.error(`✗ Error converting ${basename(inputPath)}:`, error.message);
    return false;
  }
}

/**
 * Batch convert all markdown files in a directory
 */
async function batchConvert(dirPath, outputDir) {
  try {
    const files = await readdir(dirPath);
    const mdFiles = files.filter(f => extname(f).toLowerCase() === '.md');

    if (mdFiles.length === 0) {
      console.log(`No markdown files found in ${dirPath}`);
      return;
    }

    console.log(`Found ${mdFiles.length} markdown file(s)\n`);

    let successCount = 0;
    let failCount = 0;

    for (const file of mdFiles) {
      const inputPath = join(dirPath, file);
      const outputFileName = basename(file, '.md') + '.docx';
      const outputPath = join(outputDir || dirPath, outputFileName);

      const success = await convertFile(inputPath, outputPath);

      if (success) {
        successCount++;
      } else {
        failCount++;
      }
    }

    console.log(`\nCompleted: ${successCount} successful, ${failCount} failed`);

  } catch (error) {
    console.error('Error during batch conversion:', error.message);
    process.exit(1);
  }
}

/**
 * Main execution
 */
async function main() {
  try {
    if (config.batch) {
      // Batch mode
      const batchPath = resolve(config.batchDir);
      const outputPath = config.outputDir ? resolve(config.outputDir) : batchPath;

      await batchConvert(batchPath, outputPath);
    } else {
      // Single file mode
      const inputPath = resolve(config.inputFile);
      const outputFileName = basename(inputPath, '.md') + '.docx';
      const outputPath = config.outputDir
        ? join(resolve(config.outputDir), outputFileName)
        : join(dirname(inputPath), outputFileName);

      await convertFile(inputPath, outputPath);
    }
  } catch (error) {
    console.error('Fatal error:', error.message);
    if (config.verbose) {
      console.error(error.stack);
    }
    process.exit(1);
  }
}

// Run
main();
