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
          │  raw/, wiki/course_content/,  │  wiki/textbook_breakdown/
          │  wiki/info/                    │
          └───────────────┬────────────────┘
                           ▼
                  ┌──────────────────┐
                  │   course-manager   │  ← core (this repo)
                  │   wiki/综合/         │
                  └─────────┬──────────┘
                             │  {Semester}/_exports/planvault-time-sensitive.md
                             ▼
                  ┌──────────────────┐
                  │  Planning Sink     │
                  │  (optional)         │
                  │  currently:          │
                  │  PlanVault            │
                  └──────────────────┘
```

## Core: course-manager (this repo)

Reads whatever the Evidence Driver and (optional) Content Driver produce;
writes `wiki/综合/` and the Planning Sink hand-off file. Not a pluggable
role — it's what owns these contracts.

## Evidence Driver — required, interface v1

**Contract**, per course directory:

- `raw/_manifest/canvas-objects.json` — one entry per synced object, per
  `canvas-object-model.md`'s schema (`canvas_type`, `canvas_id`,
  `course_id`, `title`, `updated_at_canvas`, `source_url`, plus
  `latest_snapshot` and `content_hash` on the manifest entry).
- `wiki/course_content/` + `wiki/info/` — one digested note per raw
  object, each with a `source_snapshot` frontmatter field pointing back to
  its evidence.

Full detail: `references/canvas-manager-integration.md`.

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

## Building a replacement

1. Pick the role (Evidence Driver / Content Driver / Planning Sink).
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
