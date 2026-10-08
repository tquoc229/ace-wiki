---
name: ace-wiki
description: "Karpathy's LLM Wiki: build/query/maintain an interlinked, OKF-conformant markdown knowledge base. Subcommands: init · ingest · query · save · lint · gaps · viz. Use for 'tạo wiki', 'nạp nguồn/ingest vào wiki', 'hỏi wiki', 'lưu insight vào wiki', 'kiểm tra wiki', 'tìm lỗ hổng/mở rộng wiki', or any question against an existing wiki. Agent-agnostic — runs on Claude, Codex, Gemini, Hermes, Antigravity, or any runtime with file + shell access."
license: MIT
metadata:
  version: "4.3.1"
  author: Hermes Agent (original) · adapted to agent-agnostic, OKF-native form
  okf_version: "0.1"
  keywords: [wiki, knowledge-base, okf, ingest, query, lint, research, notes, markdown, rag-alternative, second-brain]
---

# Karpathy's LLM Wiki

Build and maintain a persistent, compounding knowledge base as interlinked markdown files.
Based on [Andrej Karpathy's LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).

Unlike RAG (which rediscovers knowledge from scratch per query), the wiki compiles knowledge
once and keeps it current: cross-references already exist, contradictions are already flagged,
synthesis reflects everything ingested. **Division of labor:** the human curates sources and
directs analysis; the agent summarizes, cross-references, files, and maintains consistency.

## Tool Capabilities (resolve to your runtime, once)

Every operation is described via six abstract capabilities. Map them to your runtime's tools;
any equivalent works. With shell access, the fallback column works everywhere.

| Capability | What it does | Claude Code | Gemini CLI | Hermes | Shell fallback |
|------------|--------------|-------------|------------|--------|----------------|
| **FETCH**  | URL/PDF → markdown | `WebFetch` | `web_fetch` | `web_extract` | `curl -sL <url>` |
| **READ**   | read a file | `Read` | `read_file` | `read_file` | `cat` · `sed -n '1,40p'` |
| **WRITE**  | create/overwrite a file | `Write` | `write_file` | `write_file` | `printf > f` |
| **EDIT**   | modify part of a file | `Edit` | `replace` | `edit_file` | `sed -i` · `>>` |
| **SEARCH** | grep contents / glob names | `Grep`,`Glob` | `search_file_content`,`glob` | `search_files` | `rg` · `grep -rn` · `find` |
| **EXEC**   | run a command | `Bash` | `run_shell_command` | `execute_code` | the shell |

Other runtimes (Codex, Cursor, Windsurf, IDE agents): use their built-in equivalents or the
shell column. If a capability is missing (e.g. no FETCH), degrade gracefully — ask the user to
paste the content and continue.

## Commands

| Command | Description | Reference |
|---|---|---|
| `wiki init` | Scaffold a new bundle; build AGENTS.md **with the user** | [references/commands/init.md](references/commands/init.md) |
| `wiki ingest <source>` | Capture raw + compound into wiki pages | [references/commands/ingest.md](references/commands/ingest.md) |
| `wiki query <question>` | Answer index-first, cite pages, file back | [references/commands/query.md](references/commands/query.md) |
| `wiki save` | File an insight from the current conversation | [references/commands/save.md](references/commands/save.md) |
| `wiki lint` | Health-check: scripted checks + judgment checks | [references/commands/lint.md](references/commands/lint.md) |
| `wiki gaps` | Find missing pages, rank, create after approval | [references/commands/gaps.md](references/commands/gaps.md) |
| `wiki viz` | Regenerate `viz.html` + `graph.mmd` (see § Scripts) | — |

### Routing rules
1. **No argument / just "wiki"** → render the table as a menu and ask.
2. **First word matches a verb** → load its reference file; the rest is the argument.
3. **A URL / file / pasted source with intent to keep** → `ingest`. "Save this / lưu lại
   (insight from chat)" → `save`.
4. **A free question when a wiki exists at the resolved path** → `query`.
5. **"Create/start a wiki or knowledge base"** → `init`; "lint / audit / health-check" → `lint`.
6. **"Wiki thiếu gì / có lỗ hổng gì / mở rộng wiki / expand wiki / find missing pages"** → `gaps`.
7. **Ambiguous** → show the menu; don't guess.

Companion skill: **`ace-research`** (independent) actively searches the web to fill gaps this
wiki can't fill from within — it feeds `raw/` and reports, never writes wiki pages itself.

Load only the matching reference file — the sections below apply to every command.

## Wiki Location

Resolve once per session, in priority order:
1. An explicit path in the request.
2. A `WIKI_PATH` environment variable.
3. A `wiki_path:` line in the nearest `CLAUDE.md` / agent config.
4. A project-local `./wiki` directory, if it exists; else ask, defaulting to `~/wiki`.

The wiki is just a directory of markdown files — no database, no special tooling. It opens as
an Obsidian vault (see [references/obsidian.md](references/obsidian.md) — load only when the
user mentions Obsidian/sync/search tooling).

## Architecture: Three Layers

```
wiki/
├── AGENTS.md           # Layer 3: domain/agent config — THE AUTHORITY for this bundle
├── index.md            # root navigation (okf_version + ## Sections)
├── log.md              # newest-first action log
├── raw/                # Layer 1: immutable source captures (articles/, papers/, ...)
└── entities/ concepts/ comparisons/ queries/   # Layer 2: agent-owned wiki pages
```

- **Layer 1 — raw/**: immutable; the agent reads but never modifies. Not concepts.
- **Layer 2 — the wiki**: agent-owned pages, created/updated/cross-referenced by the agent.
- **Layer 3 — AGENTS.md**: domain, conventions, tag taxonomy, tone, thresholds and local write rules.
- **No pre-scaffolding**: create each directory (with its `index.md`, linked from the parent's
  `## Sections`) the first time something is filed into it.

**AGENTS.md is seed-then-authority:** `init` seeds it from
[references/templates/agents-template.md](references/templates/agents-template.md) and
concretizes it with the user. From then on the bundle's AGENTS.md **wins over this skill**
whenever they disagree — skill upgrades never silently rewrite an existing wiki's schema.

**Legacy compatibility:** if a pre-v4.3 bundle has `SCHEMA.md` but no `AGENTS.md`, read
`SCHEMA.md` as its authority for that operation. Do not create new `SCHEMA.md` files. Rename
to `AGENTS.md` only with owner approval and update live references in the same migration.

## OKF Contract

Every bundle is [Open Knowledge Format](https://github.com/GoogleCloudPlatform/knowledge-catalog)
conformant. Three hard rules (validator ERRORs):
1. Every non-reserved `.md` starts with **parseable YAML frontmatter**.
2. That frontmatter has a **non-empty `type`** string.
3. **Reserved files** (`index.md`, `log.md`) carry no `type`; only the root `index.md` has
   frontmatter, and only `okf_version`.

House conventions (producer lints, not spec violations): relative links **with `.md`** (never
`[[wikilinks]]`); an `index.md` per directory (descriptions copied from page frontmatter);
`log.md` newest-first under `## YYYY-MM-DD` headings; frontmatter core `type`+`title`+
`description` (+`created`/`updated`/`tags`/`sources`). Full specs on demand:
[frontmatter](references/templates/frontmatter-template.md) ·
[index](references/templates/index-template.md) ·
[log](references/templates/log-template.md). `AGENTS.md`, legacy `SCHEMA.md`, `README.md`, `_template.*`, `raw/`
and `_archive/` are **not concepts** — the scripts know this.

## Resuming an Existing Wiki (do this every session)

Before any operation on an existing wiki, orient:
① READ `AGENTS.md` (or legacy `SCHEMA.md` only if needed) → ② READ root `index.md` (what exists) →
③ READ the top ~30 lines of `log.md` (recent activity — it's newest-first).
For large wikis (100+ pages), also SEARCH the topic at hand before creating anything.
Skipping this causes duplicates, missed cross-references, and schema violations.

## Scripts (countable checks; judgment stays with the agent)

`scripts/` ships Python helpers (require **PyYAML**: `pip install pyyaml`), runnable via EXEC:

```bash
python <skill-dir>/scripts/validate.py  <wiki> --strict   # OKF conformance + wiki lints
python <skill-dir>/scripts/visualize.py <wiki> [--title T] # → <wiki>/viz.html + graph.mmd
python <skill-dir>/scripts/ingest_probe.py <file>          # detect type/size/structure → strategy
python <skill-dir>/scripts/strip_images.py <file.md>       # base64 blobs → assets/ files
```

`validate.py` checks: frontmatter/`type`/reserved rules (errors) + broken links, orphans,
missing fields, layer-tag coverage, oversized pages, index completeness, raw sha256 drift
(lints). `visualize.py` renders the concept graph as a self-contained HTML (no network) plus a
Mermaid overview. `ingest_probe.py` + `strip_images.py` power the large/binary-source pipeline
([references/ingest-large-sources.md](references/ingest-large-sources.md) — load from ingest
when a source is binary, >~50 KB, or blob-laden). Boundary: **countable → script; judgment
(contradictions, staleness, relevance) → agent** — see [lint](references/commands/lint.md).
No Python? Lint describes SEARCH-based fallbacks.

## Pitfalls

- **Never modify `raw/`** — corrections go in wiki pages.
- **Always orient first**; **always update index + log** — they're the navigational backbone.
- **No pages for passing mentions**; no page you can't write ≥3 meaningful sentences about.
- **No isolated pages** — every page links ≥2 others.
- **Tags come from AGENTS.md's taxonomy** — add there first, then use.
- **Re-read before updating a page; integrate, don't append; never silently overwrite
  contradictions** (details in [ingest](references/commands/ingest.md)).
- **Ask before mass-updating** (10+ pages) and **rotate the log** at 500 entries.

---

*v3.x made the skill agent-agnostic (abstract capabilities) and OKF-conformant (relative `.md`
links, required `description`, newest-first log). v4.0.0 restructured it per the OKF Skill
Architecture: slim always-on SKILL.md + per-command references + on-demand templates + vendored
OKF validate/visualize scripts (wiki-adapted); added `save` (chat→wiki ingest path), update
gates & anti-cramming/anti-thinning, encyclopedia tone; DIKW layer tags moved from skill law to
AGENTS.md domain config (seed-then-authority). v4.1.0 added the large/binary-source ingest
pipeline: `ingest_probe.py` (auto-detect type/size/structure → strategy) + `strip_images.py`
(base64 blobs → asset files) + `references/ingest-large-sources.md` (conversion recipes,
skeleton reading, multi-session bookmarks, hierarchical distillation, accuracy guardrails).
v4.2.0 added `gaps` (survey → Concrete Noun Test mining → rank → approve → create, with the
Golden Rule "a page covers X's role in this wiki, not Wikipedia-about-X"), the optional
`## Research Program` AGENTS block, and the companion `ace-research` skill (independent,
bounded web-research loop that feeds raw/ and query reports — never concept pages). v4.3.0
renamed the canonical bundle authority to folder-local `AGENTS.md`; legacy `SCHEMA.md` remains
a read-only fallback for pre-migration bundles.*
