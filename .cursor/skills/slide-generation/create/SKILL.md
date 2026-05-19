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

1. **Read the style wiki.** Read `knowledge/style/wiki/index.md`, then read all five pages in full:
   - `layout-patterns.md` — which layout to use for which slide type, placeholder conventions
   - `titles-by-phase.md` — real title examples from good McKinsey decks, by deck phase
   - `structure-patterns.md` — reusable structural sequences (proposal arc, diagnostic sequence, etc.)
   - `style-ai-data-readiness.md` — example deliverable deck
   - `style-faf-p2.md` — example proposal deck
   
   These are your few-shot examples. Draft your slides to match this standard.

2. **Read the outline.** Read `work/sessions/<slug>/outline.md` — this is the structural contract. The slide list, titles, body summaries, and visual placeholders have been agreed with the user. Do not add slides or change the structure.

3. **Draft content before writing code.** For each slide in the outline, expand the one-line body summary into the final title and bullet text. Apply McKinsey communication standards (below) and the style wiki patterns at this stage.

4. **Fill the page.** The One Firm Template is **13.333" wide × 7.500" tall** (confirmed). The Default layout title placeholder is `left=0.607", width=12.120"` — always match this for body text boxes so content spans the full slide width. Available body height is ~5.70" (title + subtitle end at ~1.25"; leave a 0.5" bottom margin). A slide with content clustered at the top and blank space below looks unfinished.

   **The primary lever for page fill is font size, not spacing.** If content doesn't fill the slide, increase font size. Do not increase bullet spacing or padding to fill space — that creates airy, sparse-looking layouts. Account for text wrapping: if annotations are long sentences they will wrap to 2 lines, so either trim them to ~95 characters or increase font size to compensate.

5. **Write and run a Python script** using `python-pptx`:
   - Template: `Presentation("knowledge/style/One Firm Template.pptx")` — always use this file
   - **Remove all built-in template slides first** (the template ships with ~8 placeholder slides that must be deleted before adding yours):
     ```python
     xml_slides = prs.slides._sldIdLst
     for _ in range(len(xml_slides)):
         rId = xml_slides[0].rId
         prs.part.drop_rel(rId)
         del xml_slides[0]
     ```
   - For each slide: use the **layout selection guide** below to pick the correct layout index
   - Set title, subtitle (if applicable), and body text from the drafted content using **placeholder index** — do not match by name (the actual placeholder names in the template do not match the documented names). Use a helper:
     ```python
     def set_ph(slide, idx, text):
         for ph in slide.placeholders:
             if ph.placeholder_format.idx == idx:
                 ph.text_frame.text = text
                 return True
         return False
     ```
   - Populate the **on-page tracker** placeholder on every slide (see below)
   - For slides where the outline specifies `Visual: placeholder: <description>`, insert a grey-box placeholder (see "Visuals" section)
   - Populate the **Title-slide placeholders** for the cover (see below)
   - Save to `work/sessions/<slug>/slide-deck.pptx`

### Layout selection guide

| Slide type | Layout name | Index |
|-----------|-------------|-------|
| Cover | Title | 0 |
| Standard content (default) | Default | 1 |
| Section divider | Section | 4 |
| Agenda / section tracker | 1/4 | 6 |
| Two-column comparison | 1/2 | 8 |
| Opening context slide | 2/3 | 9 |
| Verbatim quote | Quote | 5 |
| Closing slide | End | 13 |

When in doubt, use Default (1) — it is the workhorse of the template.

### Confirmed placeholder indices (One Firm Template)

Use `set_ph(slide, idx, text)` for all placeholder access. Never match by name — the actual names in the template do not match the style wiki documentation.

**Cover slide (layout 0 — Title):**
| idx | Role |
|-----|------|
| 0 | Main title |
| 1 | Subtitle / date line |
| 13 | Document type badge |
| 14 | Client logo (leave empty) |

**Default content slide (layout 1 — Default):**
| idx | Role |
|-----|------|
| 0 | Slide title |
| 1 | Subtitle (framing text below title; leave empty if title is self-sufficient) |
| 17 | On-page tracker (top-right; always populate) |

Example cover population:
```python
set_ph(cover, 0,  "Deck title")
set_ph(cover, 1,  "May 2026")     # date only — ph 13 already carries the document type label
set_ph(cover, 13, "Proposal")
```

Example content slide population:
```python
set_ph(slide, 0,  "Slide title in sentence case")
set_ph(slide, 17, "Section name")   # on-page tracker
# idx 1 (subtitle) — leave empty unless needed
```

### Body text boxes

On the Default layout, add body content as a text box (the template has no pre-built body placeholder). Always match the title placeholder dimensions exactly:
- `left = Inches(0.607)`, `width = Inches(12.120)`
- `top = Inches(1.30)` (just below subtitle), `height = Inches(5.70)`

Keep annotation/supporting text lines to ~95 characters so they fit on a single line at common font sizes. Longer lines wrap and break the spacing calculations.

### Bullet lists — use real PowerPoint bullet characters

Never fake a bullet with an en-dash string (`"–  text"`). Always use real PowerPoint bullet formatting via XML so bullets have proper indentation and render as `•`. Use this helper:

```python
from lxml import etree
from pptx.oxml.ns import qn

def _set_real_bullet(para, indent_inches=0.22):
    """Apply a real PowerPoint bullet (•) to a paragraph via OOXML."""
    pPr = para._p.get_or_add_pPr()
    indent_emu = str(int(indent_inches * 914400))
    pPr.set("marL", indent_emu)
    pPr.set("indent", str(-int(indent_inches * 914400)))
    for tag in ("a:buNone", "a:buChar", "a:buFont", "a:buAutoNum"):
        for el in pPr.findall(qn(tag)):
            pPr.remove(el)
    buFont = etree.SubElement(pPr, qn("a:buFont"))
    buFont.set("typeface", "Arial")
    buFont.set("charset", "0")
    buChar = etree.SubElement(pPr, qn("a:buChar"))
    buChar.set("char", "\u2022")   # •

def add_bullet_tb(slide, l, t, w, h, bullets, size=12, color=None, gap_pt=20):
    txb = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf  = txb.text_frame
    tf.word_wrap = True
    first = True
    for text in bullets:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        p.space_before = Pt(0 if first else gap_pt)
        p.space_after  = Pt(0)
        _set_real_bullet(p)
        run = p.add_run()
        run.text = text
        run.font.size  = Pt(size)
        if color:
            run.font.color.rgb = color
        first = False
    return txb
```

**Bullet font sizing**: Use 12pt as the default bullet size. Never go below 11pt for body bullets.

**Bullet spacing**: Always set `space_before` to 0pt on the first bullet and **3pt** on all subsequent bullets. Do not vary spacing between bullets to try to fill a box — this produces uneven, airy layouts. **Font size is the only correct lever for filling space.** If the content looks sparse, increase font size (12pt → 13pt → 14pt), not gap_pt. The `gap_pt` parameter in `add_bullet_tb` should always be 3.

**Calibrated line-wrap**: At 12pt in a ~3.6" wide column, approximately **38 characters** fit per line (empirically confirmed). PowerPoint's actual line height is approximately `font_pt × 1.35`. Use these to estimate whether a given font size will overflow a fixed-height container before you build.

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

**Sentence case (no Title Case)**
McKinsey uses sentence case in slide titles, not Title Case. Capitalize only the first word and proper nouns. The same rule applies to section headers and any heading-style text on a slide.
- Wrong: "Revenue Fell 18% YoY, Driven By APAC Churn"
- Right: "Revenue fell 18% YoY, driven by APAC churn"

**Parallel structure**
Every set of bullets on a slide must share the same grammatical form. Choose one form (verb-led, noun phrase, etc.) and hold it across all bullets on that slide, and across all titles within a section.

**Active voice**
Default to active voice. Use passive only when the actor is genuinely unknown or irrelevant. When in doubt, write active.

**Selective bolding — almost always apply**
Selective bolding is not always required, but should be used on almost every content slide. When in doubt, add it. The standard:

- **Bold is always at the start of the bullet.** McKinsey writing is bottom line up front — the impact or key phrase leads. Because the conclusion comes first, the bolded words are always the opening of the sentence, never buried in the middle or at the end.
  - Correct: **"Pricing tiers** by customer type, scale, and use case drive the biggest revenue uplift"
  - Wrong: "Revenue uplift is driven by **pricing tiers** defined by customer type and scale"
- **Per bullet**: bold the opening key phrase — typically 2–5 words that capture the main point of that bullet.
- **Per callout box**: bold the opening key phrase of the callout sentence.
- One bolded phrase per bullet maximum. Do not over-bold.
- Do not bold section headers, box titles, or framing questions — those are already visually distinct.
- If you draft a slide and nothing is bolded, strongly reconsider. Absence of bolding is a likely miss.

**Concision**
Trim every bullet to the minimum words needed to convey the meaning. Cut qualifiers, filler phrases, and redundant context. Titles should be one sentence, ideally under 12 words.

**Consistent terminology**
Pick one name for each concept and use it throughout the entire deck. Do not let synonyms drift across slides.

**Punctuation and symbols**
- No em dashes (—). Use a comma, colon, or rewrite the sentence instead.
- No arrows (→, ->, =>) in slide text. Rewrite as a phrase ("which drives", "leading to").
- No plus signs (+) as conjunctions or list separators. Write "and" or use a proper list.
- Use "e.g." for illustrative examples — always wrapped in parentheses as `(e.g., ...)`. The parentheses are part of the convention. Never write `e.g., ...` inline without parentheses. Do not use "such as" or "for example" as substitutes.

## Callout boxes

A callout box is a full-width banner at the bottom of a slide that highlights one key insight or contextualizing note. Use it sparingly — one per slide, maximum.

**Required style (confirmed from example decks):**
- Solid background — McKinsey dark navy (`#002033`; never a light / semi-transparent fill)
- Text is **center-aligned**, white (`#FFFFFF`)
- No left accent bar, no border
- Height must be **proportionate to the text**: use 0.75"–0.85" for one sentence, up to ~1.0" for two sentences. A callout that is much taller than its text looks empty and unprofessional. Do not make the callout taller than needed.
- Font size: **11–12pt** — match the body font size of the slide so the callout reads at the same visual weight as the body. Do not use tiny text (< 11pt) in a large box.
- Spans the full content width (`left=0.607"`, `width=12.120"`)
- One to three sentences maximum. Keep the callout tight.

```python
CALLOUT_BG = RGBColor(0x00, 0x20, 0x33)   # McKinsey dark navy

callout = slide.shapes.add_shape(1,
    Inches(0.607), Inches(CALLOUT_TOP), Inches(12.120), Inches(0.85))
callout.fill.solid()
callout.fill.fore_color.rgb = CALLOUT_BG
callout.line.fill.background()   # no border

tf = callout.text_frame
tf.word_wrap = True
tf.margin_left  = Inches(0.20)
tf.margin_right = Inches(0.20)
tf.margin_top   = Inches(0.12)
tf.margin_bottom = Inches(0.12)

p = tf.paragraphs[0]
p.alignment = PP_ALIGN.CENTER
run = p.add_run()
run.text = "Your insight text here."
run.font.size  = Pt(10.5)
run.font.bold  = False
run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
```

Do not use light-blue backgrounds, left accent stripes, or left-aligned text in callout boxes. Those are not the McKinsey pattern.

## Visuals: use placeholders, do not generate

Never attempt to generate charts, diagrams, images, or other visuals programmatically. The deck is a structural draft; the user will drop in the real visuals afterwards.

When the outline specifies `Visual: placeholder: <description>`, insert a grey rectangle on the slide with centered "PLACEHOLDER: <description>" text. The description must be specific enough that the user knows exactly what to drop in (e.g. "PLACEHOLDER: waterfall chart, FY24 revenue bridge by segment").

```python
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor

def add_placeholder(slide, description, left=Inches(1), top=Inches(2),
                    width=Inches(8), height=Inches(4)):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor(0xD9, 0xD9, 0xD9)
    shape.line.color.rgb = RGBColor(0xBF, 0xBF, 0xBF)
    tf = shape.text_frame
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.text = f"PLACEHOLDER: {description}"
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.font.size = Pt(14)
    p.font.color.rgb = RGBColor(0x59, 0x59, 0x59)
```

Size and position the placeholder to fit the slide's available content area. If the slide is text-plus-visual, scale the placeholder to the right half (or wherever the visual belongs); if visual-only, fill the body area.

## Guardrails

- Only use content retrieved in Phase 1 — do not add facts.
- No speaker notes.
- If `python-pptx` is not installed: `py -m pip install python-pptx`
