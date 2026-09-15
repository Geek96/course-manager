<p align="center">
  <img src="https://img.shields.io/badge/AI_Agent-Skill-7C3AED?style=for-the-badge" alt="AI Agent Skill"/>
  <img src="https://img.shields.io/badge/version-0.3.0-10B981?style=for-the-badge" alt="Version 0.3.0"/>
  <img src="https://img.shields.io/github/license/Geek96/course-manager?style=for-the-badge&color=6B7280" alt="MIT License"/>
</p>

<h1 align="center">🗓️ course-manager</h1>

<p align="center">
  <strong>基于截止日期的综合汇总——跨课程的 Canvas 证据，以及（可选）教材覆盖情况</strong>
  <br/>
  <code>Evidence Driver + Content Driver → wiki/综合/ → Planning Sink</code>
  <br/><br/>
  <strong>CourseOS</strong> 的核心——见 <a href="FRAMEWORK.md">FRAMEWORK.md</a>
</p>

<p align="center">
  <a href="README.md">English</a> | <strong>简体中文</strong>
</p>

---

## 🧱 CourseOS

这个仓库是 CourseOS 的**核心**——负责定义接口契约、产出学生真正会读的东西的那一部分。它依赖的每一样东西都是可替换的**组件（component）**，而不是绑定死的固定工具：

| 角色 | 是否必需？ | 当前实现 |
|------|-----------|---------------------------|
| Evidence Driver（证据驱动） | 是——没有它什么都跑不起来 | [canvas-manager](https://github.com/Geek96/canvas-manager) / canvas-manager-lite |
| Content Driver（内容驱动） | 可选 | [textbook-cracking](https://github.com/Geek96/textbook-cracking) |
| Planning Sink（规划落点） | 可选 | PlanVault |

任何能产出/消费某个角色所定义契约的工具，都可以直接替换掉当前占据该角色的实现——course-manager 依赖的是**契约**，从不依赖某个具体工具的名字。完整的角色定义和如何自己搭一个替代组件，见 [FRAMEWORK.md](FRAMEWORK.md)。

---

## ✨ 特性

- **不只是正式截止日期，每一条有时间敏感性的信息都不放过** —— 既有结构化的 Canvas 截止/考试字段，也有老师只在某条公告/页面的正文里提过一嘴的日期，每一条都打上置信度标签（`structured` / `extracted-high` / `extracted-low`），让你能分清"教学大纲写明的"和"从公告里推断出来的、值得再核实一下"
- **作业总览、公告时间线、复习计划** —— 一门课真正需要的跨切面综合笔记，基于 [canvas-manager](https://github.com/Geek96/canvas-manager) 的证据生成，不是凭空编的
- **跨课程紧急度汇总** —— 一份学期级别的笔记，按所有被追踪课程的真实时间结构排优先级，而不是按"哪个资源最近被改动过"排序
- **结构化的 PlanVault 交接，带真正的合并保证** —— 一个规划工具可以读取并据此行动的暂存文件；重新生成它时，绝不会悄悄重置一行人类已经标记过 `imported`/`dismissed` 的记录——这是用经过测试的代码实现的（`scripts/merge_time_sensitive.py`），不是仅靠 agent 自觉遵守
- **感知教材的复习计划（可选）** —— 当 [textbook-cracking](https://github.com/Geek96/textbook-cracking) 已经处理过某门课的教材时，复习计划会链接真实的章节覆盖情况，而不是瞎猜一个进度表
- **Agent 原创练习内容（可选，按需生成）** —— 按章节的练习题（数学）和按周的选择题/编程练习（CS），范围锚定在课程实际的教学大纲上，绝不是把教材或教授自己的习题换个说法照搬——这部分是从 textbook-cracking 移植过来的，因为它本质上是课程范围内的工作
- **绝不写入它的数据源** —— 读取 canvas-manager 的 `raw/` 和 `wiki/course_content/`/`wiki/info/`，以及 textbook-cracking 的 `wiki/textbook_breakdown/`，但只会写入 `wiki/综合/`
- **Agent 管理区域标记规则** —— 只触碰它自己生成的那部分内容；同一文件里你自己手写的笔记永远不会被碰

---

## 📦 安装

这是一个 Claude Code 插件/skill，是 canvas-manager 的配套工具——需要至少有一门课已经被那个 skill 同步过（完整版或 Lite 都行）。如果还没装，先装那个：

```bash
npx skills add Geek96/canvas-manager
```

然后再装这个 skill：

```bash
npx skills add Geek96/course-manager
```

或者直接克隆：

```bash
git clone https://github.com/Geek96/course-manager.git
```

可选项，随时装、装哪个都行——对 course-manager 核心的截止日期视图来说都不是必需的：

```bash
npx skills add Geek96/textbook-cracking   # 感知教材的复习计划 + 可选的练习内容
```

PlanVault（消费本 skill 暂存文件的每日规划工具）不属于这个仓库家族——如果想让这份交接文件真的被规划工具消费掉，而不是只是静静躺在 `_exports/` 里，按它自己的说明另外安装。

### 其他 Agent

任何能读 Markdown skill、能跑 Python 3 的 agent 都可以使用这个仓库：克隆它，让 agent 指向 `skills/course-manager/SKILL.md` 作为入口。

---

## 🔧 依赖与前置条件

> **必需**：Python 3（仅用标准库，不用 `pip install` 任何东西），以及至少一门已经被 [canvas-manager](https://github.com/Geek96/canvas-manager) 同步过的课程（完整版或 Lite 都可以，本 skill 不关心用的是哪个）。不需要 Obsidian 插件，不需要自己的 MCP server，不直接访问 Canvas——它从不直接和 Canvas 对话。

```
☐ 想要截止日期视图的课程，已经至少跑过一次 canvas-manager
☐ Python 3（macOS/大多数 Linux 自带，不用另装）
```

**可选**：在有真实教材的课程上跑过 [textbook-cracking](https://github.com/Geek96/textbook-cracking)——有的话，复习计划会链接真实的章节覆盖情况；没有的话，会老实地给出"暂无可用结构"的提示，而不是瞎编。

---

## 🧩 工作流

```
┌─────────────────────────────────────────────────────────────┐
│  canvas-manager           textbook-cracking（可选）           │
│  raw/, wiki/course_content/, wiki/info/    wiki/textbook_breakdown/  │
│           │                          │                        │
│           └──────────┬───────────────┘                        │
│                       ▼                                       │
│                 course-manager                                │
│         wiki/综合/（按课程） + 综合/学期关注.md（按学期）        │
│                       │                                       │
│                       ▼                                       │
│    {Semester}/_exports/planvault-time-sensitive.md            │
│         （合并安全——status 列永不被重置）                       │
│                       │                                       │
│                       ▼                                       │
│              PlanVault（每日规划，独立的 skill）                │
└─────────────────────────────────────────────────────────────┘
```

| 输出 | 范围 | 构建自 |
|--------|-------|-----------|
| `wiki/综合/作业总览.md` | 按课程 | canvas-manager 的作业证据 |
| `wiki/综合/公告时间线.md` | 按课程 | canvas-manager 的公告证据 |
| `wiki/综合/考试与截止日期.md` | 按课程 | 结构化截止/考试字段 + 从正文提取的日期 |
| `wiki/综合/课程复习计划.md` | 按课程 | 课程自身声明的结构，加上 textbook-cracking 的章节覆盖（如果有的话） |
| `wiki/综合/练习题/` | 按课程、按章节，可选 | textbook-cracking 的 `章节摘要/`+`证明/`，范围锚定在课程教学大纲上 |
| `wiki/综合/选择题练习/`+`选择题答案/`+`编程练习/` | 按课程、按周，可选 | textbook-cracking 的 `周次/` |
| `{Semester}/综合/学期关注.md` | 按学期 | 每门被追踪课程的 `考试与截止日期.md` |
| `_exports/planvault-time-sensitive.md` | 按学期 | 同一份时间敏感提取结果，暂存给 PlanVault 用 |

---

## 📖 示例提示词

```text
> 给我 2026 秋季学期的课程建一个截止日期视图
> 这周所有课加起来有什么要交的？
> 更新一下我给 PlanVault 用的时间敏感暂存文件
> MATH-4317-A 有没有只在公告里提过、教学大纲没写的日期？
> 给第 3 章生成练习题，范围要卡在 MATH-4317-A 实际布置的内容上
> 给 CS-1331 的第 3 周建练习——选择题加几个 LeetCode 链接
```

---

## 📁 项目结构

```text
course-manager/
├── FRAMEWORK.md                                # CourseOS 角色/契约定义
├── skills/course-manager/
│   ├── SKILL.md                              # skill 入口
│   ├── references/
│   │   ├── time-sensitive.md                 # 提取规则、置信度分级、暂存文件 schema
│   │   ├── practice-content.md               # 可选的练习题/周练习规则
│   │   ├── obsidian-rules.md                 # wiki/综合/ 布局、标记规则
│   │   ├── canvas-manager-integration.md     # 只读数据源契约
│   │   ├── textbook-cracking-integration.md  # 可选数据源契约
│   │   └── obsidian-core.md                  # 可移植的 Obsidian 创作基线
│   ├── templates/
│   │   ├── synthesis-template.md             # 4 份课程级笔记共用
│   │   ├── 学期关注-template.md
│   │   ├── 练习题-template.md                 # 可选，数学
│   │   ├── 选择题练习-template.md              # 可选，CS
│   │   ├── 选择题答案-template.md              # 可选，CS
│   │   └── 编程练习-template.md               # 可选，CS
│   └── scripts/merge_time_sensitive.py       # 保留状态的合并逻辑，仅用标准库
├── tests/test_merge_time_sensitive.py
├── .claude-plugin/plugin.json
└── README.md
```

---

## Development

```bash
python3 -m unittest discover -s tests -v
```

零外部依赖——只用 Python 3 标准库。

---

## 📄 License

MIT © [Geek96](https://github.com/Geek96)
