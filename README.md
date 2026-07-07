# Cangjie (仓颉) —— 内容结构化总结技能

[![GitHub Release](https://img.shields.io/github/v/release/Kirky-X/cangjie?style=flat-square)](https://github.com/Kirky-X/cangjie/releases)
[![GitHub License](https://img.shields.io/github/license/Kirky-X/cangjie?style=flat-square)](LICENSE)

Cangjie 是一个面向 AI agent 的内容结构化总结 skill，把**文本、音频、视频、转录稿、论文**整理成可归档的结构化文档：学习笔记、书籍总结、播客回顾、会议纪要、项目汇报、研究分析、论文阅读笔记，以及 PRD / TRD / BP / 竞品分析 / 文献综述等产品文档。

核心原则：**先识别用户目标，再选模板，再抽取高密度信息**。用户指定模板时始终优先；未要求"简版/超短版"时默认生成 `standard-detailed` 标准偏详细版本，而不是只给提纲。完整路由表与流程文档见 [SKILL.md](SKILL.md)。

## 功能特性

### 6 大模板族

| 模板族     | 代表模板                                                                          | 目标                         |
| ---------- | --------------------------------------------------------------------------------- | ---------------------------- |
| `learning` | `course-notes` / `nonfiction-book-summary` / `fiction-book-summary`              | 学习、复习、知识提炼         |
| `media`    | `podcast-summary` / `video-program-summary`                                       | 节目回顾、亮点传播           |
| `meeting`  | `decision-minutes` / `interview-record`                                           | 纪要、访谈、共创记录         |
| `business` | `project-status-report` / `executive-brief`                                       | 汇报、风险、行动跟踪         |
| `analysis` | `research-brief` / `decision-memo` / `paper-summary`（含理论/实验/系统/综述子类型）| 研究归纳、决策支持、论文阅读 |
| `product`  | `prd` / `trd` / `business-plan` / `competitive-analysis` / `literature-review`    | 产品文档、商业计划、技术设计 |

### 多模态输入处理

- **文本**：直接识别目标和结构；长书自动判断"全书 / 部分 / 章节"层级
- **音频**：自动判单人 / 多人，会议访谈走带发言人区分的 diarization 转录
- **视频**：先提音频再转录；画面/PPT/演示依赖型内容补视觉章节
- **论文**：自动识别类型（理论 / 实验 / 系统 / 综述）匹配子模板

### 输出质量护栏

- **强制文件落盘**：所有总结类输出必须写入 `.md` 文件，禁止仅在对话中展示
- **书籍默认多文件**：1 份全书总览 + N 份章节独立文件，全书文件必须有全书级提炼（不是章节摘要拼接）
- **密度可控**：`brief` / `standard-detailed`（默认）/ `deep-dive` 三档
- **事实不补造**：缺失信息显式标注"材料未提供/无法确认"，不假设
- **层级压缩**：章节数 >12 自动启用 `hierarchical-compression`，>20 时按核心章节加权

## 安装

### 方式一：通过 `skills` 包安装（推荐）

需 [Node.js](https://nodejs.org/) 18+ 和 `skills` npm 包（v1.5.12+）。

```bash
# 安装到 Claude Code
npx skills add https://github.com/Kirky-X/cangjie.git --agent claude-code -y

# 等价简写（owner/repo）
npx skills add Kirky-X/cangjie --agent claude-code -y

# 安装到 Trae
npx skills add Kirky-X/cangjie --agent trae -y

# 列出仓库中可被发现的所有 skills（不安装）
npx skills add https://github.com/Kirky-X/cangjie.git --list
```

安装后 skill 文件位于对应 agent 的 skills 目录（如 `.claude/skills/cangjie/`）。

### 方式二：传统 git clone

```bash
git clone https://github.com/Kirky-X/cangjie.git
# 将 SKILL.md + references/ + scripts/ 链接或复制到 agent skills 目录
# 各 runtime 的 skills 目录路径示例（任选其一）：
#   Claude Code:  ~/.claude/skills/cangjie/
#   Trae:         ~/.trae-cn/skills/cangjie/
#   Cursor:       ~/.cursor/skills/cangjie/
#   Codex:        ~/.codex/skills/cangjie/
```

## 使用示例

Cangjie 作为 skill 被 agent 加载后，通过自然语言意图触发，无需显式命令。触发词包括「总结」「内容总结」「会议纪要」「报告总结」「学习笔记」「播客总结」「视频总结」「论文总结」「转录」「PRD」「BP」「TRD」「竞品分析」「市场调研」「文献综述」等。

### 课程视频 → 学习笔记

```text
总结这个 Python 入门课程视频，整理成学习笔记
```

推荐模板：`learning/course-notes`（偏实操可追加 `learning/tutorial-playbook`）

### 非虚构书籍 → 全书 + 章节文件

```text
总结这本商业书，每章都要概括，并给我一份全书的核心论点总结
```

推荐模板：`learning/nonfiction-book-summary`（默认产出 1 份全书总览 + N 份章节独立文件）

### 项目例会 → 决策纪要

```text
根据这次项目例会录音生成纪要，要包含决策和待办
```

推荐模板：`meeting/decision-minutes`

### 论文阅读 → 子类型自动匹配

```text
总结这篇论文，告诉我研究主题、主要成果、关键公式和局限性
```

推荐模板：`analysis/paper-summary`，按内容信号自动细分到：
- 定理/证明/公式推导 → `analysis/theoretical-paper-summary`
- 数据集/指标/实验对比 → `analysis/experimental-paper-summary`
- 系统架构/吞吐延迟 → `analysis/systems-paper-summary`
- 文献综述/taxonomy → `analysis/survey-paper-summary`

### 产品需求文档

```text
帮我写一份 PRD，要包含用户旅程、功能详述、验收标准和非功能需求
```

推荐模板：`product/prd`

## 工具链

| 工具             | 安装命令                                          | 用途                |
| ---------------- | ------------------------------------------------- | ------------------- |
| `ffmpeg`         | `apt install ffmpeg`                              | 视频提音频          |
| `faster-whisper` | `pip install faster-whisper librosa torch`        | ASR 转录（主）      |
| `qwen-asr`       | `pip install qwen-asr torch`                      | ASR 转录（备选）    |
| `chub`           | 见 [`references/guides/api-docs.md`](references/guides/api-docs.md) | 拉取第三方 API 最新文档 |

GPU 检查：

```bash
python -c "import torch; print('CUDA:', torch.cuda.is_available())"
```

### 脚本

| 脚本                              | 用途                          |
| --------------------------------- | ----------------------------- |
| `scripts/extract_audio.py`        | 从视频提取音频                |
| `scripts/transcribe_with_diarization.py`  | 单人课程/演讲转录      |
| `scripts/transcribe_diarize_fw.py`        | 多人会议/访谈转录（带发言人区分） |

## 目录结构

```
cangjie/
├── SKILL.md                  # 主入口：路由表 / 工作流 / 输出规则
├── references/
│   ├── registry.yaml         # 模板注册表
│   ├── taxonomy.yaml         # 模板分类法
│   ├── families/*.yaml       # 6 大模板族定义
│   ├── guides/               # 模板选择 / 编写 / 输出骨架指南
│   ├── templates-index.md    # 模板索引（指向 ../templates/）
│   ├── meeting-minutes.md    # 会议纪要参考
│   ├── video-summary.md      # 视频总结参考
│   ├── audio-summary.md      # 音频总结参考
│   └── report-summary.md     # 报告总结参考
├── templates/                # 全部文档模板（产品层 / 战略层 / 交付层 / 运营层 / 技术层 / 通用）
└── scripts/                  # ASR / 提音频脚本
```

## 输出密度策略

| 模式                | 适用场景                         | 内容覆盖                             |
| ------------------- | -------------------------------- | ------------------------------------ |
| `brief`             | 用户明确要求快读版               | 仅结论 + 少量关键点 + 最小必要待办   |
| `standard-detailed` | **默认**                          | 全部必需章节 + 足够事实和证据        |
| `deep-dive`         | 用户要求"详细拆解/完整笔记/全面" | 增加章节内层次和证据密度（含公式/实验） |

## 反模式（禁止做）

- ❌ 把"章节标题 + 一句话"当成"标准详细摘要"输出
- ❌ 把"逐章摘要拼接"当成"全书总结"（全书文件必须有全书级提炼）
- ❌ 凭训练记忆写第三方 API 调用代码（必须先 `chub get`）
- ❌ 把"讨论纪要"伪装成"决策纪要"（缺 ACTION 项时不要补造责任人）
- ❌ 节选输入伪装成完整全书阅读结果
- ❌ 短章节硬凑内容（应标"材料未提供/无法确认"）

## 许可证

MIT
