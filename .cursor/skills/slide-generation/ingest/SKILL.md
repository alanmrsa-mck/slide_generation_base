---
name: ingest
description: Ingest a raw PPTX from knowledge/content/raw/ into the wiki. Extracts slide content, writes/updates wiki pages, updates index.md and log.md. Use when a new PPTX has been added to raw/ and needs to be compiled into the wiki before slide generation.
disable-model-invocation: true
---

# Ingest

Process a PPTX from `knowledge/content/raw/` and integrate its content into the wiki at `knowledge/content/wiki/`.

## Before starting

1. Read `knowledge/content/SCHEMA.md` — all naming conventions, page formats, and workflows are defined there.
2. Confirm which PPTX file to ingest (ask the user if not specified).
3. Check that the file exists in `knowledge/content/raw/`. If not, ask the user to place it there first.

## Step 1 — Extract slide content

Write and run a Python script using `python-pptx` to extract all text from the target PPTX:

```python
from pptx import Presentation

path = "knowledge/content/raw/<filename>.pptx"
prs = Presentation(path)
for i, slide in enumerate(prs.slides, 1):
    title = slide.shapes.title.text if slide.shapes.title else "(no title)"
    body = "\n".join(
        shape.text for shape in slide.shapes
        if shape.has_text_frame and shape != slide.shapes.title
    )
    print(f"--- Slide {i}: {title} ---\n{body}\n")
```

Capture the full output in context. Do not paraphrase — use the exact text from the slides.

## Step 2 — Write the source summary page

Create `knowledge/content/wiki/source-<slug>.md` where `<slug>` is the PPTX filename lowercased with spaces replaced by hyphens (drop the `.pptx` extension).

The page must have the frontmatter block specified in `SCHEMA.md`, then a section per slide:

```markdown
---
title: <PPTX filename or inferred title>
type: source-summary
sources: [<filename>.pptx]
updated: <YYYY-MM-DD>
---

## Overview

<2-3 sentence summary of the entire deck>

## Slide-by-slide

### Slide 1: <title>
<key points>

### Slide 2: <title>
<key points>
...
```

## Step 3 — Update entity, concept, and topic pages

For each named entity (person, organisation, product, place) or concept (framework, term, idea) mentioned in the slides:

- If a page already exists in `wiki/`, open it and add the new information under a new section referencing this source.
- If no page exists, create one following the format in `SCHEMA.md`.

For each topic page that overlaps with the ingested content:

- Open the topic page and integrate the new findings, noting where the new source confirms, extends, or contradicts existing claims.

## Step 4 — Update or create overview.md

- If `wiki/overview.md` does not exist, create it with a brief synthesis of the wiki so far.
- If it exists, revise it to reflect anything materially changed by this ingest.

## Step 5 — Update index.md

Add a row to the table in `knowledge/content/wiki/index.md` for the new source summary page (and any newly created entity/concept/topic pages). Format:

```
| [[source-<slug>]] | source-summary | <one-line summary> | <filename>.pptx | <YYYY-MM-DD> |
```

## Step 6 — Append to log.md

Append an entry to `knowledge/content/wiki/log.md`:

```markdown
## [YYYY-MM-DD] ingest | <filename>.pptx
- Wrote source-<slug>.md (<N> slides)
- Created/updated: <list of pages touched>
- Updated index.md (<N> new entries)
```

## Guardrails

- Never modify files in `knowledge/content/raw/`.
- All claims in wiki pages must trace back to the source PPTX. Do not add facts from memory.
- If `python-pptx` is not installed: `pip install python-pptx`
- If the source has already been ingested (a `source-<slug>.md` already exists), ask the user whether to re-ingest (overwrite) or skip.
