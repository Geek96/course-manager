# canvas-manager Integration

CourseManager is a read-only consumer of
[canvas-manager](https://github.com/Geek96/canvas-manager)'s output. It
never writes into the raw store, `wiki/course_content/`, or `wiki/info/` —
those belong entirely to canvas-manager. See `obsidian-rules.md` for what
CourseManager does own.

## Required layout (v0.4.0)

CourseManager assumes a course already synced by canvas-manager (either
variant — full or Lite, it makes no difference here). v0.4.0 moved the
evidence store outside the vault:

```text
{Semester}.data/{Course}/
└── raw/
    └── _manifest/canvas-objects.json   # evidence (was {Course}/raw/)

{Course}/
├── readings/                            # human-readable copies of teacher uploads
├── submissions/{assignment-slug}/       # the student's own work (read-only here)
├── wiki/
│   ├── course_content/
│   └── info/
└── 课程总览.md
```

`latest_snapshot` values in the manifest are relative to
`{Semester}.data/{Course}/` (e.g. `raw/assignments/123/....md`).

If `{Semester}.data/{Course}/raw/_manifest/canvas-objects.json` doesn't
exist for a course, that course hasn't been synced by canvas-manager yet —
tell the user to run canvas-manager first rather than trying to work
around the missing evidence.

## Structured due/exam extraction

Read `{Semester}.data/{Course}/raw/_manifest/canvas-objects.json` directly
for each course. Every manifest entry with `canvas_type: assignment` (or a
quiz's `due_at`/`lock_at`, when present) is a `confidence: structured`
candidate — see `time-sensitive.md`. Do not depend on Canvas-specific
fields beyond what the manifest already normalized; canvas-manager's own
`canvas-object-model.md` schema (`canvas_type`, `canvas_id`, `course_id`,
`title`, `updated_at_canvas`, `source_url`, `content`) is the full contract
— nothing Canvas-API-specific leaks through it.

An explicitly-dated exam is usually recorded in the course's syllabus
rather than as its own manifest entry — read the relevant `wiki/info/`
note (e.g. a syllabus summary) for those, not raw snapshots.

## Prose extraction

Read `wiki/course_content/` and `wiki/info/` note bodies — the *digested*
notes, not raw Canvas snapshots — for real time mentions with no structured
field behind them, per `time-sensitive.md`'s extraction discipline. Each
note's frontmatter `source_snapshot` field traces back to the raw evidence
(relative to `{Semester}.data/{Course}/`) if you need to verify a reading
against the original.

## Submission status

`{Course}/submissions/` is the student's own work product, one folder per
assignment (`{assignment-slug}/` holding drafts and the submitted
artifact). A folder existing means submitted; no folder means not
submitted. Read-only — never write here. Surfaces as the `提交状态` column
in `wiki/综合/作业总览.md`.

## Latest-only vs. full-history evidence

canvas-manager Lite keeps only the latest version of each object (no
timestamped history); full canvas-manager keeps a full history. This
doesn't change anything about how CourseManager reads — always read
whatever's currently in `wiki/course_content/`/`wiki/info/` and the current
manifest state, never assume a history exists to look back through.

## What never to do

- Never write into the raw store, `wiki/course_content/`, `wiki/info/`,
  `readings/`, `submissions/`, `课程总览.md`, or `学期总览.md`.
- Never invent a due date, exam date, or course structure not actually
  present in canvas-manager's evidence.
- Never re-fetch Canvas yourself — if evidence looks stale, tell the user
  to re-run canvas-manager's sync first.
