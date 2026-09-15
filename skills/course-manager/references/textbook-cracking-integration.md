# textbook-cracking Integration (optional)

[textbook-cracking](https://github.com/Geek96/textbook-cracking) is
optional — a course with no textbook, or no textbook processed yet, simply
has no `wiki/textbook_breakdown/` folder. CourseManager must work fine
without it; only use what's actually there.

## What's available when it exists

```text
{Course}/
└── wiki/
    └── textbook_breakdown/
        ├── MOC.md
        ├── 章节摘要/
        ├── 概念/
        └── <model-specific folders — 证明/, 案例/, 文献/>
```

Read-only, same as canvas-manager's folders — CourseManager never writes
here.

## What v1 actually does with it

`课程复习计划.md` (see `obsidian-rules.md`) links to real chapter coverage
from `wiki/textbook_breakdown/章节摘要/` and `wiki/textbook_breakdown/MOC.md`
when building a review plan, instead of inventing a schedule — the same
"never fabricate structure" discipline as everything else this skill does.

## Not yet built (roadmap, not v1)

textbook-cracking's own `course-manager-integration.md` describes a fuller
integration: detecting a Canvas assignment's exercise reference (e.g.
"§5.2 Exercises 2aceg") and connecting it to the matching
textbook-cracking chapter/section range, publishing the result under
`wiki/综合/`. **This isn't implemented in v1.** Report the gap if a user
asks for it rather than improvising a partial version — this needs real
design (how exercise ranges get detected and matched reliably) before it's
a real feature, the same way textbook-cracking itself treats its
not-yet-built "narrative reading" content model as a deliberate future
step rather than something to stretch an existing model to cover.
