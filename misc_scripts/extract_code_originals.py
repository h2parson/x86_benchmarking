#!/usr/bin/env python3
"""
For every file in a given directory, replace its contents with only lines
571 to 782 (1-indexed, inclusive). For each of those lines:

  1. Find the SECOND occurrence of "//" and strip everything from that
     point onward (i.e. truncate the line right before the second "//").
     If there is no second occurrence, the line is left untruncated.
  2. In what remains, remove the FIRST occurrence of "//" itself (just
     those two characters), keeping the text before and after it intact.
  3. Strip leading/trailing whitespace.

Usage:
    python process_files2.py /path/to/directory [--dry-run]

--dry-run prints what would happen without modifying any files.
"""

import argparse
import sys
from pathlib import Path

START_LINE = 571
END_LINE = 782
MARKER = "//"


def process_line(line: str) -> str:
    # Find first and second occurrences of "//"
    first_idx = line.find(MARKER)
    second_idx = -1
    if first_idx != -1:
        second_idx = line.find(MARKER, first_idx + len(MARKER))

    # Step 1: truncate right before the second occurrence, if it exists
    if second_idx != -1:
        line = line[:second_idx]

    # Step 2: remove the first occurrence of "//" (just the marker itself),
    # keeping text before and after it
    idx = line.find(MARKER)
    if idx != -1:
        line = line[:idx] + line[idx + len(MARKER):]

    # Step 3: strip leading/trailing whitespace
    return line.strip()


def process_file(path: Path, dry_run: bool = False) -> None:
    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except UnicodeDecodeError:
        print(f"Skipping {path} (not valid UTF-8 text)")
        return
    except OSError as e:
        print(f"Skipping {path} (could not read: {e})")
        return

    # Slice lines 571-782 (1-indexed, inclusive) -> 0-indexed [570:782]
    selected = lines[START_LINE - 1:END_LINE]

    if not selected:
        print(f"Skipping {path} (fewer than {START_LINE} lines, nothing in range)")
        return

    processed = [process_line(line) for line in selected]
    new_content = "\n".join(processed) + "\n"

    if dry_run:
        print(f"[dry-run] Would rewrite {path} ({len(processed)} lines)")
        return

    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Rewrote {path} ({len(processed)} lines)")
    except OSError as e:
        print(f"Failed to write {path}: {e}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", help="Directory containing files to process")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would happen without modifying files",
    )
    args = parser.parse_args()

    target_dir = Path(args.directory)
    if not target_dir.is_dir():
        print(f"Error: {target_dir} is not a directory", file=sys.stderr)
        sys.exit(1)

    files = [p for p in target_dir.iterdir() if p.is_file()]
    if not files:
        print(f"No files found in {target_dir}")
        return

    for path in sorted(files):
        process_file(path, dry_run=args.dry_run)


if __name__ == "__main__":
    main()