# log.md Template

> Load when initializing a wiki. `log.md` is a reserved file: **no frontmatter**, chronological
> history **newest-first**, grouped under `## YYYY-MM-DD` date headings.

```markdown
# Wiki Log

<!-- Chronological history, NEWEST FIRST. Group entries under a `## YYYY-MM-DD` date heading.
     Each entry:  * **Action**: prose with [links](relative/path.md).
     Convention words: Initialization, Creation, Update, Removal, Fix, Deprecation.
     Historical links may dangle (exempt from the link check). Rotate at 500 entries → log-YYYY.md. -->

## YYYY-MM-DD
* **Initialization**: Created the bundle structure with [AGENTS.md](AGENTS.md), index.md, and log.md. Domain: [domain].
```

## Rules

- New entries go at the TOP (under today's heading; create the heading if missing).
- Convention words: **Initialization / Creation / Update / Removal / Fix / Deprecation** —
  plus **Query** for filed queries and **Lint** for health checks.
- Never rewrite historical entries; dangling links in old entries are expected and exempt
  from link validation.
- **Rotation:** when log.md exceeds 500 entries, rename it `log-YYYY.md` and start fresh
  (check during lint).
