<p align="center">
  <img src="https://img.shields.io/badge/AI_Agent-Skill-7C3AED?style=for-the-badge" alt="AI Agent Skill"/>
  <img src="https://img.shields.io/badge/version-0.3.0-10B981?style=for-the-badge" alt="Version 0.3.0"/>
  <img src="https://img.shields.io/github/license/Geek96/course-manager?style=for-the-badge&color=6B7280" alt="MIT License"/>
</p>

<h1 align="center">🗓️ course-manager</h1>

<p align="center">
  <strong>Deadline-aware synthesis across a course's Canvas evidence and (optionally) its textbook coverage</strong>
  <br/>
  <code>Evidence Driver + Content Driver → wiki/综合/ → Planning Sink</code>
  <br/><br/>
  The core of <strong>CourseOS</strong> — see <a href="FRAMEWORK.md">FRAMEWORK.md</a>
</p>

<p align="center">
  <strong>English</strong> | <a href="README.zh-CN.md">简体中文</a>
</p>

---

## 🧱 CourseOS

This repo is CourseOS's **core** — the piece that owns the interface
contracts and produces the thing a student actually reads. Everything it
depends on is a swappable **component**, not a fixed tool:

| Role | Required? | Current implementation(s) |
|------|-----------|---------------------------|
| Evidence Driver | Yes — nothing works without one | [canvas-manager](https://github.com/Geek96/canvas-manager) / canvas-manager-lite |
| Content Driver | Optional | [textbook-cracking](https://github.com/Geek96/textbook-cracking) |
| Planning Sink | Optional | PlanVault |

Any tool that produces/consumes a role's documented contract is a drop-in
replacement for whatever currently fills it — course-manager depends on
the contract, never on a specific tool by name. See
[FRAMEWORK.md](FRAMEWORK.md) for the full role definitions and how to
build a replacement component.

---

## ✨ Features

- **Every time-sensitive item, not just formal due dates** — structured
  Canvas due/exam fields *and* dates a teacher only ever mentioned in an
  announcement/page's prose, each tagged with a confidence tier
  (`structured` / `extracted-high` / `extracted-low`) so you can tell "the
  syllabus says this" from "inferred from an announcement, worth
  double-checking"
- **Assignment overview, announcement timeline, review plan** — the
  cross-cutting synthesis notes a course actually needs, built from
  [canvas-manager](https://github.com/Geek96/canvas-manager)'s evidence,
  not invented
- **Cross-course urgency rollup** — one semester-level note prioritized by
  real time structure across every tracked course, not by which resource
  was most recently touched
- **Structured PlanVault hand-off, with a real merge guarantee** — a
  staging file a planning tool can read and act on; regenerating it never
  silently resets a row a human already marked `imported`/`dismissed` —
  implemented as tested code
  (`scripts/merge_time_sensitive.py`), not left to agent discipline alone
- **Textbook-aware review plans (optional)** — when
  [textbook-cracking](https://github.com/Geek96/textbook-cracking) has
  processed a course's textbook, review plans link real chapter coverage
  instead of guessing a schedule
- **Agent-original practice content (optional, on request)** — per-chapter
  practice problems (math) and per-week MCQ/coding practice (CS), scope-
  grounded against the course's actual syllabus, never the textbook's or a
  professor's own exercises reworded — ported from textbook-cracking,
  since it's inherently course-scoped work
- **Never writes into its sources** — reads canvas-manager's `raw/` and
  `wiki/course_content/`/`wiki/info/`, and textbook-cracking's
  `wiki/textbook_breakdown/`, but only ever writes `wiki/综合/`
- **Agent-managed-region marker discipline** — only ever touches the
  sections of a wiki file it generated; your own handwritten notes in the
  same file are never touched

---

## 📦 Installation

This is a Claude Code plugin/skill, and a companion to canvas-manager — it
needs at least one course already synced by that skill (or by Lite; either
works). If you haven't installed that yet, get it first:

```bash
npx skills add Geek96/canvas-manager
```

Then install this skill:

```bash
npx skills add Geek96/course-manager
```

or clone directly:

```bash
git clone https://github.com/Geek96/course-manager.git
```

Optional, install either (or both) any time — neither is required for
course-manager's core deadline-aware views:

```bash
npx skills add Geek96/textbook-cracking   # textbook-aware review plans + optional practice content
```

PlanVault (the daily-planning tool this skill's staging file feeds) isn't
part of this repo family — install it per its own instructions if you want
that hand-off actually consumed, not just written to `_exports/`.

### Other Agents

Any agent that can read Markdown skills and run Python 3 can use this
repository: clone it, point the agent at
`skills/course-manager/SKILL.md` as the entry point.

---

## 🔧 Dependencies & Prerequisites

> **Required**: Python 3 (standard library only, nothing to `pip install`),
> and at least one course already synced by
> [canvas-manager](https://github.com/Geek96/canvas-manager) (full or
> Lite — this skill doesn't care which). No Obsidian plugin, no MCP server
> of its own, no Canvas access — it never talks to Canvas directly.

```
☐ canvas-manager already run at least once on the course(s) you want a
   deadline view for
☐ Python 3 (already on macOS/most Linux; nothing else to install)
```

**Optional**: [textbook-cracking](https://github.com/Geek96/textbook-cracking)
run on a course with a real textbook — review plans link real chapter
coverage when it's there, and fall back to an honest "no structure to
build from yet" note when it isn't.

---

## 🧩 Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  canvas-manager           textbook-cracking (optional)       │
│  raw/, wiki/course_content/, wiki/info/    wiki/textbook_breakdown/  │
│           │                          │                        │
│           └──────────┬───────────────┘                        │
│                       ▼                                       │
│                 course-manager                                │
│         wiki/综合/ (per course) + 综合/学期关注.md (semester)    │
│                       │                                       │
│                       ▼                                       │
│    {Semester}/_exports/planvault-time-sensitive.md            │
│         (merge-safe — status column never reset)              │
│                       │                                       │
│                       ▼                                       │
│              PlanVault (daily planning, separate skill)       │
└─────────────────────────────────────────────────────────────┘
```

| Output | Scope | Built from |
|--------|-------|-----------|
| `wiki/综合/作业总览.md` | per course | canvas-manager's assignment evidence |
| `wiki/综合/公告时间线.md` | per course | canvas-manager's announcement evidence |
| `wiki/综合/考试与截止日期.md` | per course | structured due/exam + prose-extracted dates |
| `wiki/综合/课程复习计划.md` | per course | course-stated structure, plus textbook-cracking chapter coverage when available |
| `wiki/综合/练习题/` | per course, per chapter, optional | textbook-cracking's `章节摘要/`+`证明/`, scope-grounded against the course syllabus |
| `wiki/综合/选择题练习/`+`选择题答案/`+`编程练习/` | per course, per week, optional | textbook-cracking's `周次/` |
| `{Semester}/综合/学期关注.md` | semester | every tracked course's `考试与截止日期.md` |
| `_exports/planvault-time-sensitive.md` | semester | same time-sensitive extraction, staged for PlanVault |

---

## 📖 Example Prompts

```text
> Build a deadline view for my Fall 2026 courses
> What's due across everything this week?
> Update my time-sensitive staging file for PlanVault
> Does MATH-4317-A have any dates only mentioned in an announcement, not the syllabus?
> Generate practice problems for chapter 3, scoped to what MATH-4317-A actually assigned
> Build week-3 practice for CS-1331 — MCQs plus a few LeetCode links
```

---

## 📁 Project Structure

```text
course-manager/
├── FRAMEWORK.md                                # CourseOS role/contract definitions
├── skills/course-manager/
│   ├── SKILL.md                              # skill entrypoint
│   ├── references/
│   │   ├── time-sensitive.md                 # extraction discipline, confidence tiers, staging-file schema
│   │   ├── practice-content.md               # optional practice-problem/week-practice rules
│   │   ├── obsidian-rules.md                 # wiki/综合/ layout, marker discipline
│   │   ├── canvas-manager-integration.md     # read-only source contract
│   │   ├── textbook-cracking-integration.md  # optional source contract
│   │   └── obsidian-core.md                  # portable Obsidian authoring baseline
│   ├── templates/
│   │   ├── synthesis-template.md             # shared by all 4 per-course notes
│   │   ├── 学期关注-template.md
│   │   ├── 练习题-template.md                 # optional, math
│   │   ├── 选择题练习-template.md              # optional, CS
│   │   ├── 选择题答案-template.md              # optional, CS
│   │   └── 编程练习-template.md               # optional, CS
│   └── scripts/merge_time_sensitive.py       # status-preserving merge, stdlib only
├── tests/test_merge_time_sensitive.py
├── .claude-plugin/plugin.json
└── README.md
```

---

## Development

```bash
python3 -m unittest discover -s tests -v
```

No external dependencies — Python 3 standard library only.

---

## 📄 License

MIT © [Geek96](https://github.com/Geek96)
