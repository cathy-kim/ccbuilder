#!/usr/bin/env python3
"""Shared utilities for ccbuilder scripts."""

import re
from pathlib import Path


def parse_skill_md(skill_path: Path) -> tuple[str, str, str]:
    """Parse SKILL.md and extract name, description, and full content.

    Handles YAML block scalars (>, |, >-, |-) for multiline descriptions.

    Returns:
        (name, description, full_content)
    """
    content = skill_path.read_text(encoding="utf-8")

    # Extract frontmatter
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        raise ValueError(f"No YAML frontmatter found in {skill_path}")

    frontmatter = match.group(1)

    name = ""
    description = ""

    for line in frontmatter.split("\n"):
        line = line.strip()
        if line.startswith("name:"):
            name = line.split(":", 1)[1].strip().strip('"').strip("'")
        elif line.startswith("description:"):
            desc_value = line.split(":", 1)[1].strip()
            # Handle quoted strings
            if desc_value.startswith('"') and desc_value.endswith('"'):
                description = desc_value[1:-1]
            elif desc_value.startswith("'") and desc_value.endswith("'"):
                description = desc_value[1:-1]
            else:
                description = desc_value

    return name, description, content
