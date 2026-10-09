---
rules-version: 1
---
# CourseOS 规则（在本学期目录工作的所有 agent 必读）

## 东西放在哪（四个工作面）
- 学期目录（本文件所在 .courseos/ 的上一级）是 Obsidian 笔记面：
  每门课 `{课程目录}/` 下只有 wiki/、readings/、submissions/、textbooks/。
- `../{学期}.data/{课程目录}/raw/`：Canvas 原始数据，只追加，不改写。
- `../{学期}.code/{课程目录}/`：这门课的代码。
- `courseos.json`：课程档案和功能开关，由 CourseCenter 维护。

## 做任何课程任务之前
1. 读 courseos.json：这门课 enabled 才处理；相关功能开关
   （practice / bridge / lecture-scripts）关着的事不要做。
2. 找到负责这件事的 skill，严格按它的 SKILL.md 执行：
   同步 Canvas → canvas-manager；汇总作业、时间线、待办 → course-manager；
   拆教材 → textbook-cracking。位置见下方“已安装的 skill”。

## 写入纪律
- 只写该 skill 契约允许写的目录。
- 不删除、不移动、不重命名任何已有文件（vault 和 .data 都是）。
- 不改 courseos.json；不改 _exports 待办表的 status 列（那是用户勾选的）。
- submissions/ 是用户自己的作业，只读。
- 安装软件、改系统设置之前，先征得用户同意。
- 拿不准就问用户，不要猜路径；路径以本文件和 courseos.json 为准。

## 已安装的 skill（配置时填写）
- course-manager：{路径}
- canvas-manager：{路径}
- textbook-cracking：{路径}
