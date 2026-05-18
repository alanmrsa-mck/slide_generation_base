# slide-generation

An AI-assisted pipeline for generating PowerPoint slide decks from a curated content library. Built to run inside Cursor.

## How it works

1. **Ingest** — drop a `.pptx` source file into `knowledge/content/raw/` and run `/ingest`. The agent reads every slide and writes structured wiki pages into `knowledge/content/wiki/`.
2. **Orchestrate** — run `/orchestrate` with a topic. The agent retrieves relevant wiki content, builds a slide deck using the style template, and reviews it.
3. **Output** — a `.pptx` file is saved to `work/sessions/<YYYY-MM-DD-topic-slug>/slide-deck.pptx`.

## Folder structure

```
knowledge/
├── content/
│   ├── raw/          # Source PPTX files (immutable, not committed)
│   ├── wiki/         # LLM-maintained knowledge base (not committed)
│   └── SCHEMA.md     # Wiki conventions and workflows
└── style/            # Style / template PPTX

work/
└── sessions/         # Generated decks (not committed)

.cursor/
├── rules/            # Workspace rules for the agent
└── skills/           # Agent skill definitions (ingest, create, retrieve, review, orchestrate)
```

## Guardrails

- All slide content must originate from files in `knowledge/content/raw/`. The agent does not invent facts.
- Raw PPTX source files are never modified.
- A source must be ingested before its content can be used for generation.
- If content for a topic is missing from the wiki, the agent will say so rather than fill the gap.
