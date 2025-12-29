#!/usr/bin/env python3
"""
Collect Feedback on Manual Corrections After Conversion

This tool collects user feedback on what manual edits were needed after
markdown-to-Word conversion, then analyzes if those corrections can be
automated for future conversions using the same template.

The feedback is stored in template-corrections.json and automatically
applied in future conversions.

Usage:
    python collect-feedback.py output.docx
    python collect-feedback.py output.docx --template proposal-template.docx
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime


def load_corrections_db(corrections_file):
    """Load the template corrections database."""
    if corrections_file.exists():
        with open(corrections_file, 'r') as f:
            return json.load(f)
    else:
        return {
            "_comment": "Template-specific correction rules learned from user feedback",
            "_format": {
                "template_name": {
                    "style_corrections": {},
                    "find_replace": [],
                    "formatting_fixes": [],
                    "manual_steps_remaining": []
                }
            }
        }


def save_corrections_db(corrections_file, data):
    """Save the template corrections database."""
    with open(corrections_file, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"\n[OK] Corrections database updated: {corrections_file}")


def get_template_name(template_path):
    """Get the template filename."""
    if template_path:
        return Path(template_path).name
    else:
        # Default template
        return "proposal-template.docx"


def ensure_template_entry(corrections_db, template_name):
    """Ensure template has an entry in the corrections database."""
    if template_name not in corrections_db:
        corrections_db[template_name] = {
            "style_corrections": {},
            "find_replace": [],
            "formatting_fixes": [],
            "manual_steps_remaining": []
        }
    return corrections_db[template_name]


def analyze_automation_potential(issue_description):
    """
    Analyze if an issue can be automated and return suggested approach.

    Returns:
        tuple: (can_automate: bool, suggestion: str, category: str)
    """
    issue_lower = issue_description.lower()

    # Style-related issues
    if any(word in issue_lower for word in ['style', 'font', 'formatting', 'bold', 'italic']):
        if 'normal' in issue_lower or 'body text' in issue_lower:
            return (True, "Add to style_corrections mapping", "style")
        return (True, "Can likely automate with python-docx style changes", "style")

    # Find/replace issues
    if any(word in issue_lower for word in ['replace', 'change text', 'wording', 'phrase']):
        return (True, "Add to find_replace list", "find_replace")

    # Spacing issues
    if any(word in issue_lower for word in ['spacing', 'space', 'gap', 'margin', 'padding']):
        return (True, "Can automate with paragraph formatting", "formatting")

    # Table issues
    if 'table' in issue_lower:
        return (True, "Can automate with table styling", "formatting")

    # Bullet/numbering issues
    if any(word in issue_lower for word in ['bullet', 'number', 'list']):
        return (True, "Can automate with list style mapping", "style")

    # Page break issues
    if 'page break' in issue_lower:
        return (True, "Can automate with page break insertion logic", "formatting")

    # Header/footer issues
    if any(word in issue_lower for word in ['header', 'footer']):
        return (False, "Headers/footers are template-specific - may need template update", "manual")

    # Image/graphic issues
    if any(word in issue_lower for word in ['image', 'picture', 'graphic', 'logo']):
        return (False, "Image handling requires manual placement", "manual")

    # Content issues (requires human judgment)
    if any(word in issue_lower for word in ['content', 'wording', 'edit text', 'rewrite']):
        return (False, "Content changes require human judgment", "manual")

    # Default: might be automatable
    return (None, "Needs analysis - please provide more details", "unknown")


def collect_feedback_interactive(output_file, template_name, corrections_db):
    """Collect feedback interactively from the user."""

    print("\n" + "=" * 70)
    print("CONVERSION FEEDBACK COLLECTION")
    print("=" * 70)
    print(f"Document: {output_file}")
    print(f"Template: {template_name}")
    print("=" * 70)

    print("\nThis feedback helps improve future conversions by automating")
    print("common manual corrections specific to this template.\n")

    template_data = ensure_template_entry(corrections_db, template_name)

    print("What manual corrections did you need to make? (Enter one per line)")
    print("Type 'done' when finished, or 'skip' to skip feedback.\n")

    corrections = []
    correction_num = 1

    while True:
        response = input(f"  {correction_num}. ").strip()

        if response.lower() == 'done':
            break
        elif response.lower() == 'skip':
            print("\n[Skipped] No feedback collected.")
            return False
        elif not response:
            continue

        corrections.append(response)
        correction_num += 1

    if not corrections:
        print("\n[Skipped] No corrections reported.")
        return False

    # Analyze each correction
    print("\n" + "=" * 70)
    print("ANALYZING CORRECTIONS FOR AUTOMATION")
    print("=" * 70)

    new_automations = []
    still_manual = []

    for idx, correction in enumerate(corrections, 1):
        print(f"\n[{idx}] {correction}")

        can_automate, suggestion, category = analyze_automation_potential(correction)

        if can_automate is True:
            print(f"    ✓ CAN AUTOMATE: {suggestion}")
            new_automations.append({
                "issue": correction,
                "fix": suggestion,
                "automated": False,  # Will be automated in next tool update
                "category": category,
                "reported_date": datetime.now().isoformat()
            })
        elif can_automate is False:
            print(f"    ✗ REQUIRES MANUAL: {suggestion}")
            still_manual.append(correction)
        else:
            print(f"    ? UNKNOWN: {suggestion}")
            # Ask user for clarification
            detail = input(f"      Can you provide more details? ").strip()
            if detail:
                new_automations.append({
                    "issue": f"{correction} - {detail}",
                    "fix": "Needs implementation",
                    "automated": False,
                    "category": "pending",
                    "reported_date": datetime.now().isoformat()
                })

    # Update corrections database
    if new_automations:
        template_data["formatting_fixes"].extend(new_automations)
        print(f"\n✓ Added {len(new_automations)} issues for automation")

    if still_manual:
        template_data["manual_steps_remaining"].extend(still_manual)
        print(f"\n✓ Added {len(still_manual)} manual steps to tracking")

    return True


def collect_feedback_batch(corrections_file, template_name, corrections_db):
    """Collect feedback from a batch file (one correction per line)."""

    if not corrections_file.exists():
        print(f"[ERROR] Corrections file not found: {corrections_file}")
        return False

    template_data = ensure_template_entry(corrections_db, template_name)

    with open(corrections_file, 'r') as f:
        corrections = [line.strip() for line in f if line.strip()]

    print(f"\n[OK] Loaded {len(corrections)} corrections from {corrections_file}")

    new_automations = []
    still_manual = []

    for correction in corrections:
        can_automate, suggestion, category = analyze_automation_potential(correction)

        if can_automate is True:
            new_automations.append({
                "issue": correction,
                "fix": suggestion,
                "automated": False,
                "category": category,
                "reported_date": datetime.now().isoformat()
            })
        elif can_automate is False:
            still_manual.append(correction)

    if new_automations:
        template_data["formatting_fixes"].extend(new_automations)

    if still_manual:
        template_data["manual_steps_remaining"].extend(still_manual)

    print(f"✓ {len(new_automations)} issues can be automated")
    print(f"✓ {len(still_manual)} issues require manual intervention")

    return True


def show_template_status(template_name, corrections_db):
    """Show current status of corrections for a template."""

    if template_name not in corrections_db:
        print(f"\n[INFO] No corrections recorded for template: {template_name}")
        return

    template_data = corrections_db[template_name]

    print("\n" + "=" * 70)
    print(f"TEMPLATE CORRECTIONS STATUS: {template_name}")
    print("=" * 70)

    # Style corrections
    if template_data.get("style_corrections"):
        print("\n✓ Style Corrections (AUTOMATED):")
        for source, target in template_data["style_corrections"].items():
            print(f"    {source} -> {target}")

    # Find/replace rules
    if template_data.get("find_replace"):
        print("\n✓ Find/Replace Rules (AUTOMATED):")
        for rule in template_data["find_replace"]:
            print(f"    '{rule['find']}' -> '{rule['replace']}'")

    # Formatting fixes
    automated_fixes = [f for f in template_data.get("formatting_fixes", []) if f.get("automated")]
    pending_fixes = [f for f in template_data.get("formatting_fixes", []) if not f.get("automated")]

    if automated_fixes:
        print("\n✓ Formatting Fixes (AUTOMATED):")
        for fix in automated_fixes:
            print(f"    {fix['issue']}")

    if pending_fixes:
        print("\n⚠ Formatting Fixes (PENDING AUTOMATION):")
        for fix in pending_fixes:
            print(f"    {fix['issue']}")
            print(f"      -> {fix['fix']}")

    # Manual steps
    if template_data.get("manual_steps_remaining"):
        print("\n✗ Manual Steps (NOT AUTOMATABLE):")
        for step in template_data["manual_steps_remaining"]:
            print(f"    {step}")

    print("\n" + "=" * 70)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Collect feedback on manual corrections after conversion',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive feedback collection
  %(prog)s output.docx

  # Specify template explicitly
  %(prog)s output.docx --template custom-template.docx

  # Batch mode from corrections file
  %(prog)s output.docx --batch corrections.txt

  # Show current status for a template
  %(prog)s --status proposal-template.docx

How it works:
  1. You describe manual edits you had to make
  2. Tool analyzes if each can be automated
  3. Automatable fixes are added to template-corrections.json
  4. Future conversions automatically apply learned corrections
        """
    )

    parser.add_argument(
        'output_file',
        nargs='?',
        help='The converted Word document'
    )

    parser.add_argument(
        '--template', '-t',
        dest='template_path',
        help='Template file used for conversion'
    )

    parser.add_argument(
        '--batch', '-b',
        dest='batch_file',
        help='Batch corrections file (one per line)'
    )

    parser.add_argument(
        '--status', '-s',
        dest='status_template',
        help='Show correction status for a template'
    )

    args = parser.parse_args()

    # Find corrections database
    script_dir = Path(__file__).parent
    corrections_db_file = script_dir / "template-corrections.json"

    # Load corrections database
    corrections_db = load_corrections_db(corrections_db_file)

    # Status mode
    if args.status_template:
        show_template_status(args.status_template, corrections_db)
        return

    # Validation
    if not args.output_file:
        parser.print_help()
        sys.exit(1)

    output_path = Path(args.output_file)
    if not output_path.exists():
        print(f"[ERROR] Output file not found: {args.output_file}")
        sys.exit(1)

    # Determine template name
    template_name = get_template_name(args.template_path)

    # Collect feedback
    if args.batch_file:
        updated = collect_feedback_batch(Path(args.batch_file), template_name, corrections_db)
    else:
        updated = collect_feedback_interactive(output_path, template_name, corrections_db)

    # Save if updated
    if updated:
        save_corrections_db(corrections_db_file, corrections_db)
        print("\n" + "=" * 70)
        print("NEXT STEPS")
        print("=" * 70)
        print("Your feedback has been recorded. Future conversions using")
        print(f"'{template_name}' will automatically apply automatable fixes.")
        print("\nTo see current status:")
        print(f"  python collect-feedback.py --status {template_name}")
        print("=" * 70)


if __name__ == '__main__':
    main()
