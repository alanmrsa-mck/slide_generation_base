---
name: orchestrate
description: End-to-end slide deck pipeline. Detects and resumes prior sessions, gathers a brief, aligns on a slide outline before any code runs, then builds via a two-pass create-review loop. Invoke with /orchestrate.
disable-model-invocation: true
---

# Orchestrate

Runs the full deck pipeline: brief → retrieve → align → create → review → revise → final review. Persists `brief.md`, `outline.md`, and `slide-deck.pptx` to `work/sessions/<slug>/` so sessions can be resumed.

## Phase 0 — Brief and session detection

### Step 1 — Detect existing sessions

List the folders in `work/sessions/`. If any exist, ask the user:

> "Is this a new deck, or are you continuing one of these?
>    - <slug-1>
>    - <slug-2>"

- If the user picks an existing session: read `work/sessions/<slug>/brief.md`, summarise it back, and ask "anything to update?" Apply any updates to the file. Then proceed to Phase 1.
- If new (or no existing sessions exist): run Step 2.

### Step 2 — Collect context

Default to collecting context through conversation. Do not jump straight to creation unless every item below is already fully answered by what the user has said. When in doubt, ask — a slide deck built on vague direction wastes everyone's time.

Work through these conversationally — batch related questions where natural; do not interrogate one at a time.

| # | Item | What good looks like |
|---|------|----------------------|
| 1 | **Topic / purpose** | What is this deck about? What decision or action should it drive? |
| 2 | **Audience** | Who is in the room? What do they already know? What do they care about? |
| 3 | **Storyline / angle** | What is the core argument? What should the audience believe or do after seeing this? |
| 4 | **Scope** | Roughly how many slides? Any sections or must-cover topics? Any explicit exclusions? |
| 5 | **Tone** | Formal executive update, working session, external client, internal team? |
| 6 | **Source material** | Which ingested sources are relevant? Any specific findings or data to include? |

### Step 3 — Confirm and persist

Summarise the brief back to the user:

```
Here's what I'm building:

Topic: <topic>
Audience: <audience>
Angle: <core argument>
Scope: <n> slides, covering <sections>
Tone: <tone>
Sources: <list of wiki sources>

Look right?
```

Once confirmed:
1. Build the slug: `<YYYY-MM-DD-topic-slug>` (lowercase kebab-case).
2. Create folder `work/sessions/<slug>/` if it doesn't exist.
3. Write `work/sessions/<slug>/brief.md`:

```markdown
---
created: <YYYY-MM-DD>
topic: <topic>
---

# Brief

**Topic**: <topic>
**Audience**: <audience>
**Angle**: <core argument>
**Scope**: <n> slides, covering <sections>
**Tone**: <tone>
**Sources**: <list of wiki sources>
```

## Phase 1 — Retrieve

Before running retrieve, verify `knowledge/content/wiki/index.md` has relevant pages for the topic.
- If missing, check `knowledge/content/raw/` for un-ingested files and run the `ingest` skill first.
- If `raw/` is also empty, ask the user to add source files before continuing.

Then run the `retrieve` skill. Reads from `knowledge/content/wiki/` and loads relevant content into context.

## Phase 1.5 — Slide alignment

Draft a compact per-deck outline using the brief and retrieved content. Present the full outline to the user in chat in this format:

```markdown
# Outline — <topic>

## Slide 1 — <action title, "so what">
- Body: <one-line summary of bullets>
- Visual: none | placeholder: <description of intended chart/diagram>

## Slide 2 — <action title>
- Body: <...>
- Visual: <...>
```

Then ask: "Look right? Anything to add, remove, or restructure?" Wait for explicit confirmation or redlines before proceeding. Iterate on the outline in chat until the user signs off — this is the cheapest place to restructure.

Once confirmed, write the final outline to `work/sessions/<slug>/outline.md`. This is the contract that `create` will follow.

## Phase 2a — Create (pass 1)

Run the `create` skill in **pass 1** mode. It reads `outline.md` and builds the first draft of `slide-deck.pptx` using the style template, inserting grey-box placeholders where the outline specifies visuals.

## Phase 2b — Internal review

Run the `review` skill in **`internal`** mode. Red-teams the first draft and produces a structured revision brief (must-fix and should-fix items with concrete suggested rewrites). Do not show anything to the user.

## Phase 2c — Create (pass 2)

Run the `create` skill in **pass 2** mode with the revision brief in context. The creator applies every must-fix and should-fix item and regenerates `slide-deck.pptx`.

## Phase 3 — Final check

Run the `review` skill in **`final`** mode. Presents the polished quality report to the user. If zero must-fix issues remain, return the file path. Otherwise, list the issues and ask whether to do another pass or accept the deck as-is.

---

## Standalone utility: Lint

The `lint` skill is not part of the deck generation pipeline but can be run at any time to health-check the wiki. Use it after several ingests or whenever wiki quality is in question. Invoke with `/lint`.
