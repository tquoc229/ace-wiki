# Ingesting Large & Binary Sources

> Load from `ingest` step ① when the source is binary (docx/pdf/pptx/epub...), larger than
> ~50 KB, or carries embedded base64 images. Goal: **tokens are spent only on distillation —
> never on moving bytes, re-reading, or looking at blobs.**

## Step 0 — probe, don't read

One EXEC call detects the file type, size in tokens, embedded-image load, section structure,
and recommends a strategy (the rest of this file explains each recommendation):

```bash
python <skill-dir>/scripts/ingest_probe.py <file> [--map-limit 60]
```

Trust the probe's recommendation unless the user directs otherwise. Never open a binary file
with READ; never read a file with base64 blobs before stripping.

## Decision table (what the probe auto-detects)

| Source | Technique |
|---|---|
| `.md` / `.txt` | Probe directly → strategy by size (below) |
| `.docx` | `pandoc -f docx -t gfm --wrap=none f.docx -o f.md` (or `markitdown`) → re-probe |
| `.pdf` (text layer) | `pdftotext -layout` or `markitdown` → re-probe |
| `.pdf` (scanned) | Needs OCR — tell the user; don't guess content |
| `.pptx` | `markitdown` (slides + notes) → re-probe |
| `.epub` | `pandoc -f epub -t gfm` → re-probe |
| `.xlsx` / data files | Usually better **queried on demand** (EXEC a script per question) than ingested whole; ingest only the human-written sheets/notes |
| Embedded base64 images | `python <skill-dir>/scripts/strip_images.py <f.md>` → images become real files in `assets/`, markdown shrinks to prose |

Conversion runs through EXEC — the agent never "sees" binary content. If no converter is
available in the runtime, ask the user to export markdown/text (degrade gracefully).

## Strategy by prose size (probe's `est` figure)

- **< ~8K tokens — read whole.** One pass, normal ingest flow.
- **~8K–50K — skeleton read.** Use the probe's section map (line numbers) and read only the
  slices you need via READ offset/limit or `sed -n 'A,Bp'`. Read a slice **once**, distill
  immediately into working notes, write wiki pages from the notes — never re-read the source
  to re-derive what a note already holds.
- **> ~50K — skeleton + multi-session bookmark.** Digest a group of sections per session.
  Record progress in the raw capture's frontmatter (`ingest_status: "partial — sections 01-10
  done"`) and in `log.md`; the next session greps the map and jumps to the bookmark.
- **> ~100K — consider subagent fan-out.** One section per subagent; each returns a distillate
  of a few hundred tokens; the main context never reads the source itself. Total spend is
  similar but the main context stays clean — only worth it at this scale.

## Filing the raw capture

1. Strip/convert **first**, then file the *cleaned* markdown into `raw/` (extracted images go
   to `raw/assets/`, linked relatively). Optionally keep the original binary beside it.
2. Compute `sha256` over the cleaned body **via script** (0 tokens) — convention in
   [templates/frontmatter-template.md](templates/frontmatter-template.md).
3. Big sources add two optional raw-frontmatter fields:
   `ingest_status: partial|complete` and a one-line `ingest_note` bookmark.

## Distill hierarchically — the biggest saving

A 33-chapter ebook is **not** 33 wiki pages. Apply AGENTS.md thresholds top-down:

1. One **map page** (concept) covering the whole source: what it is, its structure, each
   section in 1–2 lines. This alone often satisfies most future queries.
2. Deep pages **only** for sections the user selects (or that clearly cross the 2+ source /
   central-to-source threshold). Human curates, agent files — ask, don't dump.
3. Everything else stays reachable: the map page links the raw capture, and the section map
   (line numbers) can be pasted into the raw file's frontmatter note for later dives.

## Accuracy guardrails (cheap must not mean sloppy)

- **Never write a claim from the skeleton alone** — every claim in a wiki page comes from a
  slice you actually read this session or a note distilled from one.
- **Numbers, named frameworks, and quotes are copied verbatim** from the slice, with a
  provenance marker `^[raw/...]` on synthesized paragraphs.
- Converted tables mangle easily (docx → md): re-check the slice before citing table data.
- Single big source ⇒ pages default to `confidence: medium` until corroborated elsewhere.
- If conversion/OCR quality is doubtful, say so in the page body rather than smoothing it over.
