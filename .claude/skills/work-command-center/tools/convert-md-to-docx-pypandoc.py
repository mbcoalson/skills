#!/usr/bin/env python3
"""
Convert Markdown to Word (.docx) using pypandoc

This script uses pypandoc (Python wrapper for Pandoc) to convert markdown
files to Word documents with full table support and formatting preservation.

Features:
- Full table support (simple, grid, pipe tables)
- Complex formatting preservation
- Images and links
- Code blocks
- Custom Word templates

Requirements:
- pypandoc: pip install pypandoc
- Pandoc will be auto-downloaded if not installed

Usage:
    python convert-md-to-docx-pypandoc.py input.md
    python convert-md-to-docx-pypandoc.py input.md output.docx
    python convert-md-to-docx-pypandoc.py input.md --template template.docx
"""

import sys
import os
import argparse
from pathlib import Path

try:
    import pypandoc
except ImportError:
    print("Error: pypandoc is not installed")
    print("Install with: pip install pypandoc")
    sys.exit(1)


def setup_pandoc():
    """
    Ensure Pandoc is installed. If not, download it automatically.
    """
    try:
        # Check if pandoc is available
        pypandoc.get_pandoc_version()
        return True
    except OSError:
        print("Pandoc not found. Downloading Pandoc...")
        try:
            pypandoc.download_pandoc()
            print("[OK] Pandoc downloaded successfully")
            return True
        except Exception as e:
            print(f"[ERROR] Error downloading Pandoc: {e}")
            print("\nManual installation:")
            print("  1. Visit: https://pandoc.org/installing.html")
            print("  2. Or use: pip install pypandoc")
            return False


def convert_markdown_to_word(input_file, output_file=None, reference_doc=None):
    """
    Convert markdown file to Word document.

    Args:
        input_file (str): Path to input markdown file
        output_file (str, optional): Path to output Word file
        reference_doc (str, optional): Path to Word template for styling

    Returns:
        bool: True if successful, False otherwise
    """
    # Validate input file
    input_path = Path(input_file)
    if not input_path.exists():
        print(f"[ERROR] Input file not found: {input_file}")
        return False

    # Determine output file
    if output_file is None:
        output_path = input_path.with_suffix('.docx')
    else:
        output_path = Path(output_file)
        # Create output directory if it doesn't exist
        output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Converting: {input_path.name}")
    print(f"Output: {output_path}")

    # Prepare conversion options
    extra_args = []
    if reference_doc and Path(reference_doc).exists():
        extra_args.append(f'--reference-doc={reference_doc}')
        print(f"Using template: {reference_doc}")

    try:
        # Convert using pypandoc
        pypandoc.convert_file(
            str(input_path),
            'docx',
            outputfile=str(output_path),
            extra_args=extra_args
        )

        print(f"[OK] Converted successfully!")
        print(f"Output: {output_path.absolute()}")
        return True

    except RuntimeError as e:
        print(f"[ERROR] Conversion error: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        return False


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Convert Markdown to Word using pypandoc',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s meeting-notes.md
  %(prog)s meeting-notes.md output/notes.docx
  %(prog)s report.md --template company-template.docx
        """
    )

    parser.add_argument(
        'input_file',
        help='Input markdown file (.md)'
    )

    parser.add_argument(
        'output_file',
        nargs='?',
        default=None,
        help='Output Word file (.docx) - defaults to same name as input'
    )

    parser.add_argument(
        '--template', '-t',
        dest='reference_doc',
        help='Word template file for custom styling'
    )

    parser.add_argument(
        '--version',
        action='version',
        version=f'%(prog)s 1.0.0'
    )

    args = parser.parse_args()

    # Ensure Pandoc is installed
    if not setup_pandoc():
        sys.exit(1)

    # Perform conversion
    success = convert_markdown_to_word(
        args.input_file,
        args.output_file,
        args.reference_doc
    )

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
