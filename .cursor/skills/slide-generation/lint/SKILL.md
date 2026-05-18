---
name: lint
description: Health-check and maintain the wiki in knowledge/content/wiki/. Finds contradictions, orphan pages, missing entity/concept pages, stale frontmatter, and index gaps. Appends findings to log.md. Use when the wiki needs a quality pass or after several ingests.
disable-model-invocation: true
---

# Lint

Audit the wiki at `knowledge/content/wiki/` for consistency and completeness, then record findings in `log.md`.

## Before starting

Read `knowledge/content/SCHEMA.md` — all page types, naming conventions, frontmatter format, and cross-reference syntax are defined there.

## Steps

### 1 — Inventory all wiki pages

List every `.md` file in `knowledge/content/wiki/` except `index.md` and `log.md`. For each page, read its frontmatter (`title`, `type`, `sources`, `updated`) and collect all outbound `[[slug]]` links in the body.

### 2 — Check: index.md completeness

Read `knowledge/content/wiki/index.md`. Every page from Step 1 must have a corresponding row in the index table.

- For each page missing from the index: flag it as **missing from index**.

### 3 — Check: orphan pages

A page is an orphan if no other wiki page contains a `[[slug]]` link pointing to it (source-summary pages are exempt — they are referenced from index.md by design).

- For each orphan topic, entity, or concept page: flag it as **orphan**.

### 4 — Check: missing entity/concept pages

Scan every page body for `[[slug]]` cross-references. If a referenced slug has no corresponding `.md` file in `wiki/`, it is a broken link.

- For each broken `[[slug]]`: flag it as **missing page**.

Also scan page bodies for named entities (people, organisations, products, places) and concepts (frameworks, terms, ideas) that appear as plain text but have no `entity-<slug>.md` or `concept-<slug>.md`. Flag notable ones as **suggested page**.

### 5 — Check: stale frontmatter

For each page, compare the `updated` date in its frontmatter against the dates in `log.md` for any ingest that lists the page as touched. If a more recent ingest touched a page but its `updated` date was not refreshed, flag it as **stale**.

### 6 — Check: contradictions

For topic and entity pages that draw from multiple sources, look for conflicting claims — e.g. a figure, date, or conclusion that differs between sources cited in the same page. Flag each as **contradiction**, noting the conflicting statements and their sources.

### 7 — Report findings to user

Print a summary grouped by check:

```
Wiki Lint Report — <YYYY-MM-DD>

Missing from index  : <n> pages
Orphan pages        : <n> pages
Missing/broken pages: <n> links
Suggested new pages : <n> items
Stale frontmatter   : <n> pages
Contradictions      : <n> items

Details:
[Missing from index]
  - <slug> (type: <type>)

[Orphan pages]
  - <slug>

[Missing/broken pages]
  - [[<slug>]] referenced in <page>

[Suggested new pages]
  - "<term>" mentioned in <page> — consider creating entity-<slug>.md

[Stale frontmatter]
  - <slug>: updated <date>, but touched by ingest on <date>

[Contradictions]
  - <slug>: "<claim A>" (source: <file>) vs "<claim B>" (source: <file>)
```

If there are zero findings in a category, omit that section.

### 8 — Append to log.md

Append an entry to `knowledge/content/wiki/log.md`:

```markdown
## [YYYY-MM-DD] lint | <N> issues found
- Missing from index: <n>
- Orphans: <n>
- Missing pages: <n>
- Stale frontmatter: <n>
- Contradictions: <n>
```

## Guardrails

- Do not auto-fix issues — report only, unless the user explicitly asks you to fix a specific finding.
- Do not modify source files in `knowledge/content/raw/`.
- Do not invent new wiki content during a lint run.
- If the wiki is empty (no pages beyond `index.md` and `log.md`), report that and exit.
