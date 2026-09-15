# Practice-Content Generation (optional, on request only)

Agent-original practice content, ported from `textbook-cracking` as of its
v0.2.0 — that skill used to generate this directly, but it's inherently
course-scoped (reads a specific course's syllabus or a professor's slide
deck to ground range and difficulty), not textbook deconstruction, so it
belongs here instead. See `textbook-cracking-integration.md` for the
read-only source contract this depends on.

Not part of any regular run — only build practice content when the user
explicitly asks for it, separately from a normal synthesis update.

## What this is, and isn't

- **Is**: original problems/questions composed by the Agent, grounded in
  what `wiki/textbook_breakdown/` actually establishes.
- **Is not**: the textbook's own exercises, or the professor's own
  questions reworded/lightly edited. Never reproduce, closely paraphrase,
  or renumber a problem the textbook or a slide deck poses. If asked to
  "extract the textbook's exercises," decline that specific framing —
  composing new problems on the same material is in scope, republishing
  the source's own problems is not.

## Math: `练习题/` (one set per chapter)

Requires `wiki/textbook_breakdown/章节摘要/` and `证明/` to already cover
the requested chapter (textbook-cracking's job, read-only here).

**Calibration**:
- One step beyond a bare theorem restatement — proving a fact from
  definitions without citing the just-established result, constructing a
  counterexample or boundary case, or combining two results into one
  argument.
- Not needlessly obscure: stay inside what the ingested chapter summaries
  and proof pages actually establish plus ordinary undergraduate
  technique — don't require outside results the wiki hasn't covered.
- One idea per problem, concisely stated. No multi-part exam-style
  scaffolding unless the concept genuinely needs the setup.
- Order problems by the section in which the relevant material was
  introduced, matching the chapter summary's own section order.

**Format** (`templates/练习题-template.md`):
- One file per chapter. No answers, no hints, no worked solutions —
  statements only.
- Every problem gets a full bilingual pair: a complete Chinese statement,
  then a complete `*English: ...*` translation immediately below it — not
  just paired terminology. This is different from any "restate the
  textbook's own formal wording in English" convention — a practice
  problem is entirely Agent-composed end to end, so there's no source
  phrasing to translate faithfully; both language versions are equally
  Agent-authored and must express exactly the same problem (same
  hypotheses, same question, same notation/LaTeX in both).
- Keep the same LaTeX/notation across both language versions of a problem.

## CS: week-scoped (requires an existing `周次/` Week page)

Off by default, and a further opt-in beyond textbook-cracking's own
optional Week pages — only build these when the user explicitly asks for
practice material for one or more weeks, and only after the relevant Week
page(s) already exist in `wiki/textbook_breakdown/周次/` (practice
questions are sourced per-week, not per-chapter).

Two independent sub-types, both Agent-original, neither the professor's
nor a third party's own copyrighted material republished:

- **`选择题练习/`** (`templates/选择题练习-template.md`) — MCQs testing
  that week's syntax and concept material. Some are *modeled on* the
  professor's own slide deck's Review/Practice self-check questions (read
  the actual slide deck under `raw/files/...` per the Week page's own
  `source_files` — don't guess at what they probably asked; if a week's
  slides carry no such self-check questions, that subset is simply zero,
  don't invent a fake "modeled on" provenance) — same knowledge point,
  same rough difficulty, **never the professor's actual question reworded
  or lightly edited**. The rest are fully original, authored from what the
  Week page and its linked concept/case-study pages establish.
- **`选择题答案/`** (`templates/选择题答案-template.md`) — a **separate
  page** from the questions, never inline.
- **`编程练习/`** (`templates/编程练习-template.md`) — a short curated
  list of classic problems matching that week's topics, each a
  **link only** (typically LeetCode or a similar judge) plus a one-line
  reason it's relevant — never the problem statement, constraints,
  examples, or a solution reproduced into the wiki page.

**Volume and workload**: no fixed default — agree the per-week count and
modeled-vs-original split with the user for the specific course, and
record it on the practice page (e.g. "10 道参考幻灯片自带 Review 题的知识点
改写，20 道原创，共 30 道"). Keep `编程练习/` short enough not to compete
with the course's own graded workload for that week — a handful of
problems, not a long list; ask for a per-week ceiling rather than
assuming one.

**Frontmatter and linking**: `选择题练习/`, `选择题答案/`, and `编程练习/`
pages set `week_number` and link back to the corresponding `周次/` page
(`week_page: "[[Week 0N - ...]]"`) — they extend that week's material,
never duplicate its own explanatory content. A `选择题练习/` page never
restates concept/case-study content from linked pages, only the question
stems (and, for MCQ, the answer options) themselves.

## Scope grounding (both variants)

Before writing, determine whether this run has course context:

- **Course context available** (a canvas-manager-synced course directory
  sits alongside the textbook wiki): read the course's own evidence first
  — `raw/_manifest/canvas-objects.json`, or a `wiki/info/` syllabus note,
  or a downloaded syllabus PDF under `raw/files/` — for the actually
  assigned chapter/section (math) or week (CS) range. Scope the problem
  set to that range, not the full textbook-cracking ingestion (a
  whole-book Ingest commonly covers more than any single course assigns —
  verify from the syllabus, don't assume `wiki/textbook_breakdown/MOC.md`'s
  declared range equals the course's). State the source of the range in
  the page's `scope_source` frontmatter field and in the abstract callout.
- **No course context** (a standalone textbook wiki with no
  canvas-manager involved, or the user asks for problems independent of
  any course): scope to the chapter(s)/week(s) requested, and say plainly
  in the abstract callout that this covers the textbook's own range, not
  a specific course's syllabus.

Never silently guess a course's assigned range from a chapter's position
in the book — read the actual syllabus source or say the range is
textbook-wide.
