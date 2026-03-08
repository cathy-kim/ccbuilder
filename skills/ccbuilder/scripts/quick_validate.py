#!/usr/bin/env python3
"""quick_validate.py — SKILL.md frontmatter and structure validator.

Validates a SKILL.md file against the ccbuilder rules:
- Valid YAML frontmatter (name, description fields)
- name is kebab-case, max 64 chars
- description max 1024 chars, no angle brackets
- Line count <= 500
- Required sections present

Usage:
    python3 quick_validate.py <path-to-SKILL.md>
    python3 quick_validate.py skills/pdf-analyzer/SKILL.md
"""

import re
import sys
from pathlib import Path


REQUIRED_SECTIONS = ["목적", "사용 시점", "빠른 시작"]
NAME_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MAX_LINES = 500
MAX_NAME_LEN = 64
MAX_DESC_LEN = 1024


def parse_frontmatter(lines: list[str]) -> tuple[dict, list[str]]:
    """Extract YAML frontmatter from lines. Returns (fields_dict, body_lines)."""
    if not lines or lines[0].strip() != "---":
        return {}, lines

    end = None
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end = i
            break

    if end is None:
        return {}, lines

    fm_lines = lines[1:end]
    body = lines[end + 1 :]

    fields: dict = {}
    current_key = None
    current_value_lines: list[str] = []

    for line in fm_lines:
        kv = re.match(r"^([a-zA-Z_][a-zA-Z0-9_-]*):\s*(.*)", line)
        if kv:
            if current_key:
                fields[current_key] = "\n".join(current_value_lines).strip()
            current_key = kv.group(1)
            current_value_lines = [kv.group(2)]
        elif current_key and (line.startswith("  ") or line.startswith("\t")):
            current_value_lines.append(line.strip())
        else:
            if current_key:
                fields[current_key] = "\n".join(current_value_lines).strip()
                current_key = None
                current_value_lines = []

    if current_key:
        fields[current_key] = "\n".join(current_value_lines).strip()

    return fields, body


def validate(path: Path) -> list[str]:
    """Validate SKILL.md at path. Returns list of error messages (empty = pass)."""
    errors: list[str] = []

    if not path.exists():
        return [f"File not found: {path}"]

    lines = path.read_text(encoding="utf-8").splitlines()

    # Line count
    if len(lines) > MAX_LINES:
        errors.append(f"Line count {len(lines)} exceeds limit of {MAX_LINES}")

    # Frontmatter presence
    if not lines or lines[0].strip() != "---":
        errors.append("Missing YAML frontmatter: file must start with ---")
        return errors  # Cannot proceed without frontmatter

    fields, body = parse_frontmatter(lines)

    if not fields:
        errors.append("Frontmatter block is empty or malformed")
        return errors

    # name field
    name = fields.get("name", "")
    if not name:
        errors.append("Frontmatter missing required field: name")
    else:
        if len(name) > MAX_NAME_LEN:
            errors.append(
                f"name '{name}' is {len(name)} chars, exceeds max of {MAX_NAME_LEN}"
            )
        if not NAME_PATTERN.match(name):
            errors.append(
                f"name '{name}' is not kebab-case (lowercase letters, digits, hyphens only)"
            )

    # description field
    desc = fields.get("description", "")
    if not desc:
        errors.append("Frontmatter missing required field: description")
    else:
        if len(desc) > MAX_DESC_LEN:
            errors.append(
                f"description is {len(desc)} chars, exceeds max of {MAX_DESC_LEN}"
            )
        if "<" in desc or ">" in desc:
            errors.append("description must not contain angle brackets (< or >)")

    # Required sections in body
    full_text = "\n".join(body)
    for section in REQUIRED_SECTIONS:
        pattern = re.compile(rf"^#+\s+{re.escape(section)}", re.MULTILINE)
        if not pattern.search(full_text):
            errors.append(f"Missing required section: {section}")

    return errors


def main() -> int:
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <path-to-SKILL.md>")
        return 1

    path = Path(sys.argv[1])
    errors = validate(path)

    if errors:
        print(f"FAIL  {path}")
        for err in errors:
            print(f"  - {err}")
        return 1
    else:
        lines = path.read_text(encoding="utf-8").splitlines()
        print(f"PASS  {path}  ({len(lines)} lines)")
        return 0


if __name__ == "__main__":
    sys.exit(main())
