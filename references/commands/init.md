# wiki init — create a new wiki bundle

**Goal:** scaffold a minimal, OKF-conformant bundle and an AGENTS.md **concretized with the
user** — the schema is built specifically for the domain at init, not copied blindly.

## Steps

1. **Resolve the wiki path** (SKILL.md resolution order). Confirm with the user if ambiguous.
2. **Interview the user — be specific.** You need answers to:
   - What **domain** does this wiki cover? (one sentence)
   - What **language** should pages use?
   - Does it need **layer tags** (knowledge-depth ranking, e.g. the DIKW example)?
     Only content-production wikis usually do — default is NO.
   - 5-10 starter **domain tags** (extend the taxonomy later, in AGENTS.md first).
   - Any tone preferences beyond the encyclopedia default?
3. **Write `AGENTS.md`** from [templates/agents-template.md](../templates/agents-template.md):
   fill the domain, keep or delete the layer-tags example block, seed the domain tag list,
   adjust tone. Delete template blocks the user doesn't need — a lean schema beats a generic one.
4. **Write `index.md`** (root form) and **`log.md`** with an Initialization entry — forms in
   [templates/index-template.md](../templates/index-template.md) and
   [templates/log-template.md](../templates/log-template.md).
5. **Do NOT pre-scaffold** `raw/`, `entities/`, `concepts/`, etc. Create each directory (plus
   its `index.md`, linked from the root `## Sections`) the first time something is filed into it.
6. **Validate:** run `scripts/validate.py <wiki> --strict` (see SKILL.md § Scripts); fix findings.
7. **Confirm** the wiki is ready and suggest first sources to ingest.

## Rules

- AGENTS.md becomes the bundle's **authority** the moment init completes — later skill upgrades
  never silently rewrite it (propose changes to the user instead).
- Three files only at init: `AGENTS.md`, `index.md`, `log.md`. Everything else is on demand.
