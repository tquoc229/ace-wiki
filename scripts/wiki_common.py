#!/usr/bin/env python3
"""Wiki-specific file classification, shared by validate.py and visualize.py.

An llm-wiki bundle extends plain OKF with files that are NOT concepts:

  AGENTS.md      domain/agent config (the bundle's authority document)
  SCHEMA.md      legacy pre-v4.3 authority document
  README.md      human-facing stub
  _template.*    seed templates copied at page creation
  raw/**         immutable source captures with their own frontmatter
                 (source_url / ingested / sha256 -- no `type`)
  _archive/**    retired pages, kept for history only

Vanilla OKF tooling would flag all of these as non-conformant concepts, so
both scripts classify every .md file through `classify()` first.
"""
from __future__ import annotations

from pathlib import Path

RESERVED = {"index.md", "log.md"}
NON_CONCEPT_NAMES = {"AGENTS.md", "SCHEMA.md", "README.md"}


def classify(md: Path, root: Path) -> str:
    """Classify a markdown file: 'concept' | 'reserved' | 'raw' | 'skip'."""
    parts = md.relative_to(root).parts
    dirs = parts[:-1]
    # Underscore/dot prefixes mark non-concept machinery at any depth:
    # _archive/, _meta/, _template.*, .obsidian/, .git/, ...
    if any(d.startswith(("_", ".")) for d in dirs) or md.name.startswith(("_", ".")):
        return "skip"
    # Name-based classes win over directory-based ones: an index.md inside
    # raw/ is still a reserved navigation file, not a raw capture.
    if md.name in RESERVED:
        return "reserved"
    if md.name in NON_CONCEPT_NAMES:
        return "skip"
    if "raw" in dirs:
        return "raw"
    return "concept"
