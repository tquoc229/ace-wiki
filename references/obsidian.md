# Obsidian & Companion Tooling

> Load only when the user mentions Obsidian, sync, or asks for browsing/search tooling.

## Obsidian Integration

The wiki directory works as an Obsidian vault. Because pages use **relative markdown links**
(not `[[wikilinks]]`), configure Obsidian to match:

- Settings → Files & Links → **New link format: Relative path to file**, and turn
  **"Use [[Wikilinks]]" OFF** so Obsidian creates and resolves `[Title](path.md)` links.
- Graph View and backlinks still work — Obsidian resolves relative markdown links natively.
  (For a no-Obsidian graph, `scripts/visualize.py` emits a self-contained `viz.html`.)
- YAML frontmatter powers Dataview queries, e.g.
  `TABLE tags FROM "entities" WHERE contains(tags, "company")`.
- Set the attachment folder to `raw/assets/` for images; **Obsidian Web Clipper** converts web
  articles to markdown for quick capture into `raw/`.

If you also use an Obsidian integration/skill, point its vault path at the same directory as
the wiki so both operate on one set of files.

## Obsidian Headless (servers / headless machines)

On machines without a display, `obsidian-headless` syncs vaults via Obsidian Sync without a
GUI — the agent writes to the wiki on a server while Obsidian desktop reads it elsewhere.

```bash
# Requires Node.js 22+ and an Obsidian account with Sync
npm install -g obsidian-headless
ob login --email <email> --password '<password>'
ob sync-create-remote --name "LLM Wiki"
cd ~/wiki && ob sync-setup --vault "<vault-id>"
ob sync                # initial sync
ob sync --continuous   # foreground; use a service manager for background
```

**Continuous background sync via systemd (user unit):**

```ini
# ~/.config/systemd/user/obsidian-wiki-sync.service
[Unit]
Description=Obsidian LLM Wiki Sync
After=network-online.target
Wants=network-online.target

[Service]
ExecStart=/path/to/ob sync --continuous
WorkingDirectory=/home/user/wiki
Restart=on-failure
RestartSec=10

[Install]
WantedBy=default.target
```

```bash
systemctl --user daemon-reload
systemctl --user enable --now obsidian-wiki-sync
sudo loginctl enable-linger $USER   # survive logout
```

## Search at scale

At moderate scale (~hundreds of pages) the index files + SEARCH are enough. Beyond that,
[qmd](https://github.com/tobi/qmd) is a local markdown search engine (hybrid BM25/vector,
LLM re-ranking) with both a CLI and an MCP server.

## Related: llm-wiki-compiler

[llm-wiki-compiler](https://github.com/atomicmemory/llm-wiki-compiler) is a Node.js CLI that
batch-compiles sources into a concept wiki (same Karpathy inspiration, Obsidian-compatible).
Use this skill for agent-in-the-loop curation; use the compiler for scheduled batch compiles
of a source directory. Trade-off: the compiler owns page generation and is tuned for small
corpora.
