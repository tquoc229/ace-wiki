# 🧠 ace-wiki — Karpathy's LLM Wiki & Knowledge Graph Skill

> Build, query, and maintain a persistent, compounding markdown knowledge base following **Andrej Karpathy's LLM Wiki pattern** and the **Open Knowledge Format (OKF)**.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Format: OKF](https://img.shields.io/badge/Format-OKF--0.1-blue.svg)](https://github.com/tquoc229)
[![Obsidian](https://img.shields.io/badge/Obsidian-Ready-7C3AED?logo=obsidian&logoColor=white)](https://obsidian.md/)

---

## 🌟 Why `ace-wiki`?

Unlike standard RAG (which rediscovers fragments from scratch per query without building compounding context), `ace-wiki` **compiles knowledge once and keeps it continually updated**:
- **Compounding Knowledge**: Cross-references (`[[wikilinks]]`) are maintained automatically.
- **Contradiction Detection**: Flags conflicting claims across incoming sources instead of silently overwriting.
- **Agent-Agnostic**: Abstracted tool capabilities allow execution across **Claude Code**, **Gemini CLI**, **Hermes**, **Codex**, **Antigravity**, or any shell-enabled environment.
- **Obsidian Native**: Directly opens as an Obsidian vault with graph visualization and Dataview support.

---

## 📂 Architecture: 3 Layers

```text
wiki/
├── AGENTS.md / SCHEMA.md       # Layer 3: Governance rules, tag taxonomy, and operating manual
├── index.md                    # Layer 3: Progressive-disclosure catalog of all pages
├── log.md                      # Layer 3: Append-only chronological action log
│
├── raw/                        # Layer 1: Immutable source material (articles, transcripts, PDFs)
│   ├── articles/
│   ├── papers/
│   └── transcripts/
│
└── wiki/ (or root-level)       # Layer 2: Agent-owned knowledge graph
    ├── concepts/               # Topic & concept explanations
    ├── entities/               # Tools, models, people, companies
    ├── comparisons/            # Side-by-side comparative analyses
    ├── queries/                # Filed deep-dive synthesis answers
    └── output/                 # Deliverable-first publishable content
```

---

## ⚡ Core Commands

| Command | Action | Description |
| :--- | :--- | :--- |
| `wiki init` | **Khởi tạo** | Scaffold a new bundle and establish `AGENTS.md` / `SCHEMA.md` with the user. |
| `wiki ingest <source>` | **Nạp nguồn** | Capture immutable raw source, extract claims, compute `sha256`, and compound into wiki pages. |
| `wiki query <question>` | **Truy vấn** | Index-first Q&A, cite pages with `[[wikilinks]]`, and file novel insights. |
| `wiki save` | **Lưu insight** | File key decisions or concepts directly from the active conversation. |
| `wiki lint` | **Kiểm tra** | Audit wiki health: detect orphan pages, broken links, contradictions, and stale content. |
| `wiki gaps` | **Tìm lỗ hổng** | Automatically discover missing concepts/entities, prioritize them, and propose page creation. |
| `wiki viz` | **Trực quan hóa** | Generate interactive `viz.html` and Mermaid knowledge graph (`graph.mmd`). |

---

## 🛠️ Included Automation Scripts (`scripts/`)

- `validate.py`: Strict conformance checker for OKF links, required frontmatter, orphan detection, and naming rules.
- `visualize.py`: Compiles the markdown graph into standalone interactive `viz.html` and Mermaid graphs.
- `wiki_common.py`: Core parser, frontmatter reader, token estimator, and graph utilities.
- `ingest_probe.py`: Source probe and preliminary claim extractor.
- `okf_common.py`: Open Knowledge Format bundle helpers.
- `strip_images.py`: Strips redundant embedded media to optimize context window size.

---

## 🚀 Quick Setup

### 1. Install as an Agent Skill
Clone or copy this folder into your agent's skills directory:

```bash
# For Claude Code / Generic Agents:
git clone https://github.com/tquoc229/ace-wiki.git ~/.agents/skills/ace-wiki

# Or into an active project:
git clone https://github.com/tquoc229/ace-wiki.git .agents/skills/ace-wiki
```

### 2. Natural Language Trigger
You can interact using natural language in English or Vietnamese:
- *"Khởi tạo wiki mới"* $\rightarrow$ triggers `init`
- *"Ingest transcript bài học B1 vào wiki"* $\rightarrow$ triggers `ingest`
- *"Hỏi wiki về quy tắc quản trị rủi ro"* $\rightarrow$ triggers `query`
- *"Kiểm tra lỗi wiki và tìm các trang mồ côi"* $\rightarrow$ triggers `lint`
- *"Tìm xem wiki còn thiếu những concept quan trọng nào"* $\rightarrow$ triggers `gaps`

---

## 📜 Credits & License

- Based on [Andrej Karpathy's LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).
- Licensed under the [MIT License](LICENSE).
