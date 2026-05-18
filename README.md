# slide-generation

An AI-assisted pipeline for generating PowerPoint slide decks from a curated content library. Built to run inside Cursor.

## How it works

1. **Ingest content** — drop a source file (`.pptx`, `.pdf`, `.docx`, or `.txt`) into `knowledge/content/raw/` and run `/ingest`. The agent extracts the content and writes structured wiki pages into `knowledge/content/wiki/`.
2. **Ingest style** — drop an example McKinsey deck into `knowledge/style/examples/` and run `/ingest_style`. The agent extracts layout patterns, title conventions, and structural sequences into `knowledge/style/wiki/`.
3. **Orchestrate** — run `/orchestrate`. The agent gathers context, aligns on a slide outline, then builds and red-teams a deck using both the content and style wikis.
4. **Output** — a `.pptx` file is saved to `work/sessions/<YYYY-MM-DD-topic-slug>/slide-deck.pptx`.

## Folder structure

```
knowledge/
├── content/
│   ├── raw/          # Source files (.pptx/.pdf/.docx/.txt, immutable, not committed)
│   ├── wiki/         # LLM-maintained content knowledge base (not committed)
│   └── SCHEMA.md     # Content wiki conventions and workflows
└── style/
    ├── One Firm Template.pptx   # Canonical template (immutable)
    ├── examples/                # Reference decks for style extraction (immutable)
    └── wiki/                    # LLM-maintained style reference (not committed)
                                 # Run /ingest_style to populate from example decks

work/
└── sessions/         # Generated decks, briefs, outlines (not committed)

.cursor/
├── rules/            # Workspace rules for the agent
└── skills/           # Agent skill definitions
                      # (ingest, ingest_style, create, retrieve, review, orchestrate, lint)
```

## Guardrails

- All slide content must originate from files in `knowledge/content/raw/`. The agent does not invent facts.
- Raw PPTX source files are never modified.
- A source must be ingested before its content can be used for generation.
- If content for a topic is missing from the wiki, the agent will say so rather than fill the gap.
