# wiki gaps — find and fill missing knowledge

**Goal:** scan the wiki for entities/concepts that *deserve* a page but don't have one, rank
candidates, and — only after user approval — create them from material the wiki already holds.
This grows the wiki from within; when material is missing, hand off to the `autoresearch`
skill instead of inventing content.

## Phase 1 — Survey (countable signals first)

Run `python <skill-dir>/scripts/validate.py <wiki> --strict` and mine its output:
- **Broken links** = pages other pages *expect to exist* — the strongest gap signal.
- **Orphans** = existing pages nobody references — the inverse gap (need inbound links).
Then READ the root + section indexes for shape: empty/thin sections, and (if the wiki uses
layer tags) the layer distribution — e.g. concepts rich in `type/information` but with no
`type/wisdom` story to ground them.

## Phase 2 — Mining (judgment: the Concrete Noun Test)

Read the wiki pages (skeleton-style for big wikis) and hunt **concrete nouns** without a page.
Ask: *"X is a ___"* — if a specific noun answers it, X is a candidate.

**Mine:** people, tools/products, orgs, dated events, notable books/papers/videos mentioned in
≥2 pages; recurring concept patterns that cut across pages.
**Don't mine:** generic technologies with no arc in this wiki, single passing mentions,
entities that already have a page.

## Phase 3 — Ranking

Present a table, strongest first:

```markdown
| Candidate | Kind | Mentions | Mentioned in | Proposed home |
|-----------|------|----------|--------------|---------------|
| Evidence Triangulation | concept | 3 (1 broken link) | funnel-probing, bei, ... | concepts/ |
```

Criteria: broken-link target > mentioned in 3+ pages > mentioned in 2 pages. Every candidate
must pass **anti-thinning**: ≥3 meaningful sentences writable from existing material — if not,
list it under "needs sources" instead.

## Phase 4 — Propose and WAIT

Show: strong candidates / potential candidates / suggested comparisons (two existing pages
with comparable roles) / **needs sources** (gaps with no in-wiki material → suggest an
`autoresearch` topic or an ingest). **Never create pages without approval.**

## Phase 5 — Create approved pages

For each approved page: grep every mention across the wiki → gather material (wiki pages +
their `raw/` sources) → write per AGENTS.md (frontmatter, tone, ≥2 outbound links) → add
**backlinks** in the mentioning pages (through the ingest update gates — re-read first,
integrate) → update the directory index → log `* **Creation**: ...`.

**The Golden Rule:** a page is not Wikipedia-about-X. It covers **X's role in *this* wiki's
knowledge** — who mentions it, in what context, why it matters here.

## Phase 6 — Verify

Re-run `validate.py --strict` (new pages must not introduce orphans/broken links), then report:
pages created, backlinks added, remaining gaps parked (with their suggested next action).

## Error handling

| Situation | Action |
|---|---|
| No candidates found | Report "wiki well covered — new raw sources needed to grow"; suggest `autoresearch` topics from the domain |
| Candidate lacks material | Park under "needs sources"; propose `autoresearch`/`ingest` |
| Unclear which section a page belongs to | Ask the user |
