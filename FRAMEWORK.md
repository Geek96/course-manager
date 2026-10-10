# CourseOS — component contracts

For the plain-language version of this (what it is, why it's split up like
this), see the README. This file is the technical reference: exact
contracts, for someone actually building a replacement component.

```text
┌──────────────────┐   ┌──────────────────┐
│  Evidence Driver   │   │  Content Driver    │
│  (required)        │   │  (optional)         │
│  currently:         │   │  currently:         │
│  canvas-manager /    │   │  textbook-cracking   │
│  canvas-manager-lite │   │                      │
└─────────┬──────────┘   └─────────┬──────────┘
          │  .data/{Course}/raw/,    │  wiki/textbook_breakdown/
          │  readings/,               │
          │  wiki/course_content/,    │
          │  wiki/info/               │
          └───────────────┬────────────────┘
                           ▼
                  ┌──────────────────┐
                  │   course-manager   │  ← core (this repo)
                  │   wiki/综合/         │  ← also reads submissions/
                  └─────────┬──────────┘
                             │  {Semester}/_exports/planvault-time-sensitive.md
                             ▼
                  ┌──────────────────┐
                  │  Planning Sink     │  ← native planner (planned)
                  │  (optional)         │     currently: PlanVault
                  └──────────────────┘
```

## Work surfaces — v0.4.0

CourseOS material is classified by *work surface*, not by reader. Four
surfaces, each with its own tool and ownership:

| Surface | Tool | Contents |
|---|---|---|
| Notes | Obsidian | `wiki/`, `readings/`, `submissions/`, `textbooks/` |
| Code | VSCode | `{Semester}.code/{Course}/` — one git repo per course, outside the vault |
| Machine | scripts / agents | `{Semester}.data/{Course}/raw/` — append-only evidence, outside the vault |
| Config | CourseCenter | `courseos.json` — course profiles, feature switches |

Rules:

- The Obsidian vault only ever contains the Notes surface. Machine evidence
  (`raw/`) moved out of the vault in v0.4.0 — Obsidian no longer indexes
  it, and "excluded files" hacks are unnecessary.
- Code lives next to the vault, not in it. The vault only links to it —
  never a second copy. A `{Semester}.code-workspace` file opens every
  course repo at once. `.stignore` keeps build artifacts (`node_modules/`,
  `__pycache__/`, `build/`) out of Syncthing.
- Config (`courseos.json`) holds course profiles (schedule, location,
  instructor, grading, links) and feature switches. GUI and skills share
  the one file; switches never live inside note prose.
- `submissions/` (`{assignment-slug}/` per assignment: drafts + the
  submitted artifact) is user-written work product — neither evidence nor
  notes. course-manager reads it for 已提交/未提交 status; never writes it.

## Core: course-manager (this repo)

Reads whatever the Evidence Driver and (optional) Content Driver produce;
writes `wiki/综合/` and the Planning Sink hand-off file. Also reads
`{Course}/submissions/` to report per-assignment 已提交/未提交 status in
the assignment overview. Not a pluggable role — it's what owns these
contracts.

## Evidence Driver — required, interface v2 (v0.4.0)

**Contract**, per course:

- `{Semester}.data/{Course}/raw/` — append-only evidence, *outside* the
  Obsidian vault (moved out in v0.4.0; was `{Course}/raw/`). Layout inside
  is unchanged: `_manifest/canvas-objects.json` (one entry per synced
  object, per `canvas-object-model.md`'s schema: `canvas_type`,
  `canvas_id`, `course_id`, `title`, `updated_at_canvas`, `source_url`,
  plus `latest_snapshot` and `content_hash` on the manifest entry), plus
  timestamped snapshots per object type. `source_snapshot` frontmatter in
  wiki notes points here.
- `{Course}/readings/` — inside the vault: human-readable copies of
  teacher-uploaded readable files (pdf/docx/pptx) extracted from
  `raw/files/` on each sync, named `{Module}_{Title}.pdf`. Flat — no
  polling-numbered directories. Obsidian renders PDFs natively, so this is
  the read-in-Obsidian layer. Copies, not symlinks (Syncthing/mobile
  safe).
- `wiki/course_content/` + `wiki/info/` — one digested note per raw
  object, each with a `source_snapshot` frontmatter field pointing back to
  its evidence. Unchanged from v1.

Migration (v1→v2): one agent pass per semester — move `raw/`, extract
`readings/`, rewrite `source_snapshot` paths. Nothing in `wiki/` moves.

**Current implementations**: `canvas-manager` (API/MCP) and
`canvas-manager-lite` (opencli browser bridge) — two drivers for the same
LMS already proving the contract holds across different implementations.
A driver for a different LMS producing this same shape works here
unmodified.

## Content Driver — optional, interface v1

**Contract**: for a course directory that already has an Evidence
Driver's output, produce `wiki/textbook_breakdown/` (`MOC.md`,
`章节摘要/`, plus whatever unit folders the content model calls for —
`概念/`, `证明/`, `案例/`, `文献/`, `周次/`). Must detect the Evidence
Driver's presence and nest under `wiki/textbook_breakdown/` rather than
writing flat `wiki/...` paths.

Full detail: `references/textbook-cracking-integration.md`.

**Current implementation**: `textbook-cracking`.

## Planning Sink — optional, interface v1

**Contract**: read `{Root}/{Semester}/_exports/planvault-time-sensitive.md`
and own the `status` column correctly (only the sink writes it; the core
only ever merges by `id` and preserves it). Schema in
`references/time-sensitive.md`.

**Current implementation**: `PlanVault` (separate, not yet public).

**Planned (v0.4.0 roadmap)**: a CourseOS-native planner skill for this
role — deterministic scheduling over the staging file plus course
profiles from `courseos.json`, borrowing PlanVault's ideas but rebuilt
for CourseOS data shapes. CourseCenter's GUI already owns the
"看板 + 勾选" half (writing `status`); the planner owns "排进日程".
Contract TBD.

## Core and plugins

Two components are **core**: course-manager and canvas-manager. They are
always enabled and not replaceable — CourseCenter's sync, to-do, progress,
profile, and file pages all depend on them.

The Evidence Driver role below is filled by canvas-manager and is core in
CourseCenter; its contract still documents the data shape.

Everything else is a **plugin**: optional, can be enabled/disabled per
semester (`courseos.json` → `plugins.{id}.enabled`), and can be replaced by
any skill that reads and writes the same paths. Per-course switches live in
`courses[].features`. CourseCenter writes the effective state — including a
custom implementation's path — into `.courseos/STATE.md`; agents follow it.

| Plugin | id | Default implementation | Per-course key | Reads | Writes |
|---|---|---|---|---|---|
| 教材拆解 | `textbook` | textbook-cracking | — | `textbooks/` | `wiki/textbook_breakdown/` |
| 每周练习题 | `practice` | course-manager (built in) | `practice` | `wiki/textbook_breakdown/`, `wiki/course_content/` | `wiki/综合/` (`type: practice-problems` etc.) |
| LectoAI 课堂实录 | `lectoai` | course-manager (built in) | `lectoai` | `readings/课堂实录/` | `wiki/课堂实录/` (`type: lecture-notes`) |

LectoAI contract: LectoAI (or the user) exports lecture transcripts into
`{Course}/readings/课堂实录/` — course originals, never modified. The
plugin turns each not-yet-processed transcript into one lecture note under
`wiki/课堂实录/` with `type: lecture-notes` and a link back to its source
transcript; re-runs skip transcripts that already have a note.

## File classification

CourseCenter's course "文件" page (and any agent that needs to find course
material) classifies every file on two independent axes. course-manager
and other skills don't have to do anything for this to work — the rules
below are derived from where they already write and the `type:` they
already set.

Precedence: manual override in front matter > front-matter `type:` >
folder location and file name.

| `type:` or location | Topic (第一层) | Origin (第二层) |
|---|---|---|
| course-info, file-index, course-dashboard, semester-dashboard | 课程信息 | Agent 提取整理 |
| synthesis, planvault-export | 考试与作业 | Agent 提取整理 |
| exam-review, practice-problems, mcq-practice, mcq-answers, coding-practice | 考试与作业 | Agent 原创 |
| proof, concept, source-summary, chapter-summary, case-study, document-entry, week, event, person, moc, textbook-breakdown-index, image-gallery, lecture-notes | 笔记与书本知识 | Agent 提取整理 |
| any other file under `wiki/` | 笔记与书本知识 | Agent 提取整理 |
| `readings/` | by file name: hw/homework/exam/quiz/midterm/final/lab/project/solution/assignment → 考试与作业; syllabus/大纲/schedule/calendar → 课程信息; else 笔记与书本知识 | 课程原文件 |
| `textbooks/` | 笔记与书本知识 | 课程原文件 |
| `submissions/`, and any non-standard folder or file in the course directory | by file name (same as `readings/`) | 我的 |
| Code surface | 考试与作业 | 我的 |
| Machine surface (`raw/`) | by folder: `assignments`/`quizzes`/`submissions` → 考试与作业; `syllabus` → 课程信息; else 笔记与书本知识 | 课程原文件 |
| Not shown | `wiki/assets/`, `templates/`, hidden files, build artifacts (`.class`, `.jar`, `.o`, `.pyc`; code `build/`, `out/`, `bin/`, `node_modules/`, `__pycache__/`, `target/`) | — |

Manual override keys (values are Chinese, exactly as above; spaces in the
origin value are optional; unrecognised values are ignored):

```yaml
courseos-topic: 考试与作业        # 课程信息 / 考试与作业 / 笔记与书本知识
courseos-origin: Agent 原创      # 课程原文件 / Agent 提取整理 / Agent 原创 / 我的
```

A skill that generates a new kind of note should either use one of the
`type:` values above or set these two keys. Title shown: front-matter
`title:` > first `# heading` > file name.

## Building a replacement

1. Pick a replaceable role: a plugin from the table above, the Content
   Driver (= the 教材拆解 plugin), or the Planning Sink. Core components
   (course-manager, canvas-manager) are not replaceable in CourseCenter.
2. Read that role's linked reference doc in full, not just the summary above.
3. Produce/consume exactly that shape. Nothing else about the current
   implementation (its name, its internal folders, its own scripts) is
   part of the contract.
4. Drop it into the same course directory. No registration step exists —
   course-manager doesn't know or care what tool wrote the files, only
   whether they match the shape.

## Not yet built

This is a documentation-level contract, not a machine-enforced one — no
manifest file, no compatibility checker. Deliberate for now: get the
contracts stable first, add tooling only if drift between implementations
becomes a real problem.
