---
name: ingest_style
description: Ingest an example deck from knowledge/style/examples/ into the style wiki. Extracts HOW the deck is constructed (layout choices, title patterns, bullet structure, placeholder usage, structural sequences) — not WHAT it says. Invoke with /ingest_style.
disable-model-invocation: true
---

# Ingest style

Process an example PPTX from `knowledge/style/examples/` and compile style pattern pages into `knowledge/style/wiki/`.

This is the style-layer mirror of the `ingest` skill. The key difference: content ingest reads for **what** (facts, arguments, data); style ingest reads for **how** (layout choices, title phrasing, structure, placeholder usage).

## Before starting

1. Confirm which file to ingest (ask the user if not specified).
2. Check that the file exists in `knowledge/style/examples/`. **Do not use the Glob tool to list examples/ — use Shell `ls` instead.** Glob silently drops filenames containing brackets (e.g. `[sticky] ...`).
3. **Never use a `[sticky]`-prefixed file for style ingest.** Sticky-annotated versions contain free-floating text boxes that pollute the layout/placeholder analysis. Always use the clean (non-sticky) version of the deck.
4. If the file throws `PermissionError` when Python opens it, it is an OneDrive cloud-only placeholder. Ask the user to sync the file locally before proceeding.

## Step 1 — Extract deck structure

Write and run a Python script using `python-pptx` to extract the structural metadata from every slide. Use an absolute raw-string path — relative paths with spaces or brackets in the filename may fail:

```python
from pptx import Presentation
from pptx.util import Emu

path = r"<absolute path to file>.pptx"
prs = Presentation(path)

print(f"Slide size: {Emu(prs.slide_width).inches:.2f} x {Emu(prs.slide_height).inches:.2f} in")
print(f"Total slides: {len(prs.slides)}\n")

for i, slide in enumerate(prs.slides, 1):
    layout_name = slide.slide_layout.name
    title = "(no title)"
    subtitle = ""
    tracker = ""
    body_bullets = []

    for ph in slide.placeholders:
        name = ph.name
        text = ph.text_frame.text.strip() if ph.has_text_frame else ""
        if "Title" in name or ph.placeholder_format.idx == 0:
            title = text
        elif "Subtitle" in name or ph.placeholder_format.idx == 1:
            subtitle = text
        elif "tracker" in name.lower():
            tracker = text
        elif text:
            body_bullets.extend([line.strip() for line in text.split("\n") if line.strip()])

    print(f"--- Slide {i} ---")
    print(f"  Layout: {layout_name}")
    print(f"  Title: {title}")
    if subtitle:
        print(f"  Subtitle: {subtitle}")
    if tracker:
        print(f"  On-page tracker: {tracker}")
    if body_bullets:
        print(f"  Body ({len(body_bullets)} bullets):")
        for b in body_bullets[:6]:  # first 6 bullets
            print(f"    - {b[:120]}")
    print()
```

Capture the full output. Do not paraphrase any titles or bullets — use exact text.

## Step 2 — Write the style-source page

Create `knowledge/style/wiki/style-<slug>.md` where `<slug>` is the filename lowercased, spaces replaced with hyphens, extension dropped.

```markdown
---
title: <filename or inferred deck title>
type: style-source
sources: [<filename>.pptx]
updated: <YYYY-MM-DD>
---

## Overview

<2-3 sentences on the deck type (proposal / deliverable / template), audience, and overall structural approach>

## Deck skeleton

<ordered list of slides with layout name and title — the at-a-glance structure>

1. [Title] <title>
2. [Default] <title>
3. [Section] <title>
...

## Layout choices

<For each layout used, note which slide numbers use it and what content type it carries>

## Title patterns

<Group the actual slide titles by deck phase. Use exact text from the deck.>

**Cover / opening**
- <exact title>

**Context / objectives**
- <exact title>

**Executive summary**
- <exact title>

**Approach / workstream**
- <exact title(s)>

**Recommendations / actions**
- <exact title(s)>

**Closing**
- <exact title>

## Subtitle and tracker usage

<How is the Subtitle placeholder used? How is the On-page tracker populated? Note any patterns.>

## Bullet structure patterns

<What grammatical form do bullets use? Verb-led, noun phrases? How many per slide? Any numbering or lettering prefixes?>

## Recurring structural sequences

<If the deck repeats a structural pattern across multiple slides (e.g. "A. Rubric → B. Observations → C. Actions"), document it here as a named pattern that can be reused.>
```

## Step 3 — Update or create layout pattern pages

For each layout used in the deck (`layout-<name>.md`, e.g. `layout-default.md`, `layout-section.md`):

- If the page already exists: add an "observations from `<source>`" section with any new usage patterns seen in this deck.
- If it doesn't exist: create it.

```markdown
---
title: Layout — <name>
type: layout-pattern
sources: [<filename>.pptx, ...]
updated: <YYYY-MM-DD>
---

## Purpose

<When to use this layout — what slide types it's designed for>

## Placeholder map

<List each named placeholder and what typically goes in it>

- **Title** (`2. Slide Title`): <description>
- **Subtitle** (`3. Subtitle`): <description or "unused">
- **On-page tracker** (`1. On-page tracker`): <description>

## Observed usage

### From <source deck slug>
<Specific slide examples from this deck, with exact titles>
```

## Step 4 — Update or create title pattern pages

Group all slide titles by deck phase into a `titles-<phase>.md` page for each phase. If a page exists for that phase, append the new titles under a new source section.

Phases: `cover`, `context`, `executive-summary`, `approach`, `recommendations`, `closing`.

```markdown
---
title: Title patterns — <phase>
type: title-pattern
sources: [<filename>.pptx, ...]
updated: <YYYY-MM-DD>
---

## Pattern

<Describe the structural convention for titles in this phase — sentence structure, level of specificity, typical length>

## Examples

### From <source deck slug>
- "<exact title>"
- "<exact title>"
```

## Step 5 — Update or create structural sequence pages

If the deck uses a named recurring pattern (e.g. "A./B./C. section lettering", "rubric → observations → actions", "workstream → illustrative output" pairing), create or update `structure-<slug>.md`.

```markdown
---
title: Structure pattern — <name>
type: structure-pattern
sources: [<filename>.pptx, ...]
updated: <YYYY-MM-DD>
---

## Description

<What the pattern is and when to use it>

## Sequence

<Step-by-step breakdown>

## Examples

### From <source deck slug>
- Slide N: <title>
- Slide N+1: <title>
```

## Step 6 — Update index.md

Add rows to `knowledge/style/wiki/index.md` for every new or updated page.

```
| [[style-<slug>]] | style-source | <one-line summary> | <filename>.pptx | <YYYY-MM-DD> |
```

## Step 7 — Append to log.md

```markdown
## [YYYY-MM-DD] ingest_style | <filename>.pptx
- Wrote style-<slug>.md (<N> slides)
- Created/updated: <list of pages touched>
- Updated index.md (<N> entries)
```

## Guardrails

- Never modify files in `knowledge/style/examples/` or `knowledge/style/One Firm Template.pptx`.
- Record only structural and stylistic observations — do not record client-confidential content from example decks.
- Never ingest a `[sticky]`-prefixed file for style — sticky shapes pollute the placeholder and layout analysis. Use the clean version only.
- If the file has already been ingested (`style-<slug>.md` exists), ask the user whether to re-ingest (overwrite) or skip.
- If `python-pptx` is not installed: `python -m pip install python-pptx`
- If the file throws `PermissionError`, it is an OneDrive cloud-only placeholder — ask the user to sync it locally first.
