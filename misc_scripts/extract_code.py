#!/usr/bin/env python3
"""
For every file in a given directory, replace its contents with only lines
355 to 566 (1-indexed, inclusive), stripping everything from the first
occurrence of '//' onward on each line, and trimming leading/trailing
whitespace from each resulting line.

Usage:
    python process_files.py /path/to/directory [--dry-run]

--dry-run prints what would happen without modifying any files.
"""

import argparse
import sys
from pathlib import Path

START_LINE = 355
END_LINE = 566


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

    first = lines[0].strip()
    stalls = first.split(' ')[1]

    # Slice lines 355-566 (1-indexed, inclusive) -> 0-indexed [354:566]
    selected = lines[START_LINE - 1:END_LINE]

    if not selected:
        print(f"Skipping {path} (fewer than {START_LINE} lines, nothing in range)")
        return

    processed = []
    for line in selected:
        # Strip everything after and including the first "//"
        idx = line.find("//")
        if idx != -1:
            line = line[:idx]
        # Strip leading/trailing whitespace
        line = line.strip()
        processed.append(line)

    new_content = "\n".join(processed) + "\n"

    if dry_run:
        print(f"[dry-run] Would rewrite {path} ({len(processed)} lines)")
        return

    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Rewrote {path} ({len(processed)} lines)")
        return stalls
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

    stall_list = []

    for path in sorted(files):
        stall_list.append(process_file(path, dry_run=args.dry_run))

    print("stalls in order:")
    print(stall_list)


if __name__ == "__main__":
    main()