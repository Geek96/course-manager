---
title: "{{synthesis_title}}"
type: synthesis
course: "{{course_name}}"
created: {{YYYY-MM-DD}}
updated: {{YYYY-MM-DD}}
tags:
  - type/synthesis
  - course-manager/synthesis
  - course/{{course-slug}}
---

# {{synthesis_title}}

<!-- agent-managed:start id="courseManager:synthesis-{{note-slug}}" -->
{{按用途选表格/时间线格式：

作业总览 → | 作业 | 类型 | 状态 | Due | 来源快照 |
公告时间线 → 按时间倒序的列表，每条带日期和一句话摘要
考试与截止日期 → | 事件 | 日期 | 类型（考试/due/里程碑/公告提及）| 置信度（structured/extracted-high/extracted-low）| 备注 |
课程复习计划 → 按周或按主题的复习安排；有 wiki/textbook_breakdown/ 时链接真实章节覆盖，没有就如实说明缺什么结构，不要编

数据来自哪些 course_content/info 笔记就带 [[wikilink]] 链接，保持可溯源。"公告提及"这类从正文解析出的时间点，备注里带一句原文摘录，见
`references/time-sensitive.md`。}}
<!-- agent-managed:end -->

> [!warning] 优先级判断
> 排序/标记紧急程度时按**时间结构**（due date、考试日期、以及从公告/页面正文解析出的时间点），不要按"哪个资源最近被更新"——老师传了新文件不代表这周就该优先处理它。

---

## 我的笔记

(学生手写区域，agent 不会碰这里)
