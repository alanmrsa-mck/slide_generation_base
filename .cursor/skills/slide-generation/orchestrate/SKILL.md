---
name: orchestrate
description: End-to-end slide deck pipeline. Defaults to a context-gathering conversation before building anything. Only proceeds to slide creation once all required context is collected. Invoke with /orchestrate.
disable-model-invocation: true
---

# Orchestrate

Runs a context-gathering conversation, then produces a `.pptx` slide deck through a two-pass create-review loop.

## Default mode: Collect context first

**Do not jump straight into slide creation.** Default to collecting context through conversation unless every item in the checklist below is already fully answered by what the user has said. When in doubt, ask — a slide deck built on vague direction wastes everyone's time.

### Context checklist

Work through these conversationally. Ask about multiple items at once where natural; do not interrogate the user one question at a time.

| # | Item | What good looks like |
|---|------|----------------------|
| 1 | **Topic / purpose** | What is this deck about? What decision or action should it drive? |
| 2 | **Audience** | Who is in the room? What do they already know? What do they care about? |
| 3 | **Storyline / angle** | What is the core argument or narrative arc? What should the audience believe or do after seeing this? |
| 4 | **Scope** | Roughly how many slides? Any sections or must-cover topics? Any explicit exclusions? |
| 5 | **Tone** | Formal executive update, working session, external client, internal team? |
| 6 | **Source material** | Which ingested sources are relevant? Any specific findings or data the user wants included? |

### When to proceed without asking

Only skip context-gathering and go straight to Phase 0 if all six items are unambiguously answered by the user's request. This will be rare — default to asking.

### How to signal readiness

Once context is collected, summarise it back to the user in a short brief before proceeding:

```
Here's what I'm building:

Topic: <topic>
Audience: <audience>
Angle: <core argument>
Scope: <n> slides, covering <sections>
Tone: <tone>
Sources: <list of wiki sources to draw from>

Proceeding to build the deck — let me know if anything looks off.
```

Wait for the user to confirm or correct before moving to Phase 0.

---

## Phase 0 — Wiki check

Check that `knowledge/content/wiki/index.md` has relevant pages for the confirmed topic and sources.
- If relevant content is missing, check `knowledge/content/raw/` for uningest files and run the `ingest` skill first.
- If `raw/` is also empty, ask the user to add source files before continuing.

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
