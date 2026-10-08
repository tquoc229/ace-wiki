# index.md Templates

> Load when initializing a wiki or creating a new directory. **Every directory carries its own
> `index.md`** (OKF progressive disclosure). Two forms:

## Root index (`<wiki>/index.md`)

Carries `okf_version` frontmatter (the ONLY frontmatter allowed on a reserved file) and a
`## Sections` list linking each sub-directory's index. Points to sections, NOT a flat list of
every page. List only sections that actually exist:

```markdown
---
okf_version: "0.1"
---

# Wiki Index

> Navigation map. Start here, then drill into a section's own index.

## Sections

* [Entities](entities/index.md) - people, orgs, products, models
* [Concepts](concepts/index.md) - concepts & topics
* [Sources](raw/index.md) - immutable raw captures (not concepts)
```

## Sub-directory index (e.g. `concepts/index.md`)

**No frontmatter.** A local catalog of that directory's pages, one line each, alphabetical.
The description is **copied from each page's frontmatter** (single source of truth — don't
re-summarize). Links are relative to the index's own directory:

```markdown
# Concepts

* [Employer branding](employer-branding.md) - shaping how an org is seen as a place to work.
* [Happiness at Work](happiness-at-work.md) - a workforce that is engaged, motivated, loyal.
```

## Rules

- Only the bundle-root index carries `okf_version`; sub-directory indexes carry none.
- When a new directory is first created, also create its `index.md` and add it to the parent
  index's `## Sections` list. Never pre-scaffold empty directories.
- **Scaling:** when a section exceeds 50 entries, split by first letter or sub-domain. When the
  whole index exceeds 200 entries, add a `_meta/topic-map.md` grouping pages by theme.
