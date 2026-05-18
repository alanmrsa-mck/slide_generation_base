---
name: review
description: Open the generated .pptx, verify content against source files, and return the deck to the user. Use when reviewing slides or when orchestrate reaches Phase 3.
disable-model-invocation: true
---

# Review

Read back the generated `slide-deck.pptx` and verify it before returning to the user.

## Steps

1. Write and run a Python script using `python-pptx` to open `work/sessions/<slug>/slide-deck.pptx` and extract all slide text (titles and body).
2. Verify:
   - Every claim traces back to content extracted in Phase 1 (no invented facts)
   - Titles are concise
   - No more than 5 bullets per slide
3. If issues found: list them and ask the user whether to fix and regenerate.
4. If clean: return the file path to the user.

## Output to user

```
Deck ready: work/sessions/<slug>/slide-deck.pptx
Slides: <n>
Issues: none  (or list issues)
```
