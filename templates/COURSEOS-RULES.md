---
rules-version: 6
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
   这门课“追踪”为是才处理。核心组件 course-manager、canvas-manager 始终可用。
   插件（教材拆解、每周练习题、LectoAI 课堂实录）：停用的不要运行；写了自定义实现的，
   用那个 skill，不用默认的；按课开关为“开”的课才做（如每周练习题“开”的课，整理时
   为新的一周出练习题）。
2. 读 .courseos/journal.md 最近几段，了解之前的会话做了什么、留下了什么。
3. 找到负责这件事的 skill，严格按它的 SKILL.md 执行：
   同步 Canvas → canvas-manager；汇总作业、时间线、待办 → course-manager；
   拆教材 → 教材拆解插件（默认 textbook-cracking）。位置见下方“已安装的 skill”。

## LectoAI 课堂实录（插件启用、这门课开着时）
- 转录稿由 LectoAI 导出到 `{课程目录}/readings/课堂实录/`，是课程原文件：只读，不改不动。
- 把还没整理的转录稿写成 `wiki/课堂实录/` 下的课堂笔记，属性区 `type: lecture-notes`，
  注明来源转录稿；已整理过的不重复写。

## 同步 Canvas
- 一次只同步一门课，不要并行。canvas-manager-lite 的浏览器会话名用 cm-{课号小写}
  （例如 cm-cs-1331），同步完关闭该会话。

## 外部平台
- STATE.md 的“外部平台同步”列出每门课要同步的平台（Gradescope、Perusall、Ed、Piazza 等）。同步 Canvas 时
  按 canvas-manager-lite 的 references/platform-sync.md 一起同步，只读，不提交、不发帖；没列出的平台不要碰。
- course-manager 把平台上的作业并入待办，与 Canvas 上的同一件事去重；学期全景条目写上相关资料（related）。

## 待办与长期项目
- 待办表的 `status`、`user_priority` 两列是用户的（CourseCenter 写），只能经 merge_time_sensitive.py 按 id 保留，不要改。
- 长期项目：发现疑似的写 .courseos/projects/{id}.json（state: candidate）并在会话里问用户是否追踪；
  追踪中的按 course-manager 的 references/tasks-and-projects.md 拆子任务，并写 wiki/综合/长期项目/ 下的只读计划。
  重写项目文件时保留用户的决定：state（tracked/declined）、子任务完成状态、用户设的日期、用户加的子任务。

## 写入纪律
- 只写该 skill 契约允许写的目录（课堂实录插件开着时包括 wiki/课堂实录/）。另外可以写：
  .courseos/projects/（长期项目）、.courseos/profiles/（课程档案）、
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
### 第 6 版
- 外部平台同步（Gradescope、Perusall、Ed、Piazza 等）：以 STATE.md 为准，只读
- 学期全景条目新增相关资料 related（课件、教材章节、平台页面，附理由）
### 第 5 版
- 待办表新增分类、占成绩比例、提交方式、已提交 / 得分等列；status、user_priority 归用户
- 长期项目：发现后询问、拆子任务、写 .courseos/projects/ 与 wiki/综合/长期项目/
### 第 4 版
- 核心组件始终启用；插件（教材拆解、每周练习题、LectoAI 课堂实录）以 STATE.md 为准，可能有自定义实现
- 新增 LectoAI 课堂实录：读 readings/课堂实录/，写 wiki/课堂实录/（type: lecture-notes）
### 第 3 版
- 允许 course-manager 写 .courseos/progress/（学期全景，供 CourseCenter 进度页使用）
### 第 2 版
- 开关以 .courseos/STATE.md 为准；每次工作后在 .courseos/journal.md 追加日志
- 同步 Canvas 一次一门课，浏览器会话名 cm-{课号小写}
- 允许写 .courseos/profiles/（课程档案）
### 第 1 版
- 首个版本：四个工作面、写入纪律、已安装的 skill
