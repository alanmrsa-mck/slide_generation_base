# Wiki Schema

This document governs how the LLM maintains the wiki in `knowledge/content/wiki/`. Read it at the start of every ingest, retrieve, and lint operation.

---

## Directory layout

```
knowledge/content/
├── raw/            ← Source files (immutable): .pptx, .pdf, .docx, .txt
├── wiki/
│   ├── index.md   ← catalog of all wiki pages
│   ├── log.md     ← append-only operation timeline
│   └── *.md       ← topic, entity, and concept pages
└── SCHEMA.md      ← this file
```

---

## Page types

| Type | Naming convention | Purpose |
|------|-------------------|---------|
| Source summary | `source-<slug>.md` | One page per ingested source file; summarises its content |
| Topic | `topic-<slug>.md` | Synthesis of a subject across multiple sources |
| Entity | `entity-<slug>.md` | A named person, organisation, product, or place |
| Concept | `concept-<slug>.md` | A recurring idea, framework, or term |
| Overview | `overview.md` | High-level synthesis of the entire wiki |

Use lowercase kebab-case for all slugs.

---

## Page format

Every wiki page must begin with a YAML frontmatter block:

```yaml
---
title: <human-readable title>
type: source-summary | topic | entity | concept | overview
sources: [<source-slug>, ...]   # source files this page draws from
updated: <YYYY-MM-DD>
---
```

After frontmatter, write the page body in markdown. Use `[[wiki-page-slug]]` double-bracket syntax for internal cross-references.

---

## index.md format

`index.md` is a catalog of every wiki page. The LLM updates it on every ingest.

```markdown
# Wiki Index

| Page | Type | Summary | Sources | Updated |
|------|------|---------|---------|---------|
| [[source-example]] | source-summary | One-line description | example.pptx | 2026-01-01 |
```

---

## log.md format

`log.md` is append-only. Every entry uses this prefix so it is grep-parseable:

```
## [YYYY-MM-DD] <operation> | <title>
```

Operations: `ingest`, `query`, `lint`.

Example entry:

```markdown
## [2026-01-01] ingest | example.pptx
- Wrote source-example.md
- Updated topic-strategy.md (added 2 new findings)
- Updated index.md (1 new entry)
```

---

## Ingest workflow

When ingesting a source file from `raw/` (`.pptx`, `.pdf`, `.docx`, or `.txt`):

1. Read `SCHEMA.md` (this file).
2. Extract all text using the appropriate library for the file format.
3. Write a `source-<slug>.md` summary page covering the key content.
4. Identify entities and concepts mentioned; update or create their pages.
5. Identify relevant topic pages; update them to incorporate the new source.
6. If no `overview.md` exists, create one; otherwise update it.
7. Add the new page(s) to `index.md`.
8. Append an entry to `log.md`.

---

## Retrieve workflow

When retrieving content for slide generation:

1. Read `SCHEMA.md` (this file).
2. Read `wiki/index.md` to identify pages relevant to the requested topic.
3. Read those pages in full.
4. Synthesise the content into context for the `create` skill.
5. Flag any gaps: if no relevant wiki content exists, say so — do not invent content.

---

## Lint workflow

Periodically, health-check the wiki:

- Contradictions between pages (newer source supersedes older claim).
- Orphan pages with no inbound `[[links]]`.
- Concepts or entities mentioned in page bodies but lacking their own page.
- Stale `updated` dates where the frontmatter has not been refreshed after a related ingest.
- Append a `## [YYYY-MM-DD] lint | <summary>` entry to `log.md` with findings.

---

## Guardrails

- The LLM writes and maintains all wiki pages. Humans read them.
- Raw source files in `raw/` are never modified.
- Do not invent facts. All claims must trace back to a source file in `raw/`.
- Every wiki page must have frontmatter with `sources` listing the source files it draws from.
