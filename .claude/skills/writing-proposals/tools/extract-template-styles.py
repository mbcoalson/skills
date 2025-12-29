#!/usr/bin/env python3
"""
Extract and document all styles from a Word template.

This utility reads a Word document template and exports:
- All available paragraph styles
- All available character styles
- Font properties (name, size, bold, italic, color)
- Paragraph properties (alignment, spacing, indentation)
- Style inheritance information

This helps ensure proposal conversions use the exact template styles.

Usage:
    python extract-template-styles.py template.docx
    python extract-template-styles.py template.docx --output styles.txt
"""

import sys
import argparse
from pathlib import Path

try:
    from docx import Document
    from docx.shared import Pt, RGBColor
    from docx.enum.style import WD_STYLE_TYPE
except ImportError:
    print("Error: python-docx is not installed")
    print("Install with: pip install python-docx")
    sys.exit(1)


def rgb_to_hex(rgb_color):
    """Convert RGBColor to hex string."""
    if rgb_color is None:
        return "None"
    try:
        return f"#{rgb_color[0]:02x}{rgb_color[1]:02x}{rgb_color[2]:02x}"
    except:
        return "Auto"


def pt_to_string(pt_value):
    """Convert Pt value to readable string."""
    if pt_value is None:
        return "None"
    try:
        return f"{pt_value.pt}pt"
    except:
        return str(pt_value)


def extract_paragraph_style_info(style):
    """Extract detailed information about a paragraph style."""
    info = {
        'name': style.name,
        'type': 'Paragraph',
        'base_style': style.base_style.name if style.base_style else None,
        'font_name': None,
        'font_size': None,
        'bold': None,
        'italic': None,
        'color': None,
        'alignment': None,
        'space_before': None,
        'space_after': None,
        'line_spacing': None,
        'left_indent': None,
        'right_indent': None,
        'first_line_indent': None,
    }

    # Font properties
    if style.font:
        info['font_name'] = style.font.name
        info['font_size'] = pt_to_string(style.font.size)
        info['bold'] = style.font.bold
        info['italic'] = style.font.italic
        info['color'] = rgb_to_hex(style.font.color.rgb) if style.font.color else None

    # Paragraph properties
    if style.paragraph_format:
        pf = style.paragraph_format
        info['alignment'] = str(pf.alignment) if pf.alignment else None
        info['space_before'] = pt_to_string(pf.space_before)
        info['space_after'] = pt_to_string(pf.space_after)
        info['line_spacing'] = str(pf.line_spacing) if pf.line_spacing else None
        info['left_indent'] = pt_to_string(pf.left_indent)
        info['right_indent'] = pt_to_string(pf.right_indent)
        info['first_line_indent'] = pt_to_string(pf.first_line_indent)

    return info


def extract_character_style_info(style):
    """Extract detailed information about a character style."""
    info = {
        'name': style.name,
        'type': 'Character',
        'base_style': style.base_style.name if style.base_style else None,
        'font_name': None,
        'font_size': None,
        'bold': None,
        'italic': None,
        'color': None,
    }

    # Font properties
    if style.font:
        info['font_name'] = style.font.name
        info['font_size'] = pt_to_string(style.font.size)
        info['bold'] = style.font.bold
        info['italic'] = style.font.italic
        info['color'] = rgb_to_hex(style.font.color.rgb) if style.font.color else None

    return info


def format_style_info(info):
    """Format style information as readable text."""
    lines = []
    lines.append(f"Style: {info['name']}")
    lines.append(f"  Type: {info['type']}")

    if info.get('base_style'):
        lines.append(f"  Base Style: {info['base_style']}")

    # Font properties
    if info.get('font_name'):
        lines.append(f"  Font: {info['font_name']}")
    if info.get('font_size'):
        lines.append(f"  Size: {info['font_size']}")
    if info.get('bold') is not None:
        lines.append(f"  Bold: {info['bold']}")
    if info.get('italic') is not None:
        lines.append(f"  Italic: {info['italic']}")
    if info.get('color'):
        lines.append(f"  Color: {info['color']}")

    # Paragraph properties (if applicable)
    if info['type'] == 'Paragraph':
        if info.get('alignment'):
            lines.append(f"  Alignment: {info['alignment']}")
        if info.get('space_before') and info['space_before'] != 'None':
            lines.append(f"  Space Before: {info['space_before']}")
        if info.get('space_after') and info['space_after'] != 'None':
            lines.append(f"  Space After: {info['space_after']}")
        if info.get('line_spacing'):
            lines.append(f"  Line Spacing: {info['line_spacing']}")
        if info.get('left_indent') and info['left_indent'] != 'None':
            lines.append(f"  Left Indent: {info['left_indent']}")
        if info.get('first_line_indent') and info['first_line_indent'] != 'None':
            lines.append(f"  First Line Indent: {info['first_line_indent']}")

    return '\n'.join(lines)


def extract_template_styles(template_path, output_path=None):
    """
    Extract all styles from a Word template and output detailed information.

    Args:
        template_path (Path): Path to template file
        output_path (Path, optional): Path to output text file

    Returns:
        bool: True if successful
    """
    try:
        doc = Document(str(template_path))

        output_lines = []
        output_lines.append("=" * 80)
        output_lines.append(f"WORD TEMPLATE STYLE ANALYSIS")
        output_lines.append(f"Template: {template_path.name}")
        output_lines.append("=" * 80)
        output_lines.append("")

        # Organize styles by type
        paragraph_styles = []
        character_styles = []
        other_styles = []

        for style in doc.styles:
            try:
                if style.type == WD_STYLE_TYPE.PARAGRAPH:
                    paragraph_styles.append(extract_paragraph_style_info(style))
                elif style.type == WD_STYLE_TYPE.CHARACTER:
                    character_styles.append(extract_character_style_info(style))
                else:
                    other_styles.append({'name': style.name, 'type': str(style.type)})
            except Exception as e:
                print(f"[WARNING] Could not process style '{style.name}': {e}")

        # Output paragraph styles
        output_lines.append(f"PARAGRAPH STYLES ({len(paragraph_styles)} total)")
        output_lines.append("=" * 80)
        output_lines.append("")

        for style_info in sorted(paragraph_styles, key=lambda x: x['name']):
            output_lines.append(format_style_info(style_info))
            output_lines.append("")

        # Output character styles
        output_lines.append("")
        output_lines.append(f"CHARACTER STYLES ({len(character_styles)} total)")
        output_lines.append("=" * 80)
        output_lines.append("")

        for style_info in sorted(character_styles, key=lambda x: x['name']):
            output_lines.append(format_style_info(style_info))
            output_lines.append("")

        # Output other styles if any
        if other_styles:
            output_lines.append("")
            output_lines.append(f"OTHER STYLES ({len(other_styles)} total)")
            output_lines.append("=" * 80)
            output_lines.append("")
            for style in sorted(other_styles, key=lambda x: x['name']):
                output_lines.append(f"Style: {style['name']} (Type: {style['type']})")

        # Summary
        output_lines.append("")
        output_lines.append("=" * 80)
        output_lines.append("SUMMARY")
        output_lines.append("=" * 80)
        output_lines.append(f"Total Paragraph Styles: {len(paragraph_styles)}")
        output_lines.append(f"Total Character Styles: {len(character_styles)}")
        output_lines.append(f"Total Other Styles: {len(other_styles)}")
        output_lines.append("")

        # Key styles for proposals
        output_lines.append("KEY STYLES FOR PROPOSALS:")
        key_style_names = [
            'Normal', 'Body Text', 'Body Text 2', 'Body Text 3',
            'Heading 1', 'Heading 2', 'Heading 3', 'Heading 4',
            'Title', 'Subtitle', 'List Paragraph', 'Quote'
        ]

        for style_name in key_style_names:
            found = next((s for s in paragraph_styles if s['name'] == style_name), None)
            if found:
                output_lines.append(f"  ✓ {style_name}")
            else:
                output_lines.append(f"  ✗ {style_name} (not found)")

        output_lines.append("")
        output_lines.append("=" * 80)

        # Output to file or console
        output_text = '\n'.join(output_lines)

        if output_path:
            output_path.write_text(output_text, encoding='utf-8')
            print(f"[OK] Style analysis written to: {output_path}")
            print(f"     {len(paragraph_styles)} paragraph styles")
            print(f"     {len(character_styles)} character styles")
        else:
            print(output_text)

        return True

    except Exception as e:
        print(f"[ERROR] Failed to extract styles: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Extract and document styles from Word template',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s template.docx
  %(prog)s template.docx --output template-styles.txt
  %(prog)s proposal-template.docx -o styles-analysis.txt

This tool helps ensure proposal conversions use exact template styles.
        """
    )

    parser.add_argument(
        'template_file',
        help='Word template file (.docx)'
    )

    parser.add_argument(
        '--output', '-o',
        dest='output_file',
        help='Output file for style analysis (default: print to console)'
    )

    args = parser.parse_args()

    # Validate template file
    template_path = Path(args.template_file)
    if not template_path.exists():
        print(f"[ERROR] Template file not found: {args.template_file}")
        sys.exit(1)

    # Determine output path
    output_path = None
    if args.output_file:
        output_path = Path(args.output_file)

    # Extract styles
    success = extract_template_styles(template_path, output_path)

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
