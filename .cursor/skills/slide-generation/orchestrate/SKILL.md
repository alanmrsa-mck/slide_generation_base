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

## Phase 2 — Create

Run the `create` skill.  
Uses content from Phase 1 and the style template from `knowledge/style/` to build `slide-deck.pptx`.

## Phase 3 — Review

Run the `review` skill.  
Reads back `slide-deck.pptx`, verifies content, and returns the file path to the user.  
If issues are found, ask the user whether to fix and re-run Phase 2.
