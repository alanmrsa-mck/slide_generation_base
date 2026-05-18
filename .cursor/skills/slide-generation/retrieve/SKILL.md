---
name: retrieve
description: Read the wiki in knowledge/content/wiki/ and load relevant content into context for slide generation. Use when gathering source material for slides, or when orchestrate reaches Phase 1.
disable-model-invocation: true
---

# Retrieve

Load relevant content from the wiki at `knowledge/content/wiki/` into context for use in Phase 2.

## Before starting

Read `knowledge/content/SCHEMA.md` to understand wiki structure, page types, and cross-reference conventions.

## Steps

1. Read `knowledge/content/wiki/index.md` to get a catalog of all wiki pages and their one-line summaries.
2. Identify pages relevant to the requested topic — check source summaries, topic pages, and concept/entity pages.
3. Read each relevant page in full.
4. Synthesise the retrieved content in context, noting which wiki page (and ultimately which source PPTX) each piece came from.
5. Flag any gaps: if no relevant wiki content exists for the requested topic, tell the user and suggest running the `ingest` skill on a relevant PPTX in `knowledge/content/raw/`.

## Guardrails

- Do not paraphrase beyond what the wiki pages say.
- All wiki content traces back to source PPTX files in `knowledge/content/raw/` — do not add facts from memory.
- If the wiki is empty or has no relevant pages, do not proceed to Phase 2. Ask the user to ingest content first.
