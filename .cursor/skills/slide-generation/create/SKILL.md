---
name: create
description: Build a .pptx slide deck from retrieved content using the style template. Called in two passes — pass 1 builds the first draft, pass 2 incorporates the internal revision brief from the review skill.
disable-model-invocation: true
---

# Create

Using the content from Phase 1 and the style template, write and run a python-pptx script to produce `slide-deck.pptx`.

## Pass mode

This skill is called twice by orchestrate:

- **Pass 1** — build the first draft from retrieved content. Apply McKinsey communication standards proactively.
- **Pass 2** — a revision brief from the internal review will be in context. Work through every flagged item before regenerating the PPTX.

---

## Pass 1 — First draft

1. Identify the style template in `knowledge/style/` (the `.pptx` file there).
2. Draft the slide content before writing any code. Apply McKinsey communication standards (see below) at this stage — it is far easier to fix language before the PPTX is built than after.
3. Write and run a Python script using `python-pptx` that:
   - Opens the template: `Presentation("knowledge/style/<template>.pptx")`
   - Inspects available slide layouts: `prs.slide_layouts`
   - For each slide: picks the appropriate layout, adds a slide, sets title and body text from the drafted content
   - Saves to `work/sessions/<YYYY-MM-DD-topic-slug>/slide-deck.pptx`
4. Create the session folder before saving if it doesn't exist.

## Pass 2 — Revision

A revision brief from the internal review is in context. Before regenerating the PPTX:

1. Read through every item in the brief in order.
2. For each **Must fix** item: apply the suggested rewrite exactly, or improve on it if you can do better. Do not skip any.
3. For each **Should fix** item: apply the suggested rewrite unless there is a clear reason not to.
4. Apply any deck-wide terminology changes (the brief will specify the preferred term).
5. Once all revisions are applied to the drafted content, regenerate the full PPTX using the same python-pptx approach as Pass 1 — overwrite the existing file.

## McKinsey communication standards

Apply these when drafting every slide title and bullet. The review skill will red-team for violations — fix them here first.

**Top-down communication (impact first)**
Write every slide title as a complete sentence that states the insight or conclusion — not a label or topic. The reader should understand the "so what" from the title alone without reading the bullets.
- Wrong: "Revenue Performance"
- Right: "Revenue fell 18% YoY, driven by APAC churn"

**Parallel structure**
Every set of bullets on a slide must share the same grammatical form. Choose one form (verb-led, noun phrase, etc.) and hold it across all bullets on that slide, and across all titles within a section.

**Active voice**
Default to active voice. Use passive only when the actor is genuinely unknown or irrelevant. When in doubt, write active.

**Selective bolding**
Bold at most one or two key words or phrases per slide — the single most important thing the reader's eye should land on. Do not bold entire bullets. Do not bold nothing.

**Concision**
Trim every bullet to the minimum words needed to convey the meaning. Cut qualifiers, filler phrases, and redundant context. Titles should be one sentence, ideally under 12 words.

**Consistent terminology**
Pick one name for each concept and use it throughout the entire deck. Do not let synonyms drift across slides.

## Guardrails

- Only use content retrieved in Phase 1 — do not add facts.
- No speaker notes.
- If `python-pptx` is not installed: `pip install python-pptx`
