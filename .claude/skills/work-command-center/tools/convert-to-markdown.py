#!/usr/bin/env python3
"""
Convert various file types to LLM-ready Markdown using Microsoft's markitdown library.

Supports: PDF, DOCX, PPTX, XLSX, XLS, images (JPG, PNG), audio (WAV, MP3), HTML, and ZIP archives.

Usage:
    python convert-to-markdown.py <input_file> [output_file]
    python convert-to-markdown.py <input_file> --stdout
    python convert-to-markdown.py <input_file> --json

Examples:
    python convert-to-markdown.py report.pdf
    python convert-to-markdown.py data.xlsx output.md
    python convert-to-markdown.py image.png --stdout
    python convert-to-markdown.py presentation.pptx --json
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

try:
    from markitdown import MarkItDown
except ImportError:
    print("ERROR: markitdown library not found.", file=sys.stderr)
    print("Install with: pip install 'markitdown[all]'", file=sys.stderr)
    sys.exit(1)


def convert_file(
    input_path: str,
    output_path: Optional[str] = None,
    use_stdout: bool = False,
    json_output: bool = False,
) -> dict:
    """
    Convert a file to Markdown format.

    Args:
        input_path: Path to input file
        output_path: Optional path for output file (default: input_path + .md)
        use_stdout: If True, print to stdout instead of file
        json_output: If True, output as JSON with metadata

    Returns:
        Dictionary with conversion results and metadata
    """
    input_file = Path(input_path)

    # Validate input file exists
    if not input_file.exists():
        return {
            "success": False,
            "error": f"Input file not found: {input_path}",
            "input_path": input_path
        }

    # Validate input file is a file (not directory)
    if not input_file.is_file():
        return {
            "success": False,
            "error": f"Input path is not a file: {input_path}",
            "input_path": input_path
        }

    try:
        # Initialize MarkItDown
        md = MarkItDown()

        # Convert the file
        result = md.convert(str(input_file))
        markdown_content = result.text_content

        # Determine output path if not specified
        if not use_stdout and not json_output and output_path is None:
            output_path = str(input_file.with_suffix('.md'))

        # Prepare result metadata
        result_data = {
            "success": True,
            "input_path": str(input_file.absolute()),
            "input_name": input_file.name,
            "input_extension": input_file.suffix,
            "content_length": len(markdown_content),
            "line_count": len(markdown_content.splitlines()),
        }

        # Handle output based on mode
        if json_output:
            result_data["markdown"] = markdown_content
            print(json.dumps(result_data, indent=2, ensure_ascii=False))
        elif use_stdout:
            # Use UTF-8 encoding for stdout on Windows
            if sys.platform == 'win32':
                sys.stdout.reconfigure(encoding='utf-8')
            print(markdown_content)
            result_data["output_mode"] = "stdout"
        else:
            # Write to file
            output_file = Path(output_path)
            output_file.write_text(markdown_content, encoding='utf-8')
            result_data["output_path"] = str(output_file.absolute())
            result_data["output_name"] = output_file.name
            # Use ASCII-safe output for Windows console
            print(f"[OK] Converted: {input_file.name} -> {output_file.name}")
            print(f"  Lines: {result_data['line_count']} | Characters: {result_data['content_length']}")

        return result_data

    except Exception as e:
        error_data = {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__,
            "input_path": str(input_file.absolute())
        }

        if json_output:
            print(json.dumps(error_data, indent=2))
        else:
            print(f"ERROR: Failed to convert {input_file.name}", file=sys.stderr)
            print(f"  {type(e).__name__}: {e}", file=sys.stderr)

        return error_data


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Convert files to LLM-ready Markdown using Microsoft's markitdown library.",
        epilog="""
Supported file types:
  Documents: PDF, DOCX, PPTX, XLSX, XLS
  Media: JPG, PNG, WAV, MP3
  Web: HTML
  Archives: ZIP
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "input_file",
        help="Path to the file to convert"
    )

    parser.add_argument(
        "output_file",
        nargs="?",
        default=None,
        help="Optional output path (default: input_file.md)"
    )

    parser.add_argument(
        "--stdout",
        action="store_true",
        help="Print markdown to stdout instead of file"
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON with metadata"
    )

    args = parser.parse_args()

    # Convert the file
    result = convert_file(
        input_path=args.input_file,
        output_path=args.output_file,
        use_stdout=args.stdout,
        json_output=args.json
    )

    # Exit with appropriate code
    sys.exit(0 if result["success"] else 1)


if __name__ == "__main__":
    main()
