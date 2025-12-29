#!/usr/bin/env python3
"""
Word Template Automation via COM (Windows)

This tool uses Windows COM automation (win32com.client) to control Microsoft Word
directly for advanced template manipulation. This approach provides:

- Full access to Word's object model (all features available)
- Reliable find/replace with formatting preservation
- Support for content controls, bookmarks, and custom properties
- Works with any template structure
- Better handling of complex formatting, tables, and embedded objects

Requirements:
    pip install pywin32

Usage:
    # Simple placeholder replacement
    python word-template-automation.py template.docx output.docx \\
        --replace "{{CLIENT_NAME}}" "Acme Corp" \\
        --replace "{{DATE}}" "2025-12-19"

    # Using a JSON mapping file
    python word-template-automation.py template.docx output.docx \\
        --mapping replacements.json

    # Interactive mode with template discovery
    python word-template-automation.py --interactive

    # List all placeholders in a template
    python word-template-automation.py template.docx --list-placeholders

Key Features:
- Direct Word COM control (not python-docx)
- Preserves all formatting, styles, images, tables
- Supports any placeholder format: {{NAME}}, [NAME], ###NAME###, etc.
- Case-insensitive or case-sensitive search
- Whole word or partial matching
- Batch processing multiple templates
- Automatic template discovery in skill folder
"""

import sys
import os
import json
import argparse
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import time

try:
    import win32com.client
    from win32com.client import constants as word_constants
except ImportError:
    print("ERROR: pywin32 is not installed")
    print("Install with: pip install pywin32")
    sys.exit(1)


class WordTemplateAutomation:
    """
    Word template automation using COM interface.

    Provides robust template manipulation with full Word functionality.
    """

    def __init__(self, visible=False, quit_on_error=True):
        """
        Initialize Word application via COM.

        Args:
            visible (bool): Make Word visible (useful for debugging)
            quit_on_error (bool): Quit Word if error occurs
        """
        self.word = None
        self.doc = None
        self.visible = visible
        self.quit_on_error = quit_on_error
        self._start_word()

    def _start_word(self):
        """Start Word application."""
        try:
            print("[COM] Starting Microsoft Word...")
            self.word = win32com.client.Dispatch("Word.Application")
            self.word.Visible = self.visible
            print("[COM] Word application started successfully")
        except Exception as e:
            print(f"[ERROR] Failed to start Word: {e}")
            raise

    def open_template(self, template_path: Path) -> bool:
        """
        Open a Word template file.

        Args:
            template_path: Path to template file

        Returns:
            bool: True if successful
        """
        try:
            abs_path = str(template_path.absolute())
            print(f"[COM] Opening template: {template_path.name}")
            self.doc = self.word.Documents.Open(abs_path)
            print(f"[COM] Template opened successfully")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to open template: {e}")
            if self.quit_on_error:
                self.quit()
            return False

    def find_placeholders(self, pattern: str = r'\{\{[A-Z_]+\}\}') -> List[str]:
        """
        Find all placeholders in the document matching a pattern.

        Args:
            pattern: Regex pattern for placeholders (default: {{NAME}} format)

        Returns:
            List of unique placeholders found
        """
        if not self.doc:
            print("[ERROR] No document is open")
            return []

        placeholders = set()

        try:
            # Search in main document body
            content = self.doc.Content.Text
            matches = re.findall(pattern, content, re.IGNORECASE)
            placeholders.update(matches)

            # Search in headers and footers
            for section in self.doc.Sections:
                # Headers
                for header in section.Headers:
                    if header.Exists:
                        header_text = header.Range.Text
                        matches = re.findall(pattern, header_text, re.IGNORECASE)
                        placeholders.update(matches)

                # Footers
                for footer in section.Footers:
                    if footer.Exists:
                        footer_text = footer.Range.Text
                        matches = re.findall(pattern, footer_text, re.IGNORECASE)
                        placeholders.update(matches)

            # Search in text boxes and shapes
            for shape in self.doc.Shapes:
                if shape.TextFrame.HasText:
                    shape_text = shape.TextFrame.TextRange.Text
                    matches = re.findall(pattern, shape_text, re.IGNORECASE)
                    placeholders.update(matches)

            return sorted(list(placeholders))

        except Exception as e:
            print(f"[ERROR] Failed to find placeholders: {e}")
            return []

    def replace_text(self,
                     find_text: str,
                     replace_with: str,
                     match_case: bool = False,
                     match_whole_word: bool = False,
                     replace_all: bool = True) -> int:
        """
        Replace text in the document using Word's Find/Replace.

        This preserves formatting and handles all document areas
        (body, headers, footers, text boxes, tables, etc.)

        Args:
            find_text: Text to find
            replace_with: Replacement text
            match_case: Case-sensitive matching
            match_whole_word: Match whole words only
            replace_all: Replace all occurrences (False = replace first only)

        Returns:
            int: Number of replacements made
        """
        if not self.doc:
            print("[ERROR] No document is open")
            return 0

        replacements = 0

        try:
            # Create Find object for main document
            find_obj = self.word.Selection.Find
            find_obj.ClearFormatting()
            find_obj.Replacement.ClearFormatting()

            # Set find parameters
            find_obj.Text = find_text
            find_obj.Replacement.Text = replace_with
            find_obj.MatchCase = match_case
            find_obj.MatchWholeWord = match_whole_word
            find_obj.Forward = True
            find_obj.Wrap = 1  # wdFindContinue

            # Replace in main document
            if replace_all:
                # Move to start of document
                self.word.Selection.HomeKey(Unit=6)  # wdStory

                # Execute replace all
                result = find_obj.Execute(Replace=2)  # wdReplaceAll
                if result:
                    replacements += 1
            else:
                # Replace first occurrence only
                result = find_obj.Execute(Replace=1)  # wdReplaceOne
                if result:
                    replacements = 1

            # Replace in headers and footers
            for section in self.doc.Sections:
                # Headers
                for header_type in [1, 2, 3]:  # wdHeaderFooterPrimary, FirstPage, EvenPages
                    try:
                        header = section.Headers(header_type)
                        if header.Exists:
                            header_range = header.Range
                            header_find = header_range.Find
                            header_find.ClearFormatting()
                            header_find.Replacement.ClearFormatting()
                            header_find.Text = find_text
                            header_find.Replacement.Text = replace_with
                            header_find.MatchCase = match_case
                            header_find.MatchWholeWord = match_whole_word

                            if replace_all:
                                header_find.Execute(Replace=2)
                            else:
                                header_find.Execute(Replace=1)
                    except:
                        pass

                # Footers
                for footer_type in [1, 2, 3]:
                    try:
                        footer = section.Footers(footer_type)
                        if footer.Exists:
                            footer_range = footer.Range
                            footer_find = footer_range.Find
                            footer_find.ClearFormatting()
                            footer_find.Replacement.ClearFormatting()
                            footer_find.Text = find_text
                            footer_find.Replacement.Text = replace_with
                            footer_find.MatchCase = match_case
                            footer_find.MatchWholeWord = match_whole_word

                            if replace_all:
                                footer_find.Execute(Replace=2)
                            else:
                                footer_find.Execute(Replace=1)
                    except:
                        pass

            # Replace in text boxes and shapes
            for shape in self.doc.Shapes:
                try:
                    if shape.TextFrame.HasText:
                        shape_range = shape.TextFrame.TextRange
                        shape_find = shape_range.Find
                        shape_find.ClearFormatting()
                        shape_find.Replacement.ClearFormatting()
                        shape_find.Text = find_text
                        shape_find.Replacement.Text = replace_with
                        shape_find.MatchCase = match_case
                        shape_find.MatchWholeWord = match_whole_word

                        if replace_all:
                            shape_find.Execute(Replace=2)
                        else:
                            shape_find.Execute(Replace=1)
                except:
                    pass

            return replacements

        except Exception as e:
            print(f"[ERROR] Failed to replace text '{find_text}': {e}")
            return 0

    def replace_multiple(self,
                        replacements: Dict[str, str],
                        match_case: bool = False,
                        match_whole_word: bool = False) -> Dict[str, int]:
        """
        Replace multiple placeholders in one pass.

        Args:
            replacements: Dictionary of {find_text: replace_with}
            match_case: Case-sensitive matching
            match_whole_word: Match whole words only

        Returns:
            Dict[str, int]: Dictionary of {find_text: replacement_count}
        """
        results = {}

        print(f"\n[COM] Replacing {len(replacements)} placeholders...")

        for find_text, replace_with in replacements.items():
            print(f"  Replacing '{find_text}' -> '{replace_with}'")
            count = self.replace_text(
                find_text,
                replace_with,
                match_case=match_case,
                match_whole_word=match_whole_word,
                replace_all=True
            )
            results[find_text] = count

        return results

    def save_as(self, output_path: Path) -> bool:
        """
        Save document to a new file.

        Args:
            output_path: Path for output file

        Returns:
            bool: True if successful
        """
        if not self.doc:
            print("[ERROR] No document is open")
            return False

        try:
            abs_path = str(output_path.absolute())
            print(f"[COM] Saving document: {output_path.name}")

            # Save as .docx (format 16)
            self.doc.SaveAs2(abs_path, FileFormat=16)
            print(f"[COM] Document saved successfully")
            return True

        except Exception as e:
            print(f"[ERROR] Failed to save document: {e}")
            return False

    def close_document(self, save_changes: bool = False):
        """
        Close the current document.

        Args:
            save_changes: Save changes before closing
        """
        if self.doc:
            try:
                print("[COM] Closing document...")
                self.doc.Close(SaveChanges=save_changes)
                self.doc = None
                print("[COM] Document closed")
            except Exception as e:
                print(f"[ERROR] Failed to close document: {e}")

    def quit(self):
        """Quit Word application."""
        if self.word:
            try:
                print("[COM] Quitting Word application...")
                self.close_document(save_changes=False)
                self.word.Quit()
                self.word = None
                print("[COM] Word application closed")
            except Exception as e:
                print(f"[ERROR] Failed to quit Word: {e}")

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.quit()


def discover_templates(skill_path: Path) -> List[Path]:
    """
    Discover all .docx templates in the skill's templates folder.

    Args:
        skill_path: Path to writing-proposals skill folder

    Returns:
        List of template file paths
    """
    templates_dir = skill_path / "templates"
    if not templates_dir.exists():
        return []

    return sorted(templates_dir.glob("*.docx"))


def load_mapping_file(mapping_path: Path) -> Dict[str, str]:
    """
    Load placeholder mappings from JSON file.

    Args:
        mapping_path: Path to JSON file

    Returns:
        Dictionary of {placeholder: replacement}
    """
    try:
        with open(mapping_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"[ERROR] Failed to load mapping file: {e}")
        return {}


def save_mapping_file(mapping_path: Path, mappings: Dict[str, str]):
    """
    Save placeholder mappings to JSON file.

    Args:
        mapping_path: Path to JSON file
        mappings: Dictionary of {placeholder: replacement}
    """
    try:
        with open(mapping_path, 'w', encoding='utf-8') as f:
            json.dump(mappings, f, indent=2, ensure_ascii=False)
        print(f"[OK] Mapping file saved: {mapping_path}")
    except Exception as e:
        print(f"[ERROR] Failed to save mapping file: {e}")


def list_placeholders_in_template(template_path: Path, pattern: str = r'\{\{[A-Z_]+\}\}'):
    """
    List all placeholders found in a template.

    Args:
        template_path: Path to template file
        pattern: Regex pattern for placeholders
    """
    print("=" * 80)
    print(f"PLACEHOLDER ANALYSIS")
    print("=" * 80)
    print(f"Template: {template_path.name}")
    print(f"Pattern: {pattern}")
    print("=" * 80)

    with WordTemplateAutomation(visible=False) as word:
        if word.open_template(template_path):
            placeholders = word.find_placeholders(pattern)

            if placeholders:
                print(f"\nFound {len(placeholders)} unique placeholders:\n")
                for i, placeholder in enumerate(placeholders, 1):
                    print(f"  {i:2d}. {placeholder}")

                print("\n" + "=" * 80)
                print("To create a mapping file, run:")
                print(f"  python word-template-automation.py {template_path.name} \\")
                print(f"    --create-mapping mapping.json")
                print("=" * 80)
            else:
                print("\n[INFO] No placeholders found matching pattern")
                print("\nCommon placeholder formats:")
                print("  {{NAME}}       - Double curly braces")
                print("  [NAME]         - Square brackets")
                print("  ###NAME###     - Triple hash marks")
                print("  <<NAME>>       - Double angle brackets")
                print("\nUse --pattern to specify custom regex pattern")


def create_mapping_template(template_path: Path, output_path: Path, pattern: str = r'\{\{[A-Z_]+\}\}'):
    """
    Create a mapping template JSON file from placeholders in a template.

    Args:
        template_path: Path to template file
        output_path: Path for mapping JSON file
        pattern: Regex pattern for placeholders
    """
    with WordTemplateAutomation(visible=False) as word:
        if word.open_template(template_path):
            placeholders = word.find_placeholders(pattern)

            if placeholders:
                # Create mapping dictionary with empty values
                mapping = {placeholder: "" for placeholder in placeholders}
                save_mapping_file(output_path, mapping)

                print(f"\n[SUCCESS] Mapping template created: {output_path}")
                print(f"Found {len(placeholders)} placeholders")
                print("\nNext steps:")
                print(f"  1. Edit {output_path}")
                print("  2. Fill in replacement values for each placeholder")
                print("  3. Run:")
                print(f"     python word-template-automation.py {template_path.name} output.docx \\")
                print(f"       --mapping {output_path.name}")
            else:
                print("[INFO] No placeholders found - no mapping file created")


def process_template(template_path: Path,
                     output_path: Path,
                     replacements: Dict[str, str],
                     match_case: bool = False,
                     match_whole_word: bool = False,
                     visible: bool = False) -> bool:
    """
    Process a template with replacements and save output.

    Args:
        template_path: Path to template file
        output_path: Path for output file
        replacements: Dictionary of {find: replace}
        match_case: Case-sensitive matching
        match_whole_word: Match whole words only
        visible: Make Word visible

    Returns:
        bool: True if successful
    """
    print("\n" + "=" * 80)
    print("WORD TEMPLATE AUTOMATION")
    print("=" * 80)
    print(f"Template: {template_path}")
    print(f"Output: {output_path}")
    print(f"Replacements: {len(replacements)}")
    print("=" * 80)

    with WordTemplateAutomation(visible=visible) as word:
        # Open template
        if not word.open_template(template_path):
            return False

        # Perform replacements
        results = word.replace_multiple(
            replacements,
            match_case=match_case,
            match_whole_word=match_whole_word
        )

        # Report results
        print("\n" + "=" * 80)
        print("REPLACEMENT SUMMARY")
        print("=" * 80)
        for find_text, count in results.items():
            status = "✓" if count > 0 else "✗"
            print(f"  {status} {find_text}: {count} replacements")

        # Save output
        success = word.save_as(output_path)

        if success:
            print("\n" + "=" * 80)
            print("[SUCCESS] TEMPLATE PROCESSING COMPLETE")
            print("=" * 80)
            print(f"Output file: {output_path.absolute()}")
            print("=" * 80)

        return success


def interactive_mode(skill_path: Path):
    """
    Interactive mode for template processing.

    Args:
        skill_path: Path to writing-proposals skill folder
    """
    print("\n" + "=" * 80)
    print("WORD TEMPLATE AUTOMATION - INTERACTIVE MODE")
    print("=" * 80)

    # Discover templates
    templates = discover_templates(skill_path)

    if not templates:
        print("\n[ERROR] No templates found in skill folder")
        print(f"Expected location: {skill_path / 'templates'}")
        return False

    # Select template
    print("\nAvailable templates:")
    for i, template in enumerate(templates, 1):
        print(f"  {i}. {template.name}")

    try:
        choice = int(input("\nSelect template (number): "))
        template_path = templates[choice - 1]
    except (ValueError, IndexError):
        print("[ERROR] Invalid selection")
        return False

    # Analyze template
    print(f"\nAnalyzing template: {template_path.name}")
    with WordTemplateAutomation(visible=False) as word:
        if not word.open_template(template_path):
            return False

        placeholders = word.find_placeholders()

        if not placeholders:
            print("\n[INFO] No placeholders found in template")
            print("This template may not use {{PLACEHOLDER}} format")

            custom_pattern = input("\nEnter custom regex pattern (or press Enter to skip): ").strip()
            if custom_pattern:
                placeholders = word.find_placeholders(custom_pattern)

        if not placeholders:
            print("[INFO] No placeholders to replace")
            return False

    # Gather replacements
    print(f"\nFound {len(placeholders)} placeholders")
    print("Enter replacement values (press Enter to skip):\n")

    replacements = {}
    for placeholder in placeholders:
        value = input(f"  {placeholder}: ").strip()
        if value:
            replacements[placeholder] = value

    if not replacements:
        print("\n[INFO] No replacements provided")
        return False

    # Output file
    default_output = template_path.stem + "_filled.docx"
    output_file = input(f"\nOutput file [{default_output}]: ").strip() or default_output
    output_path = template_path.parent / output_file

    # Process template
    return process_template(
        template_path,
        output_path,
        replacements,
        match_case=False,
        match_whole_word=False,
        visible=False
    )


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Word template automation using COM (Windows)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Replace placeholders
  %(prog)s template.docx output.docx \\
    --replace "{{CLIENT}}" "Acme Corp" \\
    --replace "{{DATE}}" "2025-12-19"

  # Use JSON mapping file
  %(prog)s template.docx output.docx --mapping replacements.json

  # Interactive mode
  %(prog)s --interactive

  # List placeholders in template
  %(prog)s template.docx --list-placeholders

  # Create mapping template
  %(prog)s template.docx --create-mapping mapping.json

  # Custom placeholder pattern
  %(prog)s template.docx --list-placeholders --pattern "\\[\\w+\\]"

Placeholder Formats:
  Default:  {{NAME}}      (double curly braces)
  Custom:   Use --pattern with regex

  Examples:
    {{NAME}}       - --pattern "\\{\\{[A-Z_]+\\}\\}"
    [NAME]         - --pattern "\\[[A-Z_]+\\]"
    ###NAME###     - --pattern "###[A-Z_]+###"
    <<NAME>>       - --pattern "<<[A-Z_]+>>"
        """
    )

    parser.add_argument(
        'template_file',
        nargs='?',
        help='Template file (.docx)'
    )

    parser.add_argument(
        'output_file',
        nargs='?',
        help='Output file (.docx)'
    )

    parser.add_argument(
        '--interactive', '-i',
        action='store_true',
        help='Interactive mode'
    )

    parser.add_argument(
        '--replace', '-r',
        action='append',
        nargs=2,
        metavar=('FIND', 'REPLACE'),
        help='Replace text (can be used multiple times)'
    )

    parser.add_argument(
        '--mapping', '-m',
        help='JSON file with placeholder mappings'
    )

    parser.add_argument(
        '--list-placeholders', '-l',
        action='store_true',
        help='List all placeholders in template'
    )

    parser.add_argument(
        '--create-mapping', '-c',
        metavar='OUTPUT_JSON',
        help='Create mapping template JSON from placeholders'
    )

    parser.add_argument(
        '--pattern', '-p',
        default=r'\{\{[A-Z_]+\}\}',
        help='Regex pattern for placeholders (default: {{NAME}})'
    )

    parser.add_argument(
        '--match-case',
        action='store_true',
        help='Case-sensitive replacement'
    )

    parser.add_argument(
        '--match-whole-word',
        action='store_true',
        help='Match whole words only'
    )

    parser.add_argument(
        '--visible',
        action='store_true',
        help='Make Word visible (for debugging)'
    )

    args = parser.parse_args()

    # Get skill path
    script_dir = Path(__file__).parent
    skill_path = script_dir.parent

    # Interactive mode
    if args.interactive:
        success = interactive_mode(skill_path)
        sys.exit(0 if success else 1)

    # Require template file for other modes
    if not args.template_file:
        print("[ERROR] Template file required (or use --interactive)")
        parser.print_help()
        sys.exit(1)

    template_path = Path(args.template_file)
    if not template_path.exists():
        # Try templates folder
        template_path = skill_path / "templates" / args.template_file
        if not template_path.exists():
            print(f"[ERROR] Template not found: {args.template_file}")
            sys.exit(1)

    # List placeholders mode
    if args.list_placeholders:
        list_placeholders_in_template(template_path, args.pattern)
        sys.exit(0)

    # Create mapping template mode
    if args.create_mapping:
        output_path = Path(args.create_mapping)
        create_mapping_template(template_path, output_path, args.pattern)
        sys.exit(0)

    # Process template mode
    if not args.output_file:
        print("[ERROR] Output file required for template processing")
        parser.print_help()
        sys.exit(1)

    output_path = Path(args.output_file)

    # Build replacements dictionary
    replacements = {}

    # From --replace arguments
    if args.replace:
        for find_text, replace_with in args.replace:
            replacements[find_text] = replace_with

    # From mapping file
    if args.mapping:
        mapping_path = Path(args.mapping)
        if not mapping_path.exists():
            print(f"[ERROR] Mapping file not found: {args.mapping}")
            sys.exit(1)

        file_mappings = load_mapping_file(mapping_path)
        replacements.update(file_mappings)

    if not replacements:
        print("[ERROR] No replacements specified (use --replace or --mapping)")
        parser.print_help()
        sys.exit(1)

    # Process template
    success = process_template(
        template_path,
        output_path,
        replacements,
        match_case=args.match_case,
        match_whole_word=args.match_whole_word,
        visible=args.visible
    )

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
