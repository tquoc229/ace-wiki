# wiki lint — health-check the wiki

**Goal:** keep the wiki healthy as it grows. Two halves: **countable checks run as a script**;
**judgment checks the agent performs by reading**. (Boundary: countable → script;
judgment → agent.)

## Part 1 — scripted checks (run first)

```bash
python <skill-dir>/scripts/validate.py <wiki> --strict [--max-lines 200]
```

Covers: OKF conformance (frontmatter parse, non-empty `type`, reserved-file rules) ·
broken/extension-less links · orphan concepts · missing recommended fields
(`title`/`description`/`created`/`updated`/`tags`) · layer-tag coverage and duplicates ·
oversized pages · index completeness (every dir indexed, every page listed) ·
raw/ frontmatter and **sha256 drift** (raw edited or source changed — raw/ is immutable).

No Python available? Approximate with SEARCH: for each page, grep for `](...page.md)` inbound
references (zero hits = orphan); eyeball the rest.

## Part 2 — judgment checks (agent reads, script can't)

① **Contradictions:** pages sharing tags/entities but stating different facts; surface all
   pages with `contested: true` or `contradictions:` for user review.
② **Stale content:** pages whose `updated` is >90 days older than the newest source mentioning
   the same entities.
③ **Quality signals:** list `confidence: low` pages and single-source pages with no confidence
   set — candidates for corroboration or demotion.
④ **Tag audit:** flag tags in use that aren't in AGENTS.md's taxonomy.
⑤ **Coverage gaps (light):** note concepts mentioned across several pages but lacking their
   own page. For the full mining/ranking/creation workflow, run `wiki gaps`
   ([gaps.md](gaps.md)) — lint only *flags*, gaps *fills*.
⑥ **Log rotation:** if `log.md` exceeds 500 entries, rotate to `log-YYYY.md`.

## Part 3 — report & log

- Report findings with file paths and suggested actions, grouped by severity:
  broken links > orphans > source drift > contested > stale > style.
- Fix what the user approves; add `* **Lint**: N issues found, M fixed.` under today's heading
  in `log.md`.

## Maintenance action — archiving

When content is fully superseded or out of scope:
1. Move the page to `_archive/` keeping its sub-path (e.g. `_archive/entities/old.md`).
2. Remove it from its directory `index.md`.
3. Update inbound links — replace with plain text + "(archived)".
4. Log the removal.
