# slide-generation

An AI-assisted pipeline for generating McKinsey-style PowerPoint decks from a curated content library. Built to run inside Cursor.

## How it works

1. **Ingest content** — drop a source file (`.pptx`, `.pdf`, `.docx`, or `.txt`) into `knowledge/content/raw/` and run `/ingest`. The agent extracts the content and writes structured wiki pages into `knowledge/content/wiki/`.
2. **Ingest style** — drop an example McKinsey deck into `knowledge/style/examples/` and run `/ingest_style`. The agent extracts layout patterns, title conventions, and structural sequences into `knowledge/style/wiki/`.
3. **Orchestrate** — run `/orchestrate`. The agent gathers context, aligns on a brief and slide outline with you, then builds and red-teams the deck using both wikis.
4. **Output** — a `.pptx` file is saved to `work/sessions/<YYYY-MM-DD-topic-slug>/slide-deck.pptx`.

## Key design choices

- **Visual QA in every review pass.** Slides are exported to PNG via PowerPoint COM and read as images before any text-based review. The agent looks at what the slide actually renders as, not just the XML.
- **Two-pass create → review loop.** Every deck gets a first draft, an internal review that produces a revision brief, and a second pass before anything is shown to the user.
- **Style is wiki-driven.** Layout patterns, title conventions, bolding rules, and callout styles are all codified in `knowledge/style/wiki/` — extracted from real McKinsey example decks, not hallucinated.
- **Content only from source.** The agent never invents facts. All claims trace to ingested source files.

## McKinsey style rules (enforced)

- **Sentence case** on all titles — no Title Case.
- **Bottom line up front** — titles state the insight, not the topic. Bullets lead with the key phrase.
- **Selective bolding** — opening phrase of each bullet bolded; callout box opening phrase bolded. Bold is the skimmability lever.
- **Real PowerPoint bullets** (•) via OOXML — never en-dash strings.
- **`(e.g., ...)`** with parentheses always.
- **No em dashes, arrows, or plus signs** as connectors.
- **Font size fills the page**, not bullet spacing. Bullet `space_before` is always 0pt / 3pt.
- **Callouts**: solid dark navy (`#002033`), center-aligned white text, height proportionate to text.

## Folder structure

```
knowledge/
├── content/
│   ├── raw/          # Source files (.pptx/.pdf/.docx/.txt — immutable, not committed)
│   ├── wiki/         # LLM-maintained content knowledge base (not committed)
│   └── SCHEMA.md     # Content wiki conventions and page format
└── style/
    ├── One Firm Template.pptx   # Canonical slide template (immutable)
    ├── examples/                # Reference McKinsey decks for style extraction (immutable)
    └── wiki/                    # LLM-maintained style reference (not committed)
                                 # Populated by /ingest_style

scripts/
└── render_slides.py  # Export any .pptx to PNG via PowerPoint COM (used in review)

work/
└── sessions/         # Per-session output: brief.md, outline.md, slide-deck.pptx (not committed)

.cursor/
├── rules/            # Workspace-level agent rules
└── skills/           # Agent skill definitions
    └── slide-generation/
        ├── orchestrate/  # Top-level coordinator — context gathering, brief, two-pass build
        ├── retrieve/     # Pull relevant content from the wiki
        ├── create/       # Write and run python-pptx scripts to produce .pptx
        ├── review/       # Visual QA + McKinsey language red-team
        ├── ingest/       # Process raw source files into wiki pages
        ├── ingest_style/ # Extract style patterns from example decks
        └── lint/         # Wiki maintenance and consistency checks
```

## Guardrails

- All slide content must originate from files in `knowledge/content/raw/`. The agent does not invent facts.
- Raw source files are never modified.
- A source must be ingested before its content can be used for generation.
- If content for a topic is missing from the wiki, the agent will say so rather than fill the gap.
- Output is always a `.pptx` file. No intermediate formats.
