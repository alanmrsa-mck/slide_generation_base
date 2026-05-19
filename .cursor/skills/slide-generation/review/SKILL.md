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

## Step 1 — Render slides to PNG and visually inspect them

**This step is mandatory and must happen before any text-based analysis.** Do not skip it. Do not rely on code alone to catch layout problems — you must look at the rendered images.

### 1a. Export slides to PNG

Run this script to export every slide as a PNG image:

```python
import sys, pathlib, win32com.client

SLUG     = "<slug>"
BASE     = pathlib.Path(r"c:\Users\Alan Ma\OneDrive - McKinsey & Company\Documents\slide-generation")
pptx     = BASE / "work" / "sessions" / SLUG / "slide-deck.pptx"
out_dir  = BASE / "work" / "sessions" / SLUG / "slides_png"
out_dir.mkdir(exist_ok=True)

ppt = win32com.client.Dispatch("PowerPoint.Application")
ppt.Visible = True
prs = ppt.Presentations.Open(str(pptx.resolve()), ReadOnly=True, Untitled=False, WithWindow=False)
for i in range(1, prs.Slides.Count + 1):
    prs.Slides(i).Export(str(out_dir / f"slide_{i:02d}.png"), "PNG", 1920, 1080)
    print(f"Exported slide {i}")
prs.Close()
ppt.Quit()
```

Alternatively, use the shared utility: `py scripts/render_slides.py work/sessions/<slug>/slide-deck.pptx work/sessions/<slug>/slides_png`

### 1b. Read and visually inspect every PNG

After rendering, read each `slide_XX.png` using the Read tool and look at it with your own eyes. For each slide, explicitly check:

- **Page fill**: Does the content occupy most of the slide? Large blank areas below content are a layout failure. Content should fill at least ~75% of the body area.
- **Text overflow**: Is any text cut off at the edges or bottom of the slide?
- **Width**: Do text boxes and shapes span the full content width (~12.12"), or do they leave a wide margin on one side?
- **Subtitle / cover stacking**: On cover slides, does the subtitle text render cleanly on separate lines, or do elements overlap?
- **Box/table alignment**: Are multi-column layouts evenly spaced? Do boxes align horizontally?
- **Callout boxes**: Is the callout text fully visible and not overflowing its container?
- **Overall visual impression**: Does the slide look like a credible McKinsey deliverable, or does it look amateur/sparse?

Write explicit observations for each slide, e.g.:
> "Slide 2: boxes leave ~30% white space at the bottom — must fix. Cover subtitle text is stacking cleanly."

These visual observations feed directly into the revision brief (internal mode) or user report (final mode).

### 1c. Run code-based layout checks

In addition to the visual inspection, run this Python script to catch measurable issues:

```python
from pptx import Presentation
from pptx.util import Inches

TITLE_W     = 12.120
BODY_TOP    = 1.30
BODY_BOTTOM = 7.00

prs = Presentation("work/sessions/<slug>/slide-deck.pptx")
print(f"Total slides: {len(prs.slides)}")

for i, slide in enumerate(prs.slides, 1):
    print(f"\n=== Slide {i} ===")
    body_shapes = []
    for shape in slide.shapes:
        if shape.has_text_frame:
            for para in shape.text_frame.paragraphs:
                line = "".join(r.text for r in para.runs).strip()
                if line:
                    print(f"  [{shape.name}] {line}")
        if shape.top is not None and shape.top / 914400 > BODY_TOP:
            body_shapes.append(shape)

    for shape in slide.shapes:
        if shape.width is not None and shape.has_text_frame:
            w = shape.width / 914400
            if w < TITLE_W * 0.85:
                print(f"  [LAYOUT WARNING] '{shape.name}' only {w:.2f}\" wide — may not fill slide")

    if body_shapes:
        max_bottom = max((s.top + s.height) / 914400 for s in body_shapes
                         if s.top is not None and s.height is not None)
        fill_pct = (max_bottom - BODY_TOP) / (BODY_BOTTOM - BODY_TOP) * 100
        print(f"  [LAYOUT] Content fills {fill_pct:.0f}% of body (bottom at {max_bottom:.2f}\")")
        if fill_pct < 70:
            print(f"  [LAYOUT WARNING] Only {fill_pct:.0f}% fill — increase font/spacing")
```

Flag any `[LAYOUT WARNING]` lines as must-fix items. Visual observations (1b) take precedence over code output — trust what you see.

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
- Selective bolding should be present on almost every content slide. Flag slides with zero bolding as a **should-fix** (rare exceptions exist, but absence usually means it was forgotten).
- The expected pattern: **one bolded key phrase per bullet**, always at the **beginning** of the bullet. McKinsey writing is bottom line up front — the impact leads, so the bold is always on the opening words, never mid-sentence or at the end. Flag any bolded phrase that does not open the bullet as a must-fix.
- Also bold the opening phrase of any callout box.
- Bold must be on a specific 2–5 word phrase, not an entire bullet or sentence. Flag over-bolded runs (whole bullets bolded) as a must-fix.
- Flag slides with excessive bolding (more than one bolded phrase per bullet) as a should-fix.

**Concision**
- Bullets should be tight. If a bullet can be cut by a third without losing meaning, it must be. Flag verbose bullets.
- Titles should be one punchy sentence. If a title exceeds ~12 words, it is too long.

**Consistent terminology**
- The same concept must be named the same way across all slides. Flag synonym drift (e.g. "customers" on slide 2, "clients" on slide 5, "end-users" on slide 7 — pick one and use it throughout).

**Punctuation and symbols**
- No em dashes (—). Flag any occurrence; suggest a comma, colon, or sentence rewrite.
- No arrows (→, ->, =>) in slide text. Flag and suggest a phrase rewrite ("which drives", "leading to").
- No plus signs (+) as conjunctions or separators. Flag and suggest "and" or a proper list.
- Always `(e.g., ...)` — the parentheses are mandatory. Flag any `e.g.,` that is not wrapped in parentheses, or any use of "such as" or "for example". Flag the absence of closing parenthesis too (e.g., writing `e.g., RAG, memo generation` instead of `(e.g., RAG, memo generation)`).

**Bullet formatting**
- Bullets must use real PowerPoint bullet characters (•), not en-dash or hyphen strings (`–  text`, `- text`). Flag any bullet line that starts with a dash, hyphen, or en-dash character as a must-fix.
- Bullet font should be at least 11pt. Flag anything smaller as a must-fix.
- Bullet `space_before` should be 0pt on the first bullet and 3pt on subsequent bullets. Flag any slide where bullets are spaced more than ~6pt apart — over-spacing is a layout failure, not a solution to sparse content. The fix is always to increase font size, never to increase bullet spacing.

**Callout box style**
- Callout boxes must have a solid dark background (McKinsey dark navy — not light blue, not white, not semi-transparent).
- Callout text must be center-aligned, white. Left-aligned text in a callout box is a style violation.
- Callout height must be proportionate to its text. A callout that is much taller than the text it contains looks empty. Flag oversized callouts (height more than ~2× what the text needs) as a must-fix.
- Callout font must match the body font size (11–12pt). Flag tiny callout text in a large box as a must-fix.
- Flag any callout with a light fill, left accent bar, or left-aligned text as a must-fix.

---

## Step 4 — Output

### If mode is `internal` — Revision Brief

Produce a structured brief to be passed directly to the create skill for the second pass. Do not show this to the user.

```
REVISION BRIEF — Pass 1 → Pass 2

Slide 1 — "<current title>"
  [Must fix] <layout or language issue>. Suggested fix: <specific rewrite or dimension change>
  [Should fix] <issue>. Suggested fix: <specific rewrite>

Slide 3 — "<current title>"
  [Must fix] <issue>. Suggested fix: <specific rewrite>

Terminology: use "<preferred term>" consistently throughout (currently varies: <variants>)

Layout: <any width, fill, or overflow issues flagged by the visual QA script>

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
