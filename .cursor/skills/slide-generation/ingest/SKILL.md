---
name: ingest
description: Ingest a source file from knowledge/content/raw/ into the wiki. Supports .pptx, .pdf, .docx, .txt, and .xlsx. Handles [sticky]-annotated PPTX files. Extracts content, writes/updates wiki pages, updates index.md and log.md. Use when a new file has been added to raw/ and needs to be compiled into the wiki before slide generation.
disable-model-invocation: true
---

# Ingest

Process a source file from `knowledge/content/raw/` and integrate its content into the wiki at `knowledge/content/wiki/`.

Supported formats: `.pptx` (primary), `.pdf`, `.docx`, `.txt`, `.xlsx`, `.md`.

## Before starting

1. Read `knowledge/content/SCHEMA.md` — all naming conventions, page formats, and workflows are defined there.
2. Confirm which file to ingest (ask the user if not specified).
3. Check that the file exists in `knowledge/content/raw/`. **Do not use the Glob tool to list raw/ — filenames containing brackets (e.g. `[sticky] ...`) are silently skipped by Glob. Always use Shell `ls` (or PowerShell `dir`) to list the directory.**
4. If a file has a `[sticky]` prefix, see the special handling section below before proceeding.
5. If a file appears accessible by `ls` but throws `PermissionError` when Python tries to open it, it is likely a locked OneDrive placeholder. Note this in the source page and skip extraction for that file; use the `[sticky]` counterpart if one exists.

## Step 1 — Extract content

Detect the file extension and use the appropriate extraction method. Always use absolute paths when calling Python — relative paths with spaces or brackets in the filename may fail silently.

**`.pptx` (clean version)** — use `python-pptx`. Output one block per slide:

```python
from pptx import Presentation

path = r"<absolute path to file>.pptx"
prs = Presentation(path)
for i, slide in enumerate(prs.slides, 1):
    layout = slide.slide_layout.name
    title = "(no title)"
    subtitle, body_parts = "", []
    for ph in slide.placeholders:
        name = ph.name
        text = ph.text_frame.text.strip() if ph.has_text_frame else ""
        if "Title" in name or ph.placeholder_format.idx == 0:
            title = text
        elif "Subtitle" in name or ph.placeholder_format.idx == 1:
            subtitle = text
        elif text:
            body_parts.append(text)
    print(f"--- Slide {i} [{layout}]: {title} ---")
    if subtitle: print(f"  Subtitle: {subtitle}")
    for bp in body_parts:
        for line in [l.strip() for l in bp.split("\n") if l.strip()][:8]:
            print(f"  > {line[:200]}")
    print()
```

**`[sticky] *.pptx` (sticky-annotated version)** — see the dedicated section below.

**`.xlsx`** — use `openpyxl`. Install if missing: `python -m pip install openpyxl`. Use `read_only=True` to avoid parsing errors with complex workbooks (pivot tables, external links):

```python
import openpyxl

wb = openpyxl.load_workbook(r"<absolute path to file>.xlsx", read_only=True)
print("Sheets:", wb.sheetnames)
for sheet_name in wb.sheetnames:
    ws = wb[sheet_name]
    print(f"\n=== Sheet: {sheet_name} ===")
    for row in ws.iter_rows(values_only=True):
        if any(cell is not None for cell in row):
            print(row)
```

Iterate sheets selectively — most workbooks have many sheets; read headers of each to identify which contain data vs. metadata vs. configuration.

---

## [sticky] PPTX — special extraction

A file named `[sticky] <filename>.pptx` is a deck with team working notes embedded as free-floating text boxes (non-placeholder shapes) placed on top of the normal slide content. These annotations are distinct from the slide's designed placeholder content.

**What to extract:**

1. **Slide structure** — title and subtitle from placeholders (same as a clean PPTX)
2. **Sticky annotations** — text from all non-placeholder shapes with a text frame

Use this script to extract both layers simultaneously:

```python
from pptx import Presentation

path = r"<absolute path to [sticky] file>.pptx"
prs = Presentation(path)
print(f"Total slides: {len(prs.slides)}\n")

for i, slide in enumerate(prs.slides, 1):
    # Placeholder layer (slide content)
    title = "(no title)"
    ph_texts = set()
    for ph in slide.placeholders:
        text = ph.text_frame.text.strip() if ph.has_text_frame else ""
        if "Title" in ph.name or ph.placeholder_format.idx == 0:
            title = text
        if text:
            ph_texts.add(text)

    # Non-placeholder layer (sticky annotations)
    stickies = []
    for shape in slide.shapes:
        if shape.is_placeholder or not shape.has_text_frame:
            continue
        text = shape.text_frame.text.strip()
        if text and text not in ph_texts:
            stickies.append(text)

    if stickies:
        print(f"--- Slide {i}: {title} ---")
        for s in stickies:
            for line in [l.strip() for l in s.replace("\r", "\n").split("\n") if l.strip()]:
                print(f"  [STICKY] {line[:300]}")
        print()
```

**How to interpret the output:**
- Some slides carry their entire tabular or financial content in sticky shapes (the designed placeholder is empty or a title only) — treat this as the primary slide content.
- Other slides have substantive placeholder content with stickies as team annotations, TODOs, or interview notes — record both but distinguish them in the wiki page.
- Stickies prefixed with "TODO", action verbs, or question marks are working-session notes, not factual claims.

**Naming convention for the source page slug:** use the filename without the `[sticky] ` prefix — e.g. `[sticky] 20260522 Comcast IT IDP Internal PS.pptx` → `source-20260522-comcast-it-idp-ps.md`. List both the sticky and clean filenames in the `sources` frontmatter field.

---

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

If a required library is missing, install it (use `python -m pip install` rather than bare `pip` to ensure the right environment):
- `python -m pip install python-pptx`
- `python -m pip install pdfplumber`
- `python -m pip install python-docx`
- `python -m pip install openpyxl`

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
- If the file extension is not one of `.pptx`, `.pdf`, `.docx`, `.txt`, `.xlsx`, `.md`, tell the user it is unsupported and ask them to convert it first.
- **Never use the Glob tool to enumerate `raw/` — use Shell `ls` instead.** Glob silently drops filenames containing brackets such as `[sticky]`.
- **Do not use bare relative paths in Python scripts when the path contains spaces or brackets** — use raw absolute paths (`r"C:\..."`) to avoid `PackageNotFoundError` and similar failures.
- If `openpyxl` throws `TypeError: Nested.from_tree() missing 1 required positional argument` or a similar parse error, retry with `read_only=True` in `load_workbook()`.
- If a file is accessible by `ls` but `PermissionError` is raised when Python opens it, the file is an OneDrive cloud-only placeholder not synced locally. Note this in the wiki and do not block ingestion — use the `[sticky]` counterpart or inform the user to sync the file.
