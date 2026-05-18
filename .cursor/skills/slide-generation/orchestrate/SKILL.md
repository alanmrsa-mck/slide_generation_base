---
name: orchestrate
description: End-to-end slide deck pipeline: retrieve content from the wiki, create slides, review and return. Use when asked to build a deck or create slides. Invoke with /orchestrate.
disable-model-invocation: true
---

# Orchestrate

Runs three skills in sequence to produce a `.pptx` slide deck.

## Before starting

1. Confirm the topic with the user.
2. Check that `knowledge/content/wiki/index.md` has relevant pages for the topic.
   - If the wiki is empty or missing relevant content, check whether there are uningest PPTX files in `knowledge/content/raw/`.
   - If there are, run the `ingest` skill first, then proceed.
   - If `raw/` is also empty, ask the user to add source PPTX files to `knowledge/content/raw/` and ingest them before continuing.

## Phase 1 — Retrieve

Run the `retrieve` skill.  
Reads from `knowledge/content/wiki/` and loads relevant content into context.

## Phase 2a — Create (pass 1)

Run the `create` skill in **pass 1** mode.  
Uses content from Phase 1 and the style template from `knowledge/style/` to build the first draft of `slide-deck.pptx`.

## Phase 2b — Internal review

Run the `review` skill in **`internal`** mode.  
Red-teams the first draft and produces a structured revision brief (must-fix and should-fix items with concrete suggested rewrites). Do not show anything to the user at this stage.

## Phase 2c — Create (pass 2)

Run the `create` skill in **pass 2** mode, with the revision brief from Phase 2b in context.  
The creator applies every must-fix and should-fix item and regenerates `slide-deck.pptx`.

## Phase 3 — Final check

Run the `review` skill in **`final`** mode.  
Presents the full quality report to the user. If zero must-fix issues remain, return the file path without asking. If must-fix issues remain, list them and ask the user whether to do another pass or accept the deck as-is.

---

## Standalone utility: Lint

The `lint` skill is not part of the deck generation pipeline but can be run at any time to health-check the wiki. Use it after several ingests or whenever wiki quality is in question. Invoke with `/lint`.
