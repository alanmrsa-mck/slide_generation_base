---
name: review
description: Open the generated .pptx, verify content against source files, and red-team every slide for McKinsey communication standards. Called in two modes — internal (between create passes, outputs a revision brief) or final (end of pipeline, outputs a report to the user).
disable-model-invocation: true
---

# Review

Read back the generated `slide-deck.pptx` and red-team it. Approach every slide with maximum skepticism — assume the author is an unreliable first-year analyst who had one hour and no supervision.

## Mode

This skill is called in two modes. The calling context (orchestrate) will specify which:

- **`internal`** — called automatically after the first create pass. Output a structured revision brief for the creator. Do NOT surface anything to the user.
- **`final`** — called after the second create pass. Output the polished report to the user and ask for a decision.

---

## Step 1 — Extract slide content

Write and run a Python script using `python-pptx` to open `work/sessions/<slug>/slide-deck.pptx` and extract all slide text (titles and body bullets).

## Step 2 — Factual integrity check

For each claim on each slide, verify it traces back to content retrieved in Phase 1. Flag any statement that:
- Cannot be sourced to the retrieved content
- Overstates, hedges, or distorts what the source actually says
- Uses weasel qualifiers ("may", "could potentially", "it is possible that") without sourced basis

**Do not flag placeholder shapes** (grey rectangles with "PLACEHOLDER: ..." text). Placeholders are intentional and pre-approved via `outline.md` — the user will drop in the real visual afterwards.

## Step 3 — McKinsey language review

Interrogate every slide as a tough editor would. The standard is high and the bar is exact. Check each of the following:

**Top-down communication (impact first)**
- The slide title must deliver the "so what" — the insight or conclusion, not a label or topic. "Revenue declined" is a label. "Revenue declined 18% YoY, driven by APAC churn" is a message.
- If the title is a noun phrase or a neutral description, it is wrong. Rewrite it as a complete sentence that states the finding.

**Sentence case (no Title Case)**
- Titles, section headers, and other heading-style text must be in sentence case — only the first word and proper nouns capitalized.
- Flag any title written in Title Case (every major word capitalized). This is a hard rule, not a preference.
- Example flag: "Revenue Fell 18% YoY, Driven By APAC Churn" → "Revenue fell 18% YoY, driven by APAC churn"

**Horizontal logic (across slides)**
- Read just the slide titles top-to-bottom. They must form a coherent pyramid-principle argument.
- Each title should ladder up to the deck's overall thesis — typically stated on the executive summary slide near the front.
- Flag titles that break the flow, repeat earlier points without adding new evidence, or introduce ideas with no logical bridge from what precedes them.
- Flag the absence of a thesis-bearing top slide (executive summary or governing thought) for decks longer than ~3 slides.
- Suggest a reordering or retitling if the argument doesn't track.

**Parallel structure**
- Every set of bullets on a slide must be grammatically parallel. If the first bullet starts with a verb, all must start with a verb. If the first is a noun phrase, all are noun phrases. Mixed structure is a failure.
- Check across bullets within a slide and across slide titles within a section.

**Active voice**
- Default to active voice. "The team identified three risks" beats "Three risks were identified."
- Passive is acceptable only when the actor is genuinely unknown or irrelevant. Flag passive constructions and assess whether they are justified.

**Selective bolding**
- Bold should appear at most once or twice per slide, on the single most important word or phrase. Its job is to stop the eye on what matters most.
- Flag slides with no bolding (missed opportunity to guide attention) and slides with excessive bolding (bolding everything means bolding nothing).

**Concision**
- Bullets should be tight. If a bullet can be cut by a third without losing meaning, it must be. Flag verbose bullets.
- Titles should be one punchy sentence. If a title exceeds ~12 words, it is too long.

**Consistent terminology**
- The same concept must be named the same way across all slides. Flag synonym drift (e.g. "customers" on slide 2, "clients" on slide 5, "end-users" on slide 7 — pick one and use it throughout).

---

## Step 4 — Output

### If mode is `internal` — Revision Brief

Produce a structured brief to be passed directly to the create skill for the second pass. Do not show this to the user.

```
REVISION BRIEF — Pass 1 → Pass 2

Slide 1 — "<current title>"
  [Must fix] <issue>. Suggested fix: <specific rewrite>
  [Should fix] <issue>. Suggested fix: <specific rewrite>

Slide 3 — "<current title>"
  [Must fix] <issue>. Suggested fix: <specific rewrite>

Terminology: use "<preferred term>" consistently throughout (currently varies: <variants>)

Overall: <n> must-fix, <n> should-fix
```

Every issue must include a concrete suggested fix — not just a diagnosis. The creator should be able to apply fixes mechanically.

### If mode is `final` — User Report

Present the full report to the user:

```
Deck ready: work/sessions/<slug>/slide-deck.pptx
Slides: <n>

Slide 1 — "<title>"
  [Must fix] <issue>
  [Should fix] <issue>

...

Overall: <n> must-fix, <n> should-fix, <n> consider
Accept, or do another pass?
```

If there are zero must-fix issues: confirm the deck is clean and return the file path without asking.
