#!/usr/bin/env python3
"""
Post-process converted Markdown files to clean up TOC formatting, headers, and footers.
"""

import argparse
import re
import sys
from pathlib import Path


def clean_toc_line(line: str) -> str | None:
    """
    Clean a TOC line by removing dot leaders and page numbers.
    Returns None if the line is not a TOC entry.
    """
    # Match lines with dot leaders (....) followed by page numbers
    # Examples:
    #   1.1 UMC 1.1............................................................................................................................ 4
    #   **1 Main Functionalities ............................................................................................................... 4**

    # Pattern for bold section headers: **1 Title ... 4**
    bold_match = re.match(r'^\*\*(\d+(?:\.\d+)*)\s+(.+?)\s*\.{2,}\s*\d+\*\*$', line.strip())
    if bold_match:
        num, title = bold_match.groups()
        return f"#### {num} {title.strip()}"

    # Pattern for regular entries: 1.1 Title ... 4
    regular_match = re.match(r'^(\d+(?:\.\d+)*)\s+(.+?)\s*\.{2,}\s*\d+$', line.strip())
    if regular_match:
        num, title = regular_match.groups()
        return f"- {num} {title.strip()}"

    return None


def process_markdown(content: str) -> str:
    """
    Process markdown content to clean up TOC sections.
    """
    lines = content.split('\n')
    result = []
    in_toc = False

    for i, line in enumerate(lines):
        # Detect start of TOC section
        if re.match(r'^#{1,4}\s*\*?\*?Contents\*?\*?\s*$', line.strip(), re.IGNORECASE):
            in_toc = True
            result.append(line)
            continue

        # Detect end of TOC (next major heading or significant content)
        if in_toc and line.strip():
            # Check if this looks like a TOC entry
            cleaned = clean_toc_line(line)
            if cleaned:
                result.append(cleaned)
                continue
            # Check if it's an empty bold line (section separator in TOC)
            elif re.match(r'^\*\*\d+\s+', line.strip()):
                cleaned = clean_toc_line(line)
                if cleaned:
                    result.append(cleaned)
                    continue
            # If we hit a real heading or content, TOC is over
            elif re.match(r'^#{1,4}\s+', line) or (line.strip() and not line.strip().startswith('*')):
                # Check it's not a TOC-style line
                if not re.search(r'\.{2,}\s*\d+', line):
                    in_toc = False

        result.append(line)

    # Clean up multiple consecutive blank lines (reduce to max 1)
    output = '\n'.join(result)
    output = re.sub(r'\n{3,}', '\n\n', output)

    # Clean up excessively indented list items (common in PDF extraction)
    # Match lines with lots of leading whitespace followed by - or *
    output = re.sub(r'^[ \t]{4,}([-*])', r'\1', output, flags=re.MULTILINE)

    # Remove PDF headers/footers
    # Document title headers (e.g., "User Management Component 2.9.2 - UMC Federation...")
    output = re.sub(r'^.+\d+\.\d+(?:\.\d+)?\s*-\s*.+(?:Manual|Notes|Guide|Overview)\s*$', '', output, flags=re.MULTILINE)
    # Document ID footers (e.g., "A5E50361223-AA")
    output = re.sub(r'^A\d{1}E\d+-[A-Z]{2}\s*$', '', output, flags=re.MULTILINE)
    # Standalone page numbers (Arabic or Roman numerals)
    output = re.sub(r'^(?:i{1,3}|iv|vi{0,3}|ix|x{0,3}|\d{1,3})\s*$', '', output, flags=re.MULTILINE | re.IGNORECASE)
    # Section references in headers (e.g., "_1 Overview_")
    output = re.sub(r'^_\d+(?:\.\d+)*\s+[^_]+_\s*$', '', output, flags=re.MULTILINE)

    # Clean up multiple consecutive blank lines again after removals
    output = re.sub(r'\n{3,}', '\n\n', output)

    return output


def process_file(filepath: Path, force: bool = False) -> bool:
    """
    Process a single markdown file.
    Returns True if changes were made.
    """
    content = filepath.read_text(encoding='utf-8')
    processed = process_markdown(content)

    if content != processed:
        if not force:
            backup = filepath.with_suffix('.md.bak')
            filepath.rename(backup)
            print(f"Backup saved: {backup}")

        filepath.write_text(processed, encoding='utf-8')
        print(f"Processed: {filepath}")
        return True
    else:
        print(f"No changes: {filepath}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Post-process markdown files to clean up TOC formatting"
    )
    parser.add_argument("path", help="Markdown file or directory to process")
    parser.add_argument(
        "-f", "--force",
        action="store_true",
        help="Overwrite without creating backup",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be changed without modifying files",
    )

    args = parser.parse_args()
    path = Path(args.path)

    if path.is_file():
        files = [path]
    elif path.is_dir():
        files = list(path.rglob("*.md"))
    else:
        print(f"Error: {path} not found", file=sys.stderr)
        sys.exit(1)

    if args.dry_run:
        for f in files:
            content = f.read_text(encoding='utf-8')
            processed = process_markdown(content)
            if content != processed:
                print(f"Would modify: {f}")
                # Show a preview of changes
                for orig, new in zip(content.split('\n'), processed.split('\n')):
                    if orig != new:
                        print(f"  - {orig[:60]}...")
                        print(f"  + {new[:60]}...")
                        break
    else:
        modified = sum(1 for f in files if process_file(f, args.force))
        print(f"\nModified {modified}/{len(files)} files")


if __name__ == "__main__":
    main()
