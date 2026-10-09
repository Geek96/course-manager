---
rules-version: 3
---
# CourseOS 规则（在本学期目录工作的所有 agent 必读）

## 东西放在哪（四个工作面）
- 学期目录（本文件所在 .courseos/ 的上一级）是 Obsidian 笔记面：
  每门课 `{课程目录}/` 下只有 wiki/、readings/、submissions/、textbooks/。
- `../{学期}.data/{课程目录}/raw/`：Canvas 原始数据，只追加，不改写。
- `../{学期}.code/{课程目录}/`：这门课的代码。
- `courseos.json`：课程档案和功能开关，由 CourseCenter 维护。

## 做任何课程任务之前
1. 读 .courseos/STATE.md（由 CourseCenter 根据 courseos.json 生成，开关以它为准）：
   这门课“追踪”为是才处理；停用的组件不要运行；每周练习题为“开”的课，
   course-manager 整理时为新的一周出练习题。
2. 读 .courseos/journal.md 最近几段，了解之前的会话做了什么、留下了什么。
3. 找到负责这件事的 skill，严格按它的 SKILL.md 执行：
   同步 Canvas → canvas-manager；汇总作业、时间线、待办 → course-manager；
   拆教材 → textbook-cracking。位置见下方“已安装的 skill”。

## 同步 Canvas
- 一次只同步一门课，不要并行。canvas-manager-lite 的浏览器会话名用 cm-{课号小写}
  （例如 cm-cs-1331），同步完关闭该会话。

## 写入纪律
- 只写该 skill 契约允许写的目录。另外可以写：.courseos/profiles/（课程档案）、
  .courseos/progress/（学期全景），都由 course-manager 生成；.courseos/journal.md（只追加）。
- 不删除、不移动、不重命名任何已有文件（vault 和 .data 都是）。
- 不改 courseos.json 和 .courseos/STATE.md；不改 _exports 待办表的 status 列（那是用户勾选的）。
- submissions/ 是用户自己的作业，只读。
- 安装软件、改系统设置之前，先征得用户同意。
- 拿不准就问用户，不要猜路径；路径以本文件和 courseos.json 为准。

## 工作日志格式
每做完一件事，在 .courseos/journal.md 末尾追加一段（只追加，不改旧内容）：

```
## 2026-10-09 10:32 · {你的 agent 名} · {做了什么，如“同步并整理”}
- 完成：…
- 失败：…（原因）
- 待办：…
```

## 已安装的 skill（配置时填写）
- course-manager：{路径}
- canvas-manager：{路径}
- textbook-cracking：{路径}

## 版本变化
### 第 3 版
- 允许 course-manager 写 .courseos/progress/（学期全景，供 CourseCenter 进度页使用）
### 第 2 版
- 开关以 .courseos/STATE.md 为准；每次工作后在 .courseos/journal.md 追加日志
- 同步 Canvas 一次一门课，浏览器会话名 cm-{课号小写}
- 允许写 .courseos/profiles/（课程档案）
### 第 1 版
- 首个版本：四个工作面、写入纪律、已安装的 skill
