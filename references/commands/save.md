# wiki save — file insights from the current conversation

**Goal:** the second ingest path (*authored*, no raw source): capture a conclusion, comparison,
or insight that emerged in chat before it disappears into history.

## Steps

① **Identify and confirm scope with the user** — restate in one or two sentences WHAT insight
   will be saved. Don't save whole conversations; save the distilled conclusion.
② **Dedup against the wiki** — READ the relevant sub-indexes / SEARCH. Three outcomes:
   - **New** → create a page (usual thresholds apply — ≥3 meaningful sentences, anti-thinning).
   - **Reinforces an existing page** → update that page through the ingest update gates
     (re-read first, integrate into prose, bump `updated`).
   - **Contradicts an existing page** → follow AGENTS.md's Update Policy; never overwrite.
③ **Write the page** with normal frontmatter, except provenance:
   - `sources: [chat:YYYY-MM-DD]` — there is no raw file to point to.
   - `confidence: medium` by default (unverified single-conversation claim); `low` if
     speculative. Only `high` when the chat itself cited multiple solid sources.
   - Body notes the origin in one line: *"Filed from a conversation on YYYY-MM-DD."*
④ **Cross-reference** (≥2 relative `.md` links), **update navigation** (directory index +
   log entry `* **Creation**: Filed [Title](path.md) from conversation.`).
⑤ **Report** the file(s) created or updated.

## Rules

- `save` is for *conclusions born in chat*. Content quoted from an external source belongs to
  `ingest` (capture the raw first) — if the user pastes a URL/article mid-chat, route to ingest.
- Later corroboration from real sources should upgrade `confidence` and extend `sources:`.
