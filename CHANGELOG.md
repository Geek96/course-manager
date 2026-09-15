# Changelog

## 0.2.0

Added optional Agent-original practice-content generation, ported from
[`textbook-cracking`](https://github.com/Geek96/textbook-cracking) v0.1.0
(removed there in its own v0.2.0) — it's inherently course-scoped (reads a
specific course's syllabus or a professor's slide deck to ground range and
difficulty), not textbook deconstruction, so it belongs here instead:

- `练习题/` (math, per-chapter) — one problem set per chapter, scope-
  grounded against the course's actual syllabus range, full bilingual
  pairs, never the textbook's own exercises.
- `选择题练习/`+`选择题答案/`+`编程练习/` (CS, per-week, requires a
  `周次/` Week page to already exist) — MCQs with a separated answer key
  (some modeled on a professor's slide-deck self-check questions, never
  reworded from them) plus a short curated list of link-only external
  coding problems.

New: `references/practice-content.md`, 4 new templates, a new
`obsidian-rules.md` section, and a "Practice content generation" section
in `SKILL.md`. `references/textbook-cracking-integration.md` extended to
also read textbook-cracking's `周次/` (Week pages).

Nothing here is part of a regular run — only build practice content when
the user explicitly asks.

## 0.1.0

Initial release: deadline-aware synthesis (`作业总览.md`, `公告时间线.md`,
`考试与截止日期.md`, `课程复习计划.md` per course; `学期关注.md` per
semester), the confidence-tiered time-sensitive extraction system, and a
merge-safe PlanVault staging file
(`scripts/merge_time_sensitive.py`, 9 unit tests).
