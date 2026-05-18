---
name: create
description: Build a .pptx slide deck from retrieved content using the style template. Use when creating slides or when orchestrate reaches Phase 2.
disable-model-invocation: true
---

# Create

Using the content from Phase 1 and the style template, write and run a python-pptx script to produce `slide-deck.pptx`.

## Steps

1. Identify the style template in `knowledge/style/` (the `.pptx` file there).
2. Write and run a Python script using `python-pptx` that:
   - Opens the template: `Presentation("knowledge/style/<template>.pptx")`
   - Inspects available slide layouts: `prs.slide_layouts`
   - For each slide: picks the appropriate layout, adds a slide, sets title and body text from the retrieved content
   - Saves to `work/sessions/<YYYY-MM-DD-topic-slug>/slide-deck.pptx`
3. Create the session folder before saving if it doesn't exist.

## Guardrails

- Only use content retrieved in Phase 1 — do not add facts.
- No speaker notes.
- If `python-pptx` is not installed: `pip install python-pptx`
