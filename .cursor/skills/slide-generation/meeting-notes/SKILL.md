---
name: meeting-notes
description: Takes raw meeting notes and synthesizes them into McKinsey-style debrief notes — unbolded finding bullets, each with supporting sub-bullets (evidence, examples, data, quotes), plus a dedicated Next steps section. Next steps are grounded only in what was explicitly aligned on. Invoke with /meeting-notes.
disable-model-invocation: true
---

# Meeting Notes

Distill raw meeting notes into a compact debrief: 4–6 finding bullets, each a standalone conclusion, each supported by 2–4 sub-bullets carrying the evidence. Close with a dedicated Next steps section and an open-items footer. Match the format of the approved reference example below (the "Mike Crisafulli" debrief format) exactly.

---

## Step 1 — Ingest the notes

The user will either paste meeting notes directly or reference a file. Accept either.

- If a file path is provided, read it now.
- If notes are pasted in context, proceed with what you have.
- If neither is present, ask: "Please paste your meeting notes or share the file path."

Do not proceed until you have the raw notes in hand.

---

## Step 2 — Extract signal

Before writing anything, work through the notes mentally and identify:

1. **Key decisions made** — things the group resolved, agreed on, or closed.
2. **Key findings or facts surfaced** — data points, insights, or framing that shifted the discussion.
3. **Open questions** — items explicitly deferred or unresolved (do not surface as findings; surface in the open-items footer, or as a next step only if someone was assigned ownership).
4. **Explicit next steps** — actions with an owner or a stated timeline that the group aligned on. Only these qualify as next steps. Do not infer or invent.
5. **Themes or patterns** — recurring points, underlying tensions, or structural observations that add interpretive value.

Rank by importance to the audience. Lead with the most consequential finding.

---

## Step 3 — Draft the debrief

Write 4–6 top-level finding bullets, each with supporting sub-bullets. Hard rules:

### Structure (the Mike Crisafulli format)
- **Header line:** `# Name, Title (<date> meeting notes)` — plain, comma-separated, no em-dash, no finding baked into the header.
- **Top-level bullets are findings.** Each is a complete, standalone conclusion a reader understands on its own. State the conclusion, not the topic. No bold.
- **Sub-bullets carry the evidence.** Indent 2 spaces under each finding. 2–4 per finding. They hold the specifics: data points, examples (introduced with "e.g.," or the proper noun directly), mechanisms, and short direct quotes. Sub-bullets are NOT new findings and are NOT next steps.
- **Next steps live in their own section**, not as sub-bullets. Add a plain `Next steps` header near the bottom, then plain bullets — actions and owners only, no findings, no sub-bullets. Include the section only if the meeting produced explicit alignment on an action (owner, timeline, or both). Never infer.
- **Open-items footer** closes the file (see Step 4).

### Content rules
- **Ground everything in the notes.** Do not add interpretation, context, or nuance the notes don't support.
- **Top-down:** the most consequential finding comes first. Order by impact, not chronology.
- **Each finding is a conclusion.** A reader who sees only that line understands the substance. Topic labels are not findings.
- **Quotes:** use the interviewee's actual words when vivid or specific, trimmed to the sharpest phrase. Do not paraphrase a strong quote into a weaker one. Put quotes inline in the relevant sub-bullet (or fold a signature quote into the finding line when it is the point).

### Style rules (non-negotiable)
- **No bold anywhere.** Not on findings, not on sub-bullets, not on owners.
- **No periods at the end of any bullet** — findings, sub-bullets, or next steps. No exceptions.
- **Parallel construction** within each level. Findings share a grammatical form; sub-bullets under a finding share a form.
- **Pithy:** cut every filler word. Findings run ≤25 words; sub-bullets stay tight; next steps ≤15 words.
- **Sentence case:** first word and proper nouns only. No Title Case.
- **No em dashes** (—). Use a comma or two short clauses.
- **No semicolons.** Split into two clauses or two sub-bullets.
- **No arrows** (→, ->, =>). Rewrite as a phrase ("which drives", "leading to").
- **No weasel words** ("may", "could potentially", "it seems"). State what happened.
- **No meta-language** ("it was noted that", "the team discussed", "in this meeting"). State the substance directly.
- **Active voice by default.**

### Next steps style
- Lead with an action verb, or with the owner when named: "Antonio to send…", "Nikita to schedule…"
- Include the timeline if stated.
- No bold, no trailing period, no sub-bullets.

---

## Step 4 — Output

Save the debrief to a session folder per the session-markdown-outputs rule (`work/sessions/<YYYY-MM-DD-topic-slug>/<name>-meeting-notes.md`) and also show it in chat. Start the file directly with the header line — no preamble, no "Here are your takeaways:" opener.

Use this exact shape:

```
# [Name, Title] ([date] meeting notes)

- [Finding 1, a standalone conclusion]
  - [Supporting evidence / example / data / quote]
  - [Supporting evidence / example / data / quote]

- [Finding 2, a standalone conclusion]
  - [Supporting evidence / example / data / quote]
  - [Supporting evidence / example / data / quote]

- [Finding 3 …]
  - [Supporting evidence …]

Next steps
- [Owner] to [action] [by timeline if stated]
- [Owner] to [action]

---
*[N] open items not captured above, with no owner or timeline aligned in the meeting, [brief comma-separated list]*
```

Omit the `Next steps` section if nothing was explicitly aligned on. Omit the open-items footer only if everything was closed or next-stepped.

---

## Reference example (approved output style — match this)

This is the gold-standard format and register. Anchor all future outputs against it: unbolded finding bullets, supporting sub-bullets, a Next steps section, an open-items footer, no trailing periods.

```
# Mike Crisafulli, Head of Residential IT (6-5 meeting notes)

- NewCo greenfield is the centerpiece of the architecture story, a clean BSS stack that firewalls off the legacy
  - Born after Steve rejected the in-place plan (turn off ACSR and Amdocs CRM, unify the frontline tool, rationalize catalog and order orchestration on CSG and Amdocs) as a 3-4 year journey he had no time for
  - Adds two things Comcast lacks today, a CX control plane for journey management and decisioning, and an AI-first digital BSS layer where most friction surfaces
  - Prototype covers BSS layers 2 through 4 where friction sits, leaves network OSS out of scope, reuses the existing AID layer
  - Vendors are building working software demos, not slideware, against a 28-page prototype spec, with demos due back in about 8 weeks and a vendor-selection check-in on July 15

- Complexity is business rules, not the tech stack, which Mike states flatly as "it's not a tech problem"
  - Launching even a simple standard promotional offer (Archer) took 5 days to push through the system, because promotion, discount, and eligibility logic is duplicated across nearly every system
  - ACSR, the legacy green-screen CRM behind roughly 70% of assisted sales, lets agents freely edit any of 17,000 service codes with no guardrails, which drives fallout and rework
  - A clean modular design would localize that logic so one offer change touches one or two systems instead of all of them

- Mike is buying the core stack, not building it
  - Pushed back on the "SaaS is dead, build it agentic" message from the 52nd and 53rd floors, and both Anthropic and OpenAI advised against building core BSS from scratch
  - Sees over-customization, not the underlying technology, as the root cause, "the mainframe never stopped us, the customization did"

Next steps
- Build the end-July multi-year transformation narrative with the self-funding cost-out story
- Size the "clean" customer population with EBI and finance without ARPU impact

---
*3 open items not captured above, with no owner or timeline aligned in the meeting, the migration mechanism, the startup-team resource plan, and final vendor selection*
```

**What makes this example correct:**
- Header is plain `Name, Title (date meeting notes)`, no bold, no finding in the header
- Top-level bullets are conclusions, not topic labels, with no bold
- Sub-bullets carry the supporting specifics, examples, data, and quotes — not new findings, not next steps
- Next steps sit in their own section, actions only
- No trailing periods anywhere; no em dashes, arrows, or weasel words
- Open-items footer captures what was left unresolved

---

## Guardrails

- **Match the reference format.** Unbolded findings + supporting sub-bullets + Next steps section + open-items footer. Do not revert to bolded one-line takeaways.
- **Never invent next steps.** If the notes don't name an owner or action, it is background or an open item, not a next step.
- **4 findings minimum, 6 maximum.** If the notes are thin, write 4 tight ones with fewer sub-bullets rather than padding.
- **Sub-bullets are evidence, not findings.** If a sub-bullet reads like its own headline, promote it to a finding or fold it in.
- **Do not editorialize.** Synthesis, not commentary.
- **Do not mention the meeting itself.** State the substance directly.
- **If the notes are unclear or contradictory**, write what is clearly supported and flag ambiguity in the open-items footer rather than guessing.
