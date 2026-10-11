# Task fields, submissions, and long-term projects

Read this on every run that writes the staging file or the progress file.
CourseOS uses these fields to split the to-do list into 要交的 /
通知与可选, compute priorities, mark submitted work done, and track
long-term projects. CourseOS computes priority itself from the
inputs below — never write a priority score.

## Staging file: extra columns

`scripts/merge_time_sensitive.py` writes these columns (after
`priority_hint`); put them in each candidate row object:

| Column | Values | How to fill |
|---|---|---|
| `category` | `task` / `notice` / `optional` | `task`: something the student must submit by a deadline. `notice`: exams, regrade windows, registration deadlines, schedule changes — nothing to submit. `optional`: voluntary events, optional activities (read the prose: "you may join", "optional", "if interested"). Extra credit is a `task`. |
| `points` | number or empty | Canvas 分值 from the assignment snapshot. |
| `grade_weight` | decimal fraction of the course grade, or empty | From the syllabus grading breakdown: category weight × this item's points ÷ the category's total points (equal split if points are unknown). Example: Homework 20 % over 10 equal sets → `0.02`. Empty when the syllabus has no breakdown. |
| `submission` | `canvas` / `external` / `in-person` / `none` / empty | From Canvas 提交方式: `online_upload`, `online_text_entry`, `online_quiz`, `online_url` → `canvas`; `external_tool` (Gradescope, etc.) → `external`; `on_paper` → `in-person`; `none` / no submission → `none`. |
| `submitted` | `true` / `false` / empty | From `raw/grades/` (see below) or a matching folder in `{Course}/submissions/`. Empty when unknown. |
| `score` | e.g. `18/20`, or empty | From `raw/grades/`. |
| `project` | long-term project id, or empty | When this row is one of a tracked project's own Canvas deliverables. |

`status` and `user_priority` belong to the student (CourseOS writes
them). The script keeps both by `id`; never set them in candidate rows.

## Submission status: `raw/grades/`

canvas-manager-lite saves each course's Canvas Grades page to
`{Semester}.data/{Course}/raw/grades/{course_id}/latest.md` — one line per
assignment with its status (已交 / 迟交 / 缺交 / 未交) and score. Match
lines to rows by assignment title / Canvas id. 已交 and 迟交 → `submitted:
true`; 缺交 and 未交 past the due date → `false`.

## External platforms: `raw/{platform}/`

canvas-manager-lite saves platform data the student switched on (see its
`references/platform-sync.md`): `raw/gradescope/`, `raw/perusall/`,
`raw/ed/`, `raw/piazza/`, and others, as text objects.

- **Assignments / readings** (Gradescope, Perusall, other platforms' tables)
  become staging rows: `source_type` = the platform id (`gradescope`…),
  `source_url` = the platform page, `submission: external`, and
  `submitted` / `score` from the platform's status column.
- **Deduplicate against Canvas**: if a Canvas assignment is the same piece
  of work (similar title and the same due date, or a Canvas
  external-tool assignment pointing at that platform), keep **one** row —
  the Canvas row's `id` — and take `submitted` / `score` from the
  platform (it's the source of truth for submissions there). Put the
  platform link in that row's progress-file `related`.
- **Staff posts** (Ed, Piazza) are announcements: extract dates from them
  with the same rules as Canvas announcements (`category: notice` unless
  they create a deliverable).

## Progress file: extra fields and tracks

Each item in `.courseos/progress/{COURSE-ID}.json` also carries
`category`, `points`, `gradeWeight`, `submission`, `submitted`, `score`,
`sourceURL` (the Canvas link), and `project` — same meanings as above —
plus `related`: the course materials this task actually uses.

```json
"related": [
  {"title": "Week 5 slides", "path": "readings/Week5.pdf", "why": "Problems 2–4 use the inheritance examples"},
  {"title": "Textbook ch. 3", "path": "wiki/textbook_breakdown/章节摘要/Ch3.md", "why": "the assigned chapter"},
  {"title": "Perusall reading", "url": "https://app.perusall.com/courses/…", "why": "required annotation", "tier": "important"}
]
```

- `path` is relative to the course folder and must exist; use `url` for
  web resources. Keep it to what the task really needs (≤ 6 entries),
  each with a short `why`.
- CourseOS already links, without your help, the note for the
  task's own Canvas page and the Canvas files the description links to —
  don't repeat those. Add what needs judgement: the lecture/week the task
  builds on, textbook chapters, earlier assignments it extends, a
  platform page where the work is actually done.
- Set `"tier": "important"` on a web link that's required (a reading on a
  news site, a platform page); otherwise CourseOS classifies links
  itself (platforms / references / school admin pages).
This file is CourseOS's whole-term ledger (its 全部任务 page and the
archive read it), so include past items.

**Tracks follow the syllabus grading categories** when the syllabus has a
breakdown: one track per category, `"name"` = the category ("Homework"),
`"weight"` = its share of the grade (`0.2`). Without a breakdown, fall
back to series (HW / Quiz / Exam / Project).

## Long-term projects

### Detect

A candidate is any graded work that meets at least one of:

- opens ≥ 4 weeks before it's due (Canvas 开放 → 截止);
- estimated workload ≥ 10 hours;
- its description mentions stages: proposal, checkpoint, milestone, draft,
  progress report, final report/presentation;
- several assignments share one name (Part 1–4, Check-in / Final);
- the syllabus calls it a semester / term project or term paper.

For each new candidate, write
`{Root}/{Semester}/.courseos/projects/{id}.json` with `"state":
"candidate"` and a one-line `"reason"`, then ask the student in the
session: "发现疑似长期项目「…」（理由），要长期追踪吗？". Write their answer
into `state` (`tracked` / `declined`). If they don't answer, leave it as
`candidate` — CourseOS shows a card with 追踪 / 不追踪. Never re-ask
about a `declined` project.

### Plan (state = tracked)

Split the project into subtasks: use the assignment's own checkpoints
and their dates when it has them (`"dueSetBy": "canvas"`); otherwise
spread stages evenly from `start` to `finalDue`, leaving the last ~15 %
as buffer (`"dueSetBy": "agent"`). Give each an `estimateHours`. Also
write a read-only copy of the plan to
`{Course}/wiki/综合/长期项目/{project title}.md` (`type: synthesis`) and
put its path in `wikiNote`.

### File and ownership

```json
{
  "id": "apph1040-pwg", "course": "APPH-1040-E", "title": "Personal Wellness Goal",
  "state": "tracked", "goal": "…", "start": "2026-09-01", "finalDue": "2026-11-24 14:00",
  "reason": "…", "sources": [{"title": "…", "url": "…", "snapshot": "raw/…/latest.md"}],
  "itemIDs": ["…"], "notes": "…", "wikiNote": "wiki/综合/长期项目/Personal Wellness Goal.md",
  "subtasks": [{"id": "s1", "title": "…", "due": "2026-09-15", "dueSetBy": "agent",
                "estimateHours": 2, "done": false, "addedBy": "agent"}]
}
```

CourseOS edits some fields from the student's actions. On every
rewrite you **must keep**: `state` when it is `tracked` or `declined`;
every subtask's `done`; any subtask `due` whose `dueSetBy` is `user`; any
subtask whose `addedBy` is `user`; and any field you don't recognise.
When `finalDue` changes, re-plan only `dueSetBy: "agent"` subtasks.
