# Obsidian / Wiki Authoring Rules

This skill only ever writes into `wiki/综合/` inside a course directory, and
`综合/学期关注.md` at the semester level. Everything else in a course or
semester directory (`raw/`, `wiki/course_content/`, `wiki/info/`,
`wiki/textbook_breakdown/`, `课程总览.md`, `学期总览.md`) belongs to
canvas-manager and, optionally, textbook-cracking — read-only, never
written here. See `canvas-manager-integration.md` and
`textbook-cracking-integration.md` for the source contracts.

```text
{Course}/
└── wiki/
    └── 综合/
        ├── 作业总览.md
        ├── 公告时间线.md
        ├── 考试与截止日期.md
        ├── 课程复习计划.md
        ├── 练习题/            # optional, on request only — see practice-content.md
        ├── 选择题练习/         # optional, on request only, CS + week-scoped
        ├── 选择题答案/         # optional, on request only, CS + week-scoped
        └── 编程练习/           # optional, on request only, CS + week-scoped

{Semester}/
└── 综合/
    └── 学期关注.md
```

## The four per-course notes

- `作业总览.md` — every assignment, due date, status. Source: canvas-manager's
  `raw/_manifest/canvas-objects.json` assignment entries plus any
  `wiki/course_content/`/`wiki/info/` note that discusses one.
- `公告时间线.md` — announcements in reverse chronological order, one-line
  summary each, dated.
- `考试与截止日期.md` — every time-sensitive item, not just formal
  due/exam fields — also a real date a teacher only ever mentioned in an
  announcement/page/discussion's prose. A `类型` column
  (`考试`/`due`/`里程碑`/`公告提及`) and a `置信度` column
  (`structured`/`extracted-high`/`extracted-low`) distinguish "the syllabus
  says this" from "inferred from prose, worth double-checking" — see
  `time-sensitive.md` for the extraction discipline.
- `课程复习计划.md` — review plan, only built from real captured structure
  (a syllabus schedule, a chapter list actually stated by the course, or —
  when `wiki/textbook_breakdown/` exists — real chapter coverage from
  textbook-cracking); never invent a week-by-week plan for a course that
  hasn't published one.

Use `templates/synthesis-template.md` for all four — it's already generic
across this shape via its `{{...}}` guidance block, not one template per
note type.

## Practice content (optional, on request only)

`练习题/` (math, per-chapter) and `选择题练习/`+`选择题答案/`+`编程练习/`
(CS, per-week) — Agent-original practice problems and week-scoped
quizzes, never part of a regular run, only built when the user explicitly
asks. See `practice-content.md` for the full rule set (calibration, scope
grounding against a course's actual syllabus, bilingual/MCQ/coding-practice
format) and their own templates
(`templates/练习题-template.md`, `templates/选择题练习-template.md`,
`templates/选择题答案-template.md`, `templates/编程练习-template.md`).
Requires `wiki/textbook_breakdown/` to exist (textbook-cracking) — nothing
to generate without it.

## The semester-level note

`{Semester}/综合/学期关注.md` — cross-course urgency rollup, using
`templates/学期关注-template.md`. Built from every tracked course's
`考试与截止日期.md`, prioritized by **course time structure** (due dates,
exam dates, extracted time mentions), never by "which resource was
recently updated." A teacher uploading a file is not itself a signal of
urgency.

## Ownership boundary (read this before editing any wiki file)

A wiki file can contain both agent-generated content and the student's own
handwritten notes in the same file. This skill must never destroy the
student's own writing.

Rule: every agent-generated section starts with an HTML comment marker and
ends with a matching close marker, using `courseManager:`-prefixed IDs
(mirrors textbook-cracking's own `textbook:` prefix convention, so multiple
skills can safely share a file through distinct regions if that's ever
needed):

```markdown
<!-- agent-managed:start id="courseManager:synthesis-作业总览" -->
... content this skill generated/updated ...
<!-- agent-managed:end -->
```

When updating a wiki file:

1. Read the whole file.
2. Only replace text between a matching `agent-managed:start`/`:end` pair
   with the same `id`.
3. If no marker with that `id` exists yet, append a new marked section —
   never assume the whole file is safe to overwrite.
4. Anything outside marker pairs (the student's own prose) is left
   byte-for-byte untouched.

## Visual conventions

Every wiki file uses the templates in `../templates/`. Two things make them
worth using instead of writing prose from scratch:

- **YAML frontmatter with a `tags` hierarchy** — `type/<template-type>`,
  `course/<course-slug>`. This is what makes the vault filterable/queryable
  in Obsidian, not just a pile of files. Dataview is optional, never
  required — every note here is useful as static Markdown on its own.
- **Obsidian callouts** (`> [!abstract]`, `> [!tip]`, `> [!warning]`,
  `> [!info]`) instead of plain paragraphs for anything that's a summary,
  an action item, a risk, or an open question.
- **Wiki-links (`[[...]]`)** to the course_content/info/textbook_breakdown
  notes a synthesis row is drawn from, instead of plain text mentions — a
  filename like `作业总览.md` repeats across every course, so a
  cross-course link needs the full path
  (`[[CourseName/wiki/综合/作业总览|作业总览]]`) to avoid Obsidian
  resolving it to the wrong course.

## Never invent structure

Never fabricate a due date, exam date, review-plan week, or textbook
coverage claim that isn't actually backed by canvas-manager's evidence or
textbook-cracking's chapter summaries. If a course hasn't published enough
structure for a real review plan, say so honestly in `课程复习计划.md`
rather than guessing one.
