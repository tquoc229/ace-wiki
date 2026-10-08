# wiki ingest — integrate a source into the wiki

**Goal:** capture the raw source immutably, then compound it into the wiki — updating every
page it genuinely enriches. A single source touching 5-15 pages is normal and desired.

## Steps

① **Capture the raw source:**
   - **Large or binary source?** (docx/pdf/pptx/epub, >~50 KB, or embedded base64 images) →
     load [ingest-large-sources.md](../ingest-large-sources.md) FIRST and follow its pipeline
     (probe → convert/strip via scripts → skeleton read). Never READ a binary or blob-laden
     file directly.
   - URL → FETCH to markdown, WRITE to `raw/articles/`; PDF → `raw/papers/`;
     pasted text / transcript → the fitting `raw/` subdirectory (create dir + index on demand).
   - Name descriptively: `raw/articles/karpathy-llm-wiki-2026.md`.
   - Add raw frontmatter (`source_url`, `ingested`, `sha256`) — hash convention in
     [templates/frontmatter-template.md](../templates/frontmatter-template.md).
   - **Re-ingest of a known URL:** recompute sha256 first — skip if identical, flag drift and
     update if changed.

② **Discuss takeaways** with the user — what matters for the domain. (Skip in automated runs.)

③ **Check what already exists** — READ the relevant sub-indexes and SEARCH for mentioned
   entities/concepts. This is the difference between a compounding wiki and a pile of duplicates.

④ **Write or update wiki pages** (thresholds, tone, and **language policy** live in the
   wiki's AGENTS.md — e.g. page language and how foreign terms are glossed):
   - **New pages** only past the AGENTS.md thresholds (2+ sources or central to one), and only
     if you can write ≥3 meaningful sentences (**anti-thinning**).
   - **Existing pages — update gates (in order):**
     1. **Re-read the whole page first** — non-negotiable.
     2. Ask: *"what depth does the new entry add that the page lacks?"* — if the honest answer
        is "nothing new", **don't touch the page**.
     3. **Integrate into the existing prose** where the topic lives — never just append bullets
        at the end. Refine, don't delete: prior knowledge is folded in, not discarded.
     4. Contradiction? Follow AGENTS.md's Update Policy (note both positions, mark
        `contradictions:`, never silently overwrite).
     5. Bump `updated`.
   - **Anti-cramming:** a sub-topic reaching 3+ paragraphs inside a page → split it out.
   - **Cross-reference:** every new/updated page links ≥2 other pages (relative `.md` links);
     check that related pages link back.
   - **Tags** from AGENTS.md's taxonomy only. **Provenance** markers `^[raw/...]` on pages
     synthesizing 3+ sources. **Confidence** per the frontmatter template.

⑤ **Update navigation:** add new pages to their directory `index.md` (alphabetical, description
   copied from frontmatter); new directory → create its index + link from root `## Sections`;
   add a `log.md` entry (newest-first) listing every file created/updated.

⑥ **Report** every file created or updated. Optionally run `scripts/validate.py <wiki> --strict`.

## Bulk ingest

READ all sources first → identify all entities/concepts across them → one SEARCH pass for
existing pages → create/update in one pass → update indexes once → single log entry.
If an ingest would touch 10+ existing pages, confirm scope with the user first.
