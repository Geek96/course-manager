# Time-Sensitive Extraction

This is the rule set behind `wiki/综合/考试与截止日期.md` and the
`{Root}/{Semester}/_exports/planvault-time-sensitive.md` hand-off file (see
`sync-rules.md` for when this runs and `SKILL.md` for the hand-off
contract). "Time-sensitive" is broader than "has a Canvas `due_at`" — it
also covers a date a teacher only ever mentioned in prose (an announcement,
a page, a discussion post) with no structured field behind it.

## Two sources, two confidence tiers

### Structured (`confidence: structured`)

Comes straight from canvas-manager's own evidence: an assignment's
`due_at`/`lock_at` recorded in `raw/_manifest/canvas-objects.json`, or an
explicitly-dated exam recorded in a course's syllabus (`wiki/info/`). No
interpretation involved — the source says the date, you copy the date.
`raw_excerpt` stays empty for these; there's nothing to quote, the field
*is* the fact.

### Extracted from prose (`confidence: extracted-high` / `extracted-low`)

A date mentioned in the body text of a `wiki/course_content/` or
`wiki/info/` note (which traces back to an announcement, page, or
discussion via its `source_snapshot`), with no structured field carrying
it. Read the note's actual content (never just its title) looking for a
real, resolvable point in time — "next Tuesday's lecture is moved to the
CULC," "quiz next Wednesday," "office hours this Friday are cancelled."
Resolve relative language (`next Tuesday`, `this Friday`, `in two weeks`)
against the underlying object's own posted/updated timestamp as the
anchor — never against today's sync date, since you're reading something
that may have been posted weeks ago.

- **`extracted-high`**: the date resolves unambiguously once you have the
  anchor — an explicit calendar date ("October 12th"), or a weekday
  reference with no ambiguity about which week ("this Friday" posted on a
  Monday).
- **`extracted-low`**: real time-sensitive content, but the resolution
  required a judgment call — an ambiguous weekday reference, a date implied
  by context rather than stated, or wording you're not fully certain refers
  to a future event rather than something already past.

**Do not extract, at any confidence level:**

- Vague futurity with no resolvable date — "later this semester," "coming
  up soon," "at some point." If you can't turn it into a real date, it's
  not a candidate; leave it out entirely rather than staging it with a
  guessed date.
- Past-tense mentions of things already over — "last week's quiz went
  well." That's not time-sensitive going forward.
- Anything you'd have to fabricate detail for beyond the date itself. The
  `raw_excerpt` field exists so a human can verify your reading — if you
  can't quote a sentence that actually supports the date, don't stage it.

Every extracted row's `raw_excerpt` must be an actual quoted sentence (or
close paraphrase kept under ~200 chars) from the source note's content, not
a summary of your own reasoning.

## `event_kind`

`due` · `exam` · `quiz` · `reading` · `project` · `lecture` ·
`office-hours` · `announcement` · `other`

Pick the closest fit. Use `other` rather than stretching a category —
`announcement` is specifically for a one-off logistical time mention
(room change, cancelled session) that isn't really any of the others.

## The staging file

`{Root}/{Semester}/_exports/planvault-time-sensitive.md`, one file per
semester covering every course in it:

```markdown
---
title: "{{Semester}} 时间敏感事项候选"
type: planvault-export
semester: "{{Semester}}"
generated: {{YYYY-MM-DD}}
tags:
  - type/planvault-export
---

# {{Semester}} 时间敏感事项候选 → PlanVault

> [!info] 用途
> 本文件由 CourseManager 每次深度同步重新生成。`status` 列由消费方（如
> PlanVault 的 daily-plan skill）在用户确认/忽略后原地更新；本技能重新
> 生成时按 `id` 匹配保留已有 `status`，不会把已处理条目重置回
> `pending`。本技能自己不读、不解释这一列，只负责不破坏它。

| id | course | title | event_kind | when | confidence | raw_excerpt | source_type | source_url | source_snapshot | estimated_workload | priority_hint | status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| math4317-due-hw3 | MATH-4317-A | HW3 | due | 2026-10-12 | structured | | assignment | https://... | raw/assignments/.../....md | 2h | high | pending |
| math4317-exam-midterm1 | MATH-4317-A | Midterm 1 | exam | 2026-10-12 | structured | | page | https://... | raw/pages/.../....md | | high | pending |
| math4317-quiz-1015 | MATH-4317-A | 课上小测 | quiz | 2026-10-15 | extracted-high | "下周三课上会有一次小测，覆盖 §4-7" | announcement | https://... | raw/announcements/.../....md | | medium | pending |
```

Column notes:

- **`id`**: stable across regenerations so `status` survives. Build it from
  `{course-slug}-{event_kind}-{short-slug-of-title-or-canvas-object-id}` —
  deterministic, not a random hash, so re-running the same sync produces
  the same `id` for the same underlying fact.
- **`when`**: `YYYY-MM-DD` or `YYYY-MM-DD HH:mm` if a time is known.
- **`estimated_workload`** / **`priority_hint`**: a rough hour estimate and
  a `high`/`medium`/`low` hint, both optional, never fabricated confidently
  beyond what the source actually supports.
- **`status`**: `pending` on first appearance. Only ever written by the
  consuming planning tool afterward — regeneration must read the existing
  file first and carry each matched-`id` row's `status` forward untouched.
  A row whose `when` changed (teacher moved the date) keeps its `status`
  as-is even though `when` changed — that's a signal for the consumer to
  reconcile, not a reason to re-stage it as new. Implemented as tested code
  in `scripts/merge_time_sensitive.py`, not left to agent discipline alone
  — see that script and `tests/test_merge_time_sensitive.py`.

## Relationship to `wiki/综合/考试与截止日期.md`

That note's scope is the same broadened one — not just formal due/exam
dates anymore, but real extracted time mentions too. Add a `类型` column
value for these the same way: `考试`/`due`/`里程碑` plus `公告提及` for
anything sourced from prose rather than a structured field, and carry the
same confidence distinction in a `置信度` column so a reader can tell "the
syllabus says this" from "I inferred this from an announcement, page
checked." This note is read by the student directly in Obsidian — it holds
everything, confirmed or not; the staging file is only the subset destined
for PlanVault and gets pruned via `status` there.
