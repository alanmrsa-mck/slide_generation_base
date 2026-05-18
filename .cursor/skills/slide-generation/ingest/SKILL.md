---
name: ingest
description: Ingest a source file from knowledge/content/raw/ into the wiki. Supports .pptx, .pdf, .docx, and .txt. Extracts content, writes/updates wiki pages, updates index.md and log.md. Use when a new file has been added to raw/ and needs to be compiled into the wiki before slide generation.
disable-model-invocation: true
---

# Ingest

Process a source file from `knowledge/content/raw/` and integrate its content into the wiki at `knowledge/content/wiki/`.

Supported formats: `.pptx` (primary), `.pdf`, `.docx`, `.txt`.

## Before starting

1. Read `knowledge/content/SCHEMA.md` — all naming conventions, page formats, and workflows are defined there.
2. Confirm which file to ingest (ask the user if not specified).
3. Check that the file exists in `knowledge/content/raw/`. If not, ask the user to place it there first.

## Step 1 — Extract content

Detect the file extension and use the appropriate extraction method.

**`.pptx`** — use `python-pptx`. Output one block per slide:

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

**`.pdf`** — use `pdfplumber`. Output one block per page:

```python
import pdfplumber

with pdfplumber.open("knowledge/content/raw/<filename>.pdf") as pdf:
    for i, page in enumerate(pdf.pages, 1):
        text = page.extract_text() or ""
        print(f"--- Page {i} ---\n{text}\n")
```

**`.docx`** — use `python-docx`. Output paragraphs grouped under headings:

```python
from docx import Document

doc = Document("knowledge/content/raw/<filename>.docx")
for para in doc.paragraphs:
    if para.text.strip():
        print(para.text)
```

**`.txt`** — read directly:

```python
with open("knowledge/content/raw/<filename>.txt", encoding="utf-8") as f:
    print(f.read())
```

Capture the full output in context. Do not paraphrase — use the exact text from the source.

If a required library is missing, install it:
- `pip install python-pptx`
- `pip install pdfplumber`
- `pip install python-docx`

## Step 2 — Write the source summary page

Create `knowledge/content/wiki/source-<slug>.md` where `<slug>` is the filename lowercased with spaces replaced by hyphens, extension dropped.

The page must have the frontmatter block specified in `SCHEMA.md`. Structure the body to match the source format:

- **PPTX**: one section per slide (`### Slide N: <title>`)
- **PDF**: one section per page (`### Page N`)
- **DOCX / TXT**: sections based on headings or logical breaks in the document

```markdown
---
title: <filename or inferred title>
type: source-summary
sources: [<filename>.<ext>]
updated: <YYYY-MM-DD>
---

## Overview

<2-3 sentence summary of the entire source>

## Content

### <Section 1 title>
<key points>

### <Section 2 title>
<key points>
...
```

## Step 3 — Update entity, concept, and topic pages

For each named entity (person, organisation, product, place) or concept (framework, term, idea) mentioned in the source:

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
| [[source-<slug>]] | source-summary | <one-line summary> | <filename>.<ext> | <YYYY-MM-DD> |
```

## Step 6 — Append to log.md

Append an entry to `knowledge/content/wiki/log.md`:

```markdown
## [YYYY-MM-DD] ingest | <filename>.<ext>
- Wrote source-<slug>.md
- Created/updated: <list of pages touched>
- Updated index.md (<N> new entries)
```

## Guardrails

- Never modify files in `knowledge/content/raw/`.
- All claims in wiki pages must trace back to the source file. Do not add facts from memory.
- If the source has already been ingested (a `source-<slug>.md` already exists), ask the user whether to re-ingest (overwrite) or skip.
- If the file extension is not one of `.pptx`, `.pdf`, `.docx`, `.txt`, tell the user it is unsupported and ask them to convert it first.
