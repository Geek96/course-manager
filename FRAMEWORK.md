# CourseOS — a component framework for Canvas-synced Obsidian study vaults

`course-manager` is CourseOS's **core** — the piece that defines these
contracts, depends on the others existing, and is what actually produces
the thing a student reads (`wiki/综合/`, the PlanVault hand-off). Everything
around it is a **component**: a role with a fixed input/output contract,
not a fixed tool. Any implementation that honors a role's contract is a
drop-in replacement for whatever currently fills that role — course-manager
never depends on canvas-manager or textbook-cracking *by name*, only on
what they're contractually required to produce.

This file is the index. Each contract's exact technical shape (schemas,
field names, folder layout) lives in this repo's own reference docs —
`references/canvas-manager-integration.md` and
`references/textbook-cracking-integration.md` — this file names the roles
and states the contract at the level a replacement's author needs to
scope the work, then points there for the rest.

## Roles

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
                  │   course-manager   │  ← the core / kernel
                  │   wiki/综合/         │     (this repo)
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

### Core: the Kernel

**Role**: reads whatever the Evidence Driver and (optionally) Content
Driver produce; writes `wiki/综合/` and the Planning Sink hand-off file.
Owns the interface definitions themselves — a replacement Kernel would
have to reimplement everything in this repo's `references/`, not just
match a folder shape.

**Current implementation**: `course-manager` (this repo).

### Provider role: Evidence Driver (required — nothing works without one)

**Contract**: for a given course directory, produce

- `raw/_manifest/canvas-objects.json` — one entry per synced object,
  matching `canvas-object-model.md`'s schema (`canvas_type`, `canvas_id`,
  `course_id`, `title`, `updated_at_canvas`, `source_url`, plus a
  `latest_snapshot` path and `content_hash` in the manifest entry itself).
- `wiki/course_content/` and `wiki/info/` — one digested Markdown note per
  raw object, classified per the "does this note teach you something, or
  tell you how the course operates" test, each carrying a
  `source_snapshot` frontmatter field pointing back to its raw evidence.

Full detail: `references/canvas-manager-integration.md`.

**Current implementations**: `canvas-manager` (Canvas API/MCP) and
`canvas-manager-lite` (opencli browser bridge) — two interchangeable
Evidence Drivers for the same LMS, already proving the contract works
across differently-sourced implementations. A driver for a different LMS
(Moodle, Blackboard, ...) that produced this same manifest+wiki shape
would work here unmodified.

**Interface version**: v1 (unversioned so far — call it v1 from here on;
bump this doc's stated version and note the change here if the manifest
schema or classification rule ever changes incompatibly).

### Provider role: Content Driver (optional)

**Contract**: for a course directory that already has an Evidence Driver's
output, produce `wiki/textbook_breakdown/` — `MOC.md`, `章节摘要/`, plus
whatever unit-type folder(s) the source material's content model calls
for (`概念/`, `证明/`, `案例/`, `文献/`, `周次/`, ...). Must detect the
Evidence Driver's presence (`wiki/course_content/`/`wiki/info/` already
exist) and nest under `wiki/textbook_breakdown/` accordingly rather than
writing flat `wiki/...` paths — see the "Wiki root" contract in
`references/textbook-cracking-integration.md`.

Full detail: `references/textbook-cracking-integration.md`.

**Current implementation**: `textbook-cracking`.

**Interface version**: v1.

### Consumer role: Planning Sink (optional)

**Contract**: read `{Root}/{Semester}/_exports/planvault-time-sensitive.md`
— the row schema and the `status`-column ownership rule (only the sink
writes `status`; the Kernel only ever merges by `id` and preserves it) are
defined in `references/time-sensitive.md`. Anything that reads this file
and owns `status` correctly is a valid sink.

**Current implementation**: `PlanVault` (a separate, not-yet-public
daily-planning tool/skill).

**Interface version**: v1.

## Building a replacement component

1. Pick the role you're filling (Evidence Driver, Content Driver, or
   Planning Sink — the Kernel itself isn't a pluggable role, it's this
   repo).
2. Read that role's contract doc in full — not just this summary.
3. Produce/consume exactly that shape. Nothing else about the existing
   implementation (its name, its own internal folder structure under
   `raw/sync/`, its own scripts) is part of the contract — only what's
   documented in the linked reference file.
4. No registration step exists yet (see "What this isn't" below) — a
   replacement just needs to sit in the same course directory and produce
   the right shape; course-manager doesn't know or care what tool wrote
   it.

## What this isn't (yet)

This is a documentation-level contract, not a machine-enforced one — there
is no manifest file a component declares itself with, and no compatibility
checker. That's a deliberate v1 scope choice: get the contracts written
down and stable first, add tooling later only if drift between
implementations actually becomes a real problem. If a future version adds
a machine-checkable manifest, it'll be noted here and the "Interface
version" fields above will start mattering operationally, not just as
documentation.
