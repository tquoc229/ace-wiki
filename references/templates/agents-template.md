# AGENTS.md Seed Template

> Load at `init` only. Copy the block below into `<wiki>/AGENTS.md`, then **concretize it with
> the user**: fill the domain, prune example blocks they don't need, extend the tag taxonomy.
>
> **Seed vs authority:** this template is only the *seed*. Once initialized, the bundle's
> `AGENTS.md` is the **authority for that bundle** — it co-evolves with the user, and when it
> conflicts with a newer version of this skill, AGENTS.md wins. Never "correct" an existing
> wiki's AGENTS.md to match the skill; propose changes to the user instead.

---

```markdown
# Wiki Agent Instructions

## Domain
[What this wiki covers — e.g., "AI/ML research", "personal health", "startup intelligence"]

## Conventions
- File names: lowercase, hyphens, no spaces (e.g., `transformer-architecture.md`)
- Every wiki page starts with YAML frontmatter (see below)
- Link between pages with **relative markdown links** that include `.md`
  (e.g. `[Title](../concepts/other.md)`), minimum 2 outbound links per page. Do NOT use
  `[[wikilinks]]` — relative links resolve in any renderer and pass OKF link validation.
- When updating a page, always bump the `updated` date
- Every new page must be added to its directory's `index.md`; every action to `log.md`
- **Provenance markers:** on pages that synthesize 3+ sources, append `^[raw/articles/source.md]`
  at the end of paragraphs whose claims come from a specific source.

## Frontmatter
```yaml
---
type: entity | concept | comparison | query | summary   # OKF: required, non-empty
title: Page Title
description: One-line summary of what this page covers.  # OKF: required, one sentence
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [<domain-tags...>]          # plus exactly one type/<layer> tag if layer tags are enabled
sources: [raw/articles/source-name.md]
confidence: high | medium | low   # optional quality signal
contested: true                   # optional — unresolved contradictions
contradictions: [other-page-slug] # optional
---
```
Raw captures in `raw/` carry their own block: `source_url`, `ingested`, `sha256` (hash of the
body after the closing `---`, leading blank lines stripped).

## Language
[Set at init — page language + foreign-term policy. Example (Vietnamese wiki):]
- Pages are written in **Vietnamese** (full diacritics, correct orthography).
- English technical terms may remain, glossed in Vietnamese in parentheses on **first
  occurrence per page**: "Employer Branding (xây dựng thương hiệu nhà tuyển dụng)".
- File names stay lowercase-ASCII kebab-case regardless of page language.

## Writing Tone — encyclopedia, not blog
- Neutral register, concrete evidence. No editorial voice ("interestingly", "importantly",
  "groundbreaking", "thú vị là", "đáng chú ý").
- **Attribution over assertion:** "Karpathy describes X as..." instead of "X is amazing".
- Structure articles thematically, not chronologically.
- Emotion and judgment enter only through direct quotes from raw sources; prefer a few
  high-value quotes over many.
- One idea = one sentence. Prefer prose paragraphs; bullets only for true enumerations.

## Tag Taxonomy

### Layer tags (OPTIONAL — delete this block if the wiki doesn't rank knowledge depth)
[Example — a DIKW ladder used by content-production wikis to weight retrieval.
Keep, adapt, or delete at init; if kept, every page carries exactly one:]

| Tag | Layer | Retrieval weight | What belongs here |
|-----|-------|------------------|-------------------|
| `type/wisdom`      | Wisdom      | ×10 | Real stories, lived experience, hard-won judgment |
| `type/knowledge`   | Knowledge   | ×7  | The WHY: insights, frameworks, settled points of view |
| `type/information` | Information | ×3  | The WHAT/HOW: concepts, definitions, explanations |
| `type/data`        | Data        | ×1  | Raw facts: stats, quotes, figures, datapoints |

If a page mixes layers, pick the highest layer it genuinely delivers, or split it.
The layer tag lives in `tags:` and is orthogonal to the `type:` field (page kind).

### Domain tags (one or more per page)
[Define 10-20 top-level domain tags with the user. Add new tags here BEFORE using them.]

Rule: every tag on a page must appear in this taxonomy. New tag → add here first, then use.

## Page Thresholds
- **Create a page** when an entity/concept appears in 2+ sources OR is central to one source
- **Add to existing page** when a source mentions something already covered
- **Anti-thinning:** don't create a page unless you can write ≥3 meaningful sentences about it.
  Every touch of a page must make it richer.
- **Anti-cramming:** when a sub-topic grows to 3+ paragraphs inside a page, split it into its
  own page with cross-links. Split any page exceeding ~200 lines.
- **Archive a page** when fully superseded — move to `_archive/`, remove from index.

## Entity Pages
Overview / key facts and dates / relationships to other entities (relative `.md` links) / sources.

## Concept Pages
Definition / current state of knowledge / open questions / related concepts (relative `.md` links).

## Comparison Pages
What is compared and why / dimensions (table preferred) / verdict / sources.

## Update Policy
When new information conflicts with existing content:
1. Check dates — newer sources generally supersede older ones
2. If genuinely contradictory, note both positions with dates and sources
3. Mark in frontmatter: `contradictions: [page-name]`, optionally `contested: true`
4. Flag for user review in the lint report — never silently overwrite

## Research Program (OPTIONAL — delete if the `autoresearch` skill isn't used)
Read by the `autoresearch` companion skill before each research session.
- **Preferred sources:** official docs, original authors, peer-reviewed / in-depth analyses.
  [Add domain-specific priorities: e.g. arXiv + lab blogs for AI; SEC filings for business.]
- **Banned sources:** forums as primary evidence (link-mining only), SEO spam, undated pages.
- **Recency:** prefer sources <2 years old unless foundational; mark >3-year-old claims as
  possibly outdated.
- **Confidence rubric:** high = multiple independent authoritative sources agree;
  medium = one strong analysis; low = opinion/unverified.
- **Loop budget:** max 3 search rounds/session, max 5 fetched URLs/round. Unanswered
  questions go to the report's "Open Questions", not extra rounds.
```
