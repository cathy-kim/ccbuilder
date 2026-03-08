#!/usr/bin/env python3
"""
Package a skill directory into a distributable .skill file.

A .skill file is a zip archive containing the skill directory contents,
excluding dev-only files (evals, __pycache__, node_modules, etc.).

Usage:
    python -m scripts.package_skill /path/to/my-skill
    python -m scripts.package_skill /path/to/my-skill --output ./dist/
"""

from __future__ import annotations

import argparse
import sys
import zipfile
from pathlib import Path

from .quick_validate import validate
from .utils import parse_skill_md

EXCLUDE_PATTERNS = {
    "__pycache__",
    "node_modules",
    ".DS_Store",
    "*.pyc",
    "*.pyo",
    ".git",
    ".gitignore",
}

# Exclude evals/ at skill root only (not nested)
EXCLUDE_ROOT_DIRS = {"evals"}


def should_exclude(path: Path, root: Path) -> bool:
    """Check if a path should be excluded from packaging."""
    name = path.name

    # Check patterns
    for pattern in EXCLUDE_PATTERNS:
        if pattern.startswith("*"):
            if name.endswith(pattern[1:]):
                return True
        elif name == pattern:
            return True

    # Check root-level directory exclusions
    try:
        relative = path.relative_to(root)
        parts = relative.parts
        if len(parts) >= 1 and parts[0] in EXCLUDE_ROOT_DIRS:
            return True
    except ValueError:
        pass

    return False


def package_skill(skill_dir: Path, output_dir: Path | None = None) -> Path:
    """Package a skill directory into a .skill file."""
    skill_dir = skill_dir.resolve()

    if not skill_dir.is_dir():
        print(f"Error: {skill_dir} is not a directory", file=sys.stderr)
        sys.exit(1)

    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        print(f"Error: No SKILL.md found in {skill_dir}", file=sys.stderr)
        sys.exit(1)

    # Validate first
    print(f"Validating {skill_md}...")
    issues = validate(skill_md)
    if issues:
        print("Validation failed:", file=sys.stderr)
        for issue in issues:
            print(f"  - {issue}", file=sys.stderr)
        sys.exit(1)
    print("Validation passed!")

    # Get skill name
    name, _, _ = parse_skill_md(skill_md)

    # Determine output path
    if output_dir:
        output_dir = Path(output_dir).resolve()
        output_dir.mkdir(parents=True, exist_ok=True)
    else:
        output_dir = Path.cwd()

    output_file = output_dir / f"{name}.skill"

    # Create zip
    print(f"Packaging {name}...")
    file_count = 0

    with zipfile.ZipFile(output_file, "w", zipfile.ZIP_DEFLATED) as zf:
        for file_path in sorted(skill_dir.rglob("*")):
            if not file_path.is_file():
                continue
            if should_exclude(file_path, skill_dir):
                continue

            arcname = file_path.relative_to(skill_dir)
            zf.write(file_path, arcname)
            file_count += 1

    size_kb = output_file.stat().st_size / 1024
    print(f"Created: {output_file} ({file_count} files, {size_kb:.1f} KB)")
    return output_file


def main():
    parser = argparse.ArgumentParser(description="Package a skill into a .skill file")
    parser.add_argument("skill_dir", help="Path to skill directory")
    parser.add_argument("--output", "-o", help="Output directory (default: current directory)")
    args = parser.parse_args()

    package_skill(Path(args.skill_dir), Path(args.output) if args.output else None)


if __name__ == "__main__":
    main()
