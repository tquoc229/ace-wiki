# wiki query — answer from the wiki

**Goal:** answer index-first from compiled knowledge, cite pages, and file valuable answers
back so explorations compound like ingests do.

## Steps

① **READ the root `index.md`**, follow only the relevant section indexes.
② **For wikis with 100+ pages**, also SEARCH across `*.md` for key terms — the index alone
   may miss content. Search by tag (`tags:.*<tag>`) when the taxonomy helps.
③ **READ the relevant pages.** If the wiki ranks knowledge with layer tags (see its AGENTS.md),
   weight higher layers first when synthesizing. Skip `status: superseded`/archived content
   unless the question is historical.
④ **Synthesize an answer**, citing pages with relative links:
   "Based on [page-a](concepts/page-a.md) and [page-b](entities/page-b.md)...".
⑤ **File valuable answers back** — a substantial comparison, deep dive, or novel synthesis
   becomes a page in `queries/` or `comparisons/` (create dir + index on demand). Don't file
   trivial lookups — only answers that would be painful to re-derive.
⑥ **Log** the query in `log.md` (newest-first) and whether it was filed.

## Notes

- Filenames are part of the index: put identifiers (topic, entity, date) in page names so
  SEARCH matches fast.
- If the answer exposes a gap (concept mentioned everywhere, page nowhere), suggest an ingest
  or a new page — don't create it silently from thin air.
