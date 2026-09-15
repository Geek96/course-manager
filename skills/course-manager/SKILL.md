---
name: course-manager
description: Use when a student wants a deadline-aware view across a course or semester already synced by canvas-manager — an assignment overview, an announcement timeline, every time-sensitive item (structured due/exam dates and dates only ever mentioned in an announcement/page's prose), a review plan, or a hand-off file for a daily-planning tool like PlanVault. Read-only consumer of canvas-manager's (and optionally textbook-cracking's) output — never syncs Canvas itself, never writes into their folders.
---

# CourseManager

## Obsidian authoring contract

Before creating or updating any Obsidian artifact, read
`references/obsidian-core.md`. This package-local Core is the portable
baseline; this Skill's own rules and templates take precedence whenever
they are more specific.

## What this skill is and isn't

CourseManager sits between two evidence-producing skills and a
daily-planning tool:

```text
canvas-manager (raw Canvas evidence)  ─┐
                                        ├─▶ CourseManager (wiki/综合/) ─▶ PlanVault (daily planning)
textbook-cracking (textbook coverage) ─┘         (optional hand-off)
```

It never syncs Canvas, never downloads or reads a textbook PDF, and never
does calendars, reminders, or daily planning itself — those are
canvas-manager's, textbook-cracking's, and PlanVault's jobs respectively.
What it does: read canvas-manager's (and optionally textbook-cracking's)
already-synced output, and build the deadline-aware views neither of those
two skills produces.

## Prerequisites

At least one course directory already synced by canvas-manager (full or
Lite — see `references/canvas-manager-integration.md` for the required
layout). If nothing's been synced yet, tell the user to run canvas-manager
first rather than trying to work around missing evidence.

## Every run

1. Read `references/canvas-manager-integration.md` for how to pull
   structured due/exam data and prose-extracted time mentions from
   canvas-manager's evidence.
2. Read `references/time-sensitive.md` for the extraction discipline
   (confidence tiers, what counts as time-sensitive, the `event_kind`
   taxonomy) — this governs both `考试与截止日期.md` and the PlanVault
   staging file.
3. If the course has `wiki/textbook_breakdown/` (from textbook-cracking),
   read `references/textbook-cracking-integration.md` for what to use it
   for and what's still out of scope.
4. Build/update the four per-course notes and the semester-level rollup
   per `references/obsidian-rules.md`, using `templates/synthesis-template.md`
   and `templates/学期关注-template.md`. Respect the `courseManager:`
   agent-managed-region marker discipline — never overwrite a student's
   own writing in the same file.
5. Regenerate `{Root}/{Semester}/_exports/planvault-time-sensitive.md` via
   `scripts/merge_time_sensitive.py` — it merges newly-found candidates
   into the existing file by `id`, preserving every row's `status` column.
   Never hand-edit that file directly; always go through the script so a
   `status` a planning tool already set can't get silently reset.

## Hand-off to planning tools

This skill does not do calendars, daily planning, or reminders. Each run
regenerates `{Root}/{Semester}/_exports/planvault-time-sensitive.md` — see
`references/time-sensitive.md` for the row schema. A planning tool (e.g.
PlanVault) is expected to read that file and decide what to do with each
candidate; this skill never schedules, reminds, or writes into another
tool's vault on its own — staging only.
