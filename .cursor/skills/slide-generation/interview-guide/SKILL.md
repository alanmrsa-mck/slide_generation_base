---
name: interview-guide
description: Synthesizes a high-level verbal interview guide for one named stakeholder from an IT-excellence survey owner-mapping Excel and a benchmark-question workbook (~250 items across multiple sheets). Produces a topic-bucketed markdown guide with source-coverage mapping and a slide-friendly summary of the question text. Use when prepping a VP-level interview for an IT diagnostic or similar engagement. Invoke with /interview-guide.
disable-model-invocation: true
---

# Interview Guide

Synthesize a verbal interview guide for one named stakeholder. Output should not feel like a survey — it should read like a peer-to-peer conversation that happens to cover every relevant survey + benchmark item the engagement needs.

The guide is the **source of truth** for the interview content. The slide-friendly summary is a derived view — same questions, no coverage tables.

---

## Step 1 — Gather inputs

**Required from the user:**

1. **Stakeholder name and role** (e.g., "Ken Landry, VP Architecture")
2. **Owner-mapping Excel path** — the survey workbook with one column per stakeholder showing which questions each one owns or co-owns
3. **Benchmark workbook path** — the McKinsey IT Benchmarks workbook (or equivalent), typically ~250 questions across sheets like *TechFwd Maturity*, *KPIs*, *ADM&Arch*, *Tech*, *Infra*, *Mgmt&Sourcing*

**Optional but use if available:**

- Example interview guide (PDF / markdown) for format reference
- Wiki entry for the stakeholder at `knowledge/content/wiki/entity-<slug>.md` — auto-load if present
- Wiki concepts and topic pages relevant to the engagement (e.g., `concept-build-vs-buy.md`, `topic-<engagement>-transformation-framework.md`) — these anchor the strategic-close questions in real engagement themes

If a required input is missing, ask before proceeding. Do not guess paths.

---

## Step 2 — Identify scope and route out-of-scope items

Read the wiki entry (if present) to anchor on the stakeholder's primary domain. Use the role title to infer if no wiki exists.

**Filter the owner-mapping Excel:**
- Pull every question where the stakeholder is owner or co-owner
- Note co-owners explicitly — these become coordination items in the guide ("co-owned w/ [other stakeholder]")

**Filter the benchmark workbook:**
- Walk each sheet question-by-question
- Assign each item to the natural owner by domain (table below)
- Items NOT in the stakeholder's domain → mark for the appendix as "out of scope → [other stakeholder]"

**Domain routing defaults** (adjust to engagement reality):

| Domain | Natural owner |
|---|---|
| Architecture (target state, blueprint, modularity, reuse, rationalization, governance) | VP Architecture |
| Engineering practices (CI/CD, testing, agile maturity, code quality, DevOps) | VP Engineering |
| Data architecture, data governance, AI / ML rollout | Chief Data Officer |
| Production reliability (DR, incident, monitoring, SRE, availability) | VP Production Reliability |
| Cloud platform, infrastructure ops, FinOps, EUC, network | VP Infrastructure |
| Sourcing, vendor commercial terms, talent, org structure | VP Sourcing / CHRO |
| Demand management, project portfolio, business-IT relationship | Head of Delivery |

When ownership is genuinely ambiguous (e.g., infrastructure standardization can sit with architecture *or* infra), ask the user which way to route.

---

## Step 3 — Synthesize, don't enumerate

The single biggest failure mode is producing 30+ literal survey questions strung together. Do not do this.

**Synthesis principles:**

- **Combine related items into one question.** Blueprint existence + adherence + capability coverage + inventory comprehensiveness = one *Architecture core* question.
- **One question per "natural breath."** If a probe covers blueprint + adherence + coverage %, that's one question. If it tries to cover blueprint + governance approvals, split.
- **Lead with the conclusion-seeking question, not the topic label.** ✅ "How rigorously do new builds adhere to the blueprint?" ❌ "Tell me about your reference architecture."
- **Concrete examples in parens anchor the question.** ✅ "(e.g., one ADSL service across bundles)" beats ❌ "(across the product catalog)".
- **Open-ended, not yes/no.** ✅ "What happens when standards are violated?" ❌ "Are there compliance reviews?"
- **Translate consultant jargon inline.** "2-speed IT" becomes "can the front end move at one speed while core systems move at another (2-speed IT)". Don't assume the stakeholder will read the acronym the way you mean it.

Aim for **20-28 questions total** for a 60-90 minute VP interview. If the user has set a cap (e.g., 25), respect it and propose drop candidates beyond it.

---

## Step 4 — Bucket into topic-flavored sections

Use **6-8 buckets** organized around the natural conversational arc, not around source-document structure. Default arc:

| # | Bucket | Count | Purpose |
|---|---|---|---|
| 1 | **General** | 3 | Role, top pains, what's working — weight the rest of the conversation |
| 2 | **[Domain landscape]** | 3-5 | What exists today — counts, vendors, current footprint |
| 3 | **[Strategy / target state]** | 3-5 | Where you're headed, transformation approach, estate health |
| 4 | **[Domain core]** | 3 | Depth on the highest-leverage domain dimension |
| 5 | **[Quality dimension]** | 3 | Second-leverage dimension (e.g., reusability for architecture) |
| 6 | **Governance** | 3-5 | How decisions get made and enforced |
| 7 | **Operating model** | 2-4 | How the function is structured and runs |
| 8 | **Strategic outlook** | 2-3 | Vision, build-vs-buy, time-to-market — **always include** |

**Adapt bucket names to the stakeholder.** Use topic-flavored labels, not abstract ones:

| Stakeholder type | Bucket 4-5 names |
|---|---|
| VP Architecture | Architecture core / Reusability |
| VP Production Reliability | Resilience / Incident management |
| Chief Data Officer | Data architecture / Data quality |
| VP Engineering | Engineering practices / Delivery cadence |
| VP Sourcing | Vendor management / Talent |

Place each synthesized question in exactly one bucket. If a question genuinely straddles two (e.g., functional fragmentation = consolidation + reusability), pick the bucket where it answers the higher-leverage question.

---

## Step 5 — Apply exec-friendly wording

Treat each question as VP-to-VP language. Run every question through these checks:

| Pattern | Replace with |
|---|---|
| "Can you briefly describe..." | "Walk me through..." |
| "How well X" / "How clearly X" / "How seriously X" | Specific probe with examples |
| Bare "industry standards" | Name the standards type (e.g., TM Forum, REST/OAuth, TOGAF) |
| Yes/no questions | Open-ended ("What happens when X?") |
| Two unrelated questions glued together | Split into two bullets |
| Acronyms without translation | Translate inline (e.g., "AIB" → "Architecture Integration Board") |
| McKinsey shorthand (CMM, AIB, SOA, 2-speed IT, BAM) | Translate or pair with example |
| "B2C / B2B" | Use the client's vocabulary (e.g., "Residential / Business") |
| "Tell me about..." | Replace with a focused question; "Tell me about" invites monologue |
| Three+ questions in one breath | Split |
| Em-dashes (—) in question text | Use a comma, colon, parens, or short clause instead |

Apply McKinsey writing style from `.cursor/rules/mck-writing-style.mdc` — top-down, short and specific, parallel construction. Slide-friendly questions especially must follow this rule (no em-dashes on slides). Markdown guide questions can be slightly looser since they are a working document, not a deliverable, but stay consistent within a guide.

---

## Step 6 — Add the strategic close

**Always include a closing bucket with 2-3 forward-looking questions.** These are usually the highest-leverage questions of the interview. They are not optional even if the source items don't explicitly map to them.

The three reliable strategic-close patterns:

1. **Time-to-market through the function's lens** — "For [a large business move], how long does it really take, and what is the [function]-side bottleneck?" This is where Ken's architecture-side TTM bottleneck is different from Kevin's commerce-side TTM view.

2. **Vision and go-forward path** — "Where does [function] need to be in 2-3 years, and which path fits — [option A], [option B], or [option C]?" Ground the options in real engagement debates from the wiki (e.g., for Comcast architecture: clean-sheet build-and-migrate vs. agentic overlay vs. cap-and-grow — see `topic-comcast-it-transformation-framework`).

3. **A philosophical question grounded in engagement themes** — pull from wiki concepts (e.g., `concept-build-vs-buy` for architecture; an analogous philosophical tension for other functions). For data: centralized vs. federated ownership. For production: resilience-as-code vs. operational excellence.

**Always check the wiki for relevant concepts before drafting these.** A philosophical question grounded in a documented engagement theme is far more leveraged than a generic "what's your vision" prompt.

---

## Step 7 — Generate output files

Save to `work/sessions/YYYY-MM-DD-<stakeholder-slug>-interview/`. Two files:

### File 1: `<stakeholder-slug>-interview-guide.md`

Use this template:

```markdown
# [Stakeholder name] interview guide
**[Role title — Org context]**
Verbal conversation designed to cover [stakeholder]'s [N] survey items, ~[M] benchmark items, and [engagement-specific themes] without the survey feel.

---

## How to use this guide

- Questions are open-ended on purpose. Take notes verbatim, especially [domain-specific items: vendor names, counts, %s, timelines].
- After each section, the **Coverage** boxes show which items from the survey and benchmark workbook the section answers. Score those items yourself post-meeting.
- [One-paragraph stakeholder context — role, scope, what to anchor on. Use wiki entry if present.]
- [Out-of-scope routing — what's owned by other stakeholders and will be picked up elsewhere. List by domain → name.]
- [N] substantive questions. Full conversation = 60-90 min if every question lands; aim for 60-75 min and use the drop priority below if you run long.
- **Drop priority (cut in this order):** Q-A → Q-B → Q-C. Always keep [list essential Qs].

---

## 1. [Bucket name]

[1-2 line section intent — what this bucket is trying to surface and why.]

**Questions**

- **Q-1.** [Question text.]
- **Q-2.** [Question text.]

**Notes**

_______________________________________________________________________________________________________

**Coverage**

| Source | Item | Topic |
|---|---|---|
| Survey | QXX | [topic] |
| Benchmark | — | [topic] |
| Wiki | — | [topic, if grounded in a wiki concept] |

---

[Repeat for each bucket]

---

## Appendix A: Excel-to-guide mapping (original survey)

| Excel Q # | Question (abbrev.) | Guide section |
|---|---|---|
| QXX | [abbrev question text, note co-owners] | §N (Q-N) |

---

## Appendix B: Benchmark-to-guide mapping

| # | Benchmark question | Status | Guide |
|---|---|---|---|
| 1 | [...] | Already covered | §N (Q-N) |
| 2 | [...] | Tightened | §N (Q-N) |
| 3 | [...] | Out of scope | → [other stakeholder] |

**Status options:**
- *Already covered* — current question wording captures it
- *Tightened* — current question explicitly mentions this probe inline
- *Split into own question* — given enough leverage to be its own bullet
- *Out of scope* — routed to another stakeholder (always name them)

**Totals:** [X] already covered, [Y] tightened, [Z] split, [W] routed.

---

## Appendix C: Themes added beyond source items

| Theme | Source | Where in guide |
|---|---|---|
| [e.g., Time-to-market through architecture lens] | [Wiki / engagement debate] | §N (Q-N) |
```

### File 2: `<stakeholder-slug>-slide-questions.md`

Slide-friendly summary — bucket names + question text only, no coverage tables, no Q-numbers (slides typically show only the question text). This is what gets pasted into the slide deck.

```markdown
# [Stakeholder name] — slide question content

## [Bucket 1 name]

- [Question]
- [Question]

## [Bucket 2 name]

- [Question]
```

---

## Step 8 — Validate before declaring done

Run through this checklist:

- [ ] Every survey question owned by the stakeholder appears in Appendix A with a guide section
- [ ] Every benchmark item in the stakeholder's domain appears in Appendix B with status (covered / tightened / split / out of scope)
- [ ] Every "Out of scope" routing names the receiving stakeholder explicitly
- [ ] Strategic close bucket (Step 6) is present with 2-3 questions
- [ ] At least one strategic-close question is grounded in a wiki concept or engagement theme
- [ ] Drop priority always-keep list includes: opener, survey-mandated 1-5 score items, sensitive engagement-driven probes (from wiki), and the strategic close
- [ ] Question count is 20-28; if at the high end, propose 2-3 drop candidates so the user can trim
- [ ] No question violates the wording anti-patterns in Step 5
- [ ] Slide-friendly summary file mirrors the guide's question text exactly (bucket names match, wording matches)

---

## Wording anti-patterns (do not produce)

- "How well X..." / "How clearly X..." — too soft; replace with a specific probe
- "Tell me about..." — invites monologue; replace with a focused question
- "Briefly describe..." — hedge phrasing for VP-to-VP; cut the hedge
- Yes/no questions — limits answer depth; rephrase as open-ended
- Glued unrelated questions — split into two bullets
- Bare jargon (CMM, AIB, SOA, 2-speed IT, BAM) — translate inline or pair with an example
- Bare "industry standards" — name which kind (TM Forum, REST/OAuth, TOGAF)
- Empty hedges in questions ("Could you maybe...", "If you don't mind...") — drop entirely

---

## Reference example

The Ken Landry interview guide (VP Architecture, Comcast Cable IT, June 2026) is the gold-standard output produced by this skill. When present, see `work/sessions/2026-06-01-ken-landry-interview/ken-landry-interview-guide.md`.

Key features of that guide to anchor on:

- 8 topic-flavored buckets: General, Tech stack, Consolidation and target state, Architecture core, Reusability, Governance, Operating model, Strategic outlook
- 23 questions across the 8 buckets (3 + 4 + 4 + 3 + 3 + 4 + 3 + 3)
- Each question maps to ≥1 source item (survey + benchmark + wiki)
- Pricing was split out of the vendor-anchor question into its own bullet because it does enough work to stand alone (TTM diagnostic + consolidation prerequisite + channel consistency)
- Strategic close (Q-25, Q-26, Q-27) pulled directly from wiki: TTM through architecture lens, clean-sheet vs. agentic vs. cap-and-grow debate, build-vs-buy stance
- Drop priority cuts technology-lifecycle / function-structure detail before cutting any architecture-core or strategic-close question
- Appendix B explicitly routes 4 items to other stakeholders by domain (order management → Kevin / BJ; workflow tooling → John; BAM → John / BJ; requirements management → Amir / John)

### Sample bucket from the Ken guide (illustrating the template)

```markdown
## 4. Architecture core: blueprint, modularity, rationalization, time-to-market

The architectural substance. Q-11 covers the existence and adherence to a target-state blueprint. Q-12 covers modularity, APIs, integration plumbing, and reuse. Q-13 covers everything that should retire but hasn't. Q-14 frames all of that against the speed at which architecture lets the business actually move.

**Questions**

- **Q-11.** Is there a published reference architecture and target-state blueprint, and how rigorously do new builds adhere to it?
- **Q-12.** How modular is the architecture today: are microservices and APIs the default for new builds, and what does the middleware / integration layer look like?
- **Q-13.** What share of the portfolio is redundant, end-of-life, or out of vendor mainstream support? Is there a continuous retire-and-refresh cadence, or only periodic clean-ups?
- **Q-14.** For a large business innovation (POC to industrialization), how long does it really take, and what is the architecture-side bottleneck (governance gates, integration plumbing, stack rigidity, vendor dependency)?

**Coverage**

| Source | Item | Topic |
|---|---|---|
| Survey | Q21 | Time to implement large business innovations (co-owned w/ Kevin Rhatigan) |
| Benchmark | — | Reference architecture established |
| Benchmark | — | Modular (microservices, APIs) architecture |
| Benchmark | — | Architecture rationalization program established |
| ... | ... | ... |
```

That bucket is the shape every bucket in the output should take: short section intent → 3-5 open-ended questions → notes line → coverage table.
