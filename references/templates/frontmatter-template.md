# Frontmatter Templates

> Load when creating or checking pages. The same spec is seeded into each wiki's
> `AGENTS.md` at init — after init, **that AGENTS.md is the authority for its bundle**.

## Wiki page (concept) frontmatter

```yaml
---
type: entity | concept | comparison | query | summary   # OKF: required, non-empty
title: Page Title
description: One-line summary of what this page covers.   # OKF: required, one sentence
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [<domain-tags...>]              # plus exactly one type/<layer> tag if the wiki uses layer tags
sources: [raw/articles/source-name.md]   # or chat:YYYY-MM-DD for pages filed from conversation
# Optional quality signals:
confidence: high | medium | low        # how well-supported the claims are
contested: true                        # set when the page has unresolved contradictions
contradictions: [other-page-slug]      # pages this one conflicts with
---
```

- `type`, `title`, `description` are the **OKF-required core** — lint fails a page missing any.
  `description` is a single sentence; `index.md` entries copy it verbatim (single source of truth).
- `type:` records page *kind* (entity/concept/...). It is orthogonal to a `type/<layer>` **tag**
  (knowledge-depth layer), if the wiki's AGENTS.md defines layer tags.
- Set `confidence: medium|low` for opinion-heavy, fast-moving, or single-source claims.
  Don't mark `high` unless supported across multiple sources.

## raw/ capture frontmatter

Raw sources get a small frontmatter block so re-ingests can detect drift:

```yaml
---
source_url: https://example.com/article   # original URL, if applicable
ingested: YYYY-MM-DD
sha256: <hex digest — see convention below>
---
```

**sha256 convention (canonical):** hash the body **after the closing `---`, with leading blank
lines stripped** — in shell terms the content that follows the frontmatter block, trimmed of the
empty line(s) that separate it from the frontmatter. `scripts/validate.py` recomputes exactly
this. On re-ingest of the same URL: recompute, compare — skip if identical, flag drift and
update if different.

```bash
# Compute over the body only (after the frontmatter, leading blank lines stripped)
python -c "import sys,re,hashlib; t=open(sys.argv[1],encoding='utf-8').read(); \
print(hashlib.sha256(re.split(r'^---\s*$', t, 2, flags=re.M)[-1].lstrip('\n').encode()).hexdigest())" file.md
# Or simply hash the body text you just wrote, before saving the file.
```
