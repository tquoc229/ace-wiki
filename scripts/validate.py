#!/usr/bin/env python3
"""Validate an llm-wiki bundle (OKF v0.1 conformance + wiki producer lints).

Adapted from the OKF reference validator
(https://github.com/GoogleCloudPlatform/knowledge-catalog) with wiki-aware
file classification (see wiki_common.py) and extra wiki checks.

OKF conformance (ERROR -- spec violations):
  1. Every concept .md begins with a parseable YAML frontmatter block.
  2. That frontmatter contains a non-empty `type` string.
  3. Reserved files (index.md / log.md) carry no frontmatter, except the
     bundle-root index.md, which may declare only `okf_version`.

Producer lints (--strict, exit 1 but NOT spec violations):
  - broken intra-bundle links / links missing the .md extension
  - orphan concepts (not linked from any index or concept)
  - missing recommended fields: title, description, created, updated, tags
  - more than one `type/<layer>` tag; zero layer tags when the wiki uses them
  - concept body longer than --max-lines (default 200)
  - directory missing index.md; concept missing from its directory index
  - raw/ file missing `ingested`/`sha256`; sha256 drift (body was edited)

Usage:
    python validate.py <wiki-path> [--strict] [--max-lines N]

Exit code: 0 = clean, 1 = errors (or lints under --strict), 2 = bad invocation.
Requires PyYAML:  pip install pyyaml
"""
from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

from okf_common import (
    FRONTMATTER_RE,
    extract_links,
    is_external,
    is_nonempty_string,
    parse_frontmatter,
    path_part,
    resolve_link,
)
from wiki_common import classify

try:
    import yaml
except ImportError:
    yaml = None

RECOMMENDED_FIELDS = ("title", "description", "created", "updated", "tags")


def body_after_frontmatter(text):
    """Return the markdown body (everything after the closing '---')."""
    m = FRONTMATTER_RE.match(text)
    return text[m.end():] if m else text


def main(argv=None):
    parser = argparse.ArgumentParser(description="Validate an llm-wiki bundle.")
    parser.add_argument("wiki", help="path to the wiki bundle directory")
    parser.add_argument("--strict", action="store_true",
                        help="also run producer lints and fail (exit 1) on any")
    parser.add_argument("--max-lines", type=int, default=200,
                        help="lint concepts whose body exceeds this many lines")
    args = parser.parse_args(argv)

    if yaml is None:
        print("error: PyYAML is required. Install with: pip install pyyaml",
              file=sys.stderr)
        return 2
    root = Path(args.wiki)
    if not root.is_dir():
        print(f"error: not a directory: {root}", file=sys.stderr)
        return 2

    errors, lints = [], []
    files = sorted(p for p in root.rglob("*.md") if p.is_file())
    kind_by_file = {md: classify(md, root) for md in files}
    concepts = [md for md, k in kind_by_file.items() if k == "concept"]
    text_by_rel = {}
    link_destinations = set()
    layer_tag_users = 0  # concepts carrying a type/<layer> tag

    # Pass 1: conformance + per-file wiki checks + collect link destinations.
    for md in files:
        kind = kind_by_file[md]
        if kind == "skip":
            continue
        rel = md.relative_to(root).as_posix()
        try:
            text = md.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            errors.append((rel, "file is not valid UTF-8"))
            continue
        text_by_rel[rel] = text

        if kind == "concept":
            data, err = parse_frontmatter(text)
            if err:
                errors.append((rel, err))
            elif not is_nonempty_string(data.get("type")):
                errors.append((rel, "frontmatter is missing a non-empty 'type' string"))
            else:
                tags = data.get("tags") or []
                layers = [t for t in tags if isinstance(t, str) and t.startswith("type/")]
                if layers:
                    layer_tag_users += 1
                if args.strict:
                    for field in RECOMMENDED_FIELDS:
                        if field not in data or (
                            isinstance(data.get(field), str)
                            and not data[field].strip()
                        ):
                            lints.append((rel, f"missing recommended field '{field}'"))
                    if len(layers) > 1:
                        lints.append((rel, f"more than one layer tag: {layers}"))
                    body_lines = [ln for ln in body_after_frontmatter(text).splitlines()
                                  if ln.strip()]
                    if len(body_lines) > args.max_lines:
                        lints.append((rel, f"body has {len(body_lines)} non-empty lines "
                                           f"(> {args.max_lines}) -- consider splitting"))

        elif kind == "raw":
            data, err = parse_frontmatter(text)
            if args.strict:
                if err:
                    lints.append((rel, f"raw file: {err}"))
                else:
                    for field in ("ingested", "sha256"):
                        if not is_nonempty_string(str(data.get(field) or "")):
                            lints.append((rel, f"raw file missing '{field}'"))
                    stored = data.get("sha256")
                    if is_nonempty_string(stored):
                        # Canonical hash: body after the closing '---', with
                        # leading blank lines stripped (the ingest convention).
                        digest = hashlib.sha256(
                            body_after_frontmatter(text).lstrip("\n")
                            .encode("utf-8")).hexdigest()
                        if digest != stored.strip():
                            lints.append((rel, "sha256 drift: body no longer matches the "
                                               "stored hash (raw/ is immutable)"))

        elif kind == "reserved":
            is_root_index = md.name == "index.md" and md.parent == root
            if FRONTMATTER_RE.match(text):
                if md.name == "log.md":
                    errors.append((rel, "log.md must not carry a frontmatter block"))
                elif not is_root_index:
                    errors.append((rel, "only the bundle-root index.md may carry frontmatter"))
                else:
                    data, err = parse_frontmatter(text)
                    if err:
                        errors.append((rel, f"root index.md frontmatter is invalid: {err}"))
                    else:
                        extra = [k for k in (data or {}) if k != "okf_version"]
                        if extra:
                            errors.append((rel, "root index.md frontmatter may only declare "
                                                f"okf_version (found: {', '.join(extra)})"))

        # Collect link destinations (log.md history is expected to dangle).
        if md.name != "log.md":
            for target in extract_links(text):
                if is_external(target) or target.startswith("#"):
                    continue
                part = path_part(target)
                if part.endswith(".md"):
                    link_destinations.add(resolve_link(part, md, root).resolve())

    # Pass 2 (--strict): links, orphans, index completeness.
    if args.strict:
        for md in files:
            kind = kind_by_file[md]
            if kind in ("skip", "raw"):
                continue
            rel = md.relative_to(root).as_posix()
            text = text_by_rel.get(rel)
            if text is None:
                continue
            if md.name != "log.md":
                for target in extract_links(text):
                    if is_external(target) or target.startswith("#"):
                        continue
                    part = path_part(target)
                    if part.endswith(".md"):
                        if not resolve_link(part, md, root).resolve().exists():
                            lints.append((rel, f"broken link to '{target}'"))
                    elif part and not part.endswith("/") and (
                        part.startswith("/") or part.startswith("./")
                        or part.startswith("../")
                    ):
                        if "." not in part.rsplit("/", 1)[-1]:
                            lints.append((rel, f"intra-bundle link '{target}' is missing "
                                               "the .md extension"))
            if kind == "concept" and md.resolve() not in link_destinations:
                lints.append((rel, "orphan concept: not reachable from any index.md "
                                   "or linked by any concept"))

        # Index completeness: every concept directory has an index.md that
        # mentions each of its concepts by filename.
        for directory in sorted({md.parent for md in concepts}):
            rel_dir = directory.relative_to(root).as_posix() or "."
            idx = directory / "index.md"
            if not idx.exists():
                lints.append((rel_dir, "directory has concepts but no index.md"))
                continue
            idx_text = idx.read_text(encoding="utf-8")
            for md in concepts:
                if md.parent == directory and md.name not in idx_text:
                    lints.append((md.relative_to(root).as_posix(),
                                  f"not listed in {rel_dir}/index.md"))
        if not (root / "index.md").exists():
            lints.append((".", "bundle has no root index.md"))
        # Layer-tag coverage: if the wiki uses type/<layer> tags, every concept should have one.
        if 0 < layer_tag_users < len(concepts):
            for md in concepts:
                rel = md.relative_to(root).as_posix()
                data, err = parse_frontmatter(text_by_rel.get(rel, ""))
                if not err and data is not None:
                    tags = data.get("tags") or []
                    if not any(isinstance(t, str) and t.startswith("type/") for t in tags):
                        lints.append((rel, "wiki uses layer tags but this page has none"))

    for rel, msg in errors:
        print(f"ERROR  {rel}: {msg}")
    if args.strict:
        if lints:
            print("note: LINTs are producer-quality issues, NOT spec violations; "
                  "consumers MUST tolerate them.")
        for rel, msg in lints:
            print(f"LINT   {rel}: {msg}")

    summary = f"{len(files)} file(s), {len(concepts)} concept(s), {len(errors)} error(s)"
    if args.strict:
        summary += f", {len(lints)} lint(s)"
    print(summary)
    if errors:
        return 1
    if args.strict and lints:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
