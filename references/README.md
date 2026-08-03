# 参考资料模板体系

本目录定义内容总结 skill 的模板体系。目标不是存放大量孤立 Markdown，而是提供一套可自动选择、可人工覆盖、可持续扩展的结构化模板库。

## 目录说明

```text
references/
  README.md
  registry.yaml             # 模板注册表（所有模板 ID + required_sections + detection_signals）
  taxonomy.yaml             # 模板分类法（goals + signal_words + default_family）
  families/                 # 6 大模板族定义（每族默认模板 + 子模板清单 + selection_rules）
    learning.yaml
    media.yaml
    meeting.yaml
    business.yaml
    analysis.yaml
    product.yaml
  guides/                   # 模板选择 / 编写 / 输出骨架指南
    template-selection.md   # 模板选择决策树
    template-authoring.md   # 模板编写规范
    output-skeletons.md     # 输出骨架索引（按族拆分）
    skeletons-learning.md   # Learning 族骨架
    skeletons-media.md      # Media 族骨架
    skeletons-meeting.md    # Meeting 族骨架
    skeletons-business.md   # Business 族骨架
    skeletons-analysis.md   # Analysis 族骨架
    detail-policy.md        # 输出密度策略
    examples.md             # 完整示例集
    api-docs.md             # chub 工具使用与 API 文档拉取
  templates-index.md        # 模板索引（指向 ../templates/）
```

> 完整 Markdown 文档模板已迁移至 `../templates/`（产品层/战略层/交付层/运营层/技术层/通用），索引见 [templates-index.md](templates-index.md)。

## 设计原则

1. 用户指定优先于自动选择。
2. 模板按“输出目标”分组，而不是按输入媒介硬切。
3. 重复章节在模板族内合并，通过 `required_sections` 和 `optional_sections` 声明裁剪。
4. 一个模板定义既要能给 agent 用，也要能给人读懂。

## 模板族概览

| 模板族     | 覆盖内容                                 | 默认 fallback                    |
| ---------- | ---------------------------------------- | -------------------------------- |
| `learning` | 课程、讲座、书籍学习、教程整理           | `learning/course-notes`          |
| `media`    | 播客、节目、直播、公开视频回顾           | `media/podcast-summary`          |
| `meeting`  | 会议、讨论、访谈、1:1、工作坊            | `meeting/discussion-minutes`     |
| `business` | 周报、月报、项目状态、管理汇报           | `business/project-status-report` |
| `analysis` | 研究型归纳、论文阅读、主题综合、决策支持 | `analysis/research-brief`        |
| `product`  | 产品文档、商业计划、技术设计、交付运营   | `product/prd`                    |

## 当前模板原则

- 不做旧模板名称兼容。
- 对外只使用新的模板族和模板 ID。
- 后续新增模板时，继续按“输出目标”命名，不回退到旧的输入媒介命名。

## 论文模板分型

论文相关模板现在分为 5 个：

- `analysis/paper-summary`
- `analysis/theoretical-paper-summary`
- `analysis/experimental-paper-summary`
- `analysis/systems-paper-summary`
- `analysis/survey-paper-summary`

自动选择时，若能从内容中识别论文类型，应优先落到具体子模板；识别不明确时回落到 `analysis/paper-summary`。

## 书籍模板分型

书籍相关模板现在分为 2 个：

- `learning/nonfiction-book-summary`
- `learning/fiction-book-summary`

自动选择时，应先判断书籍是非虚构还是叙事类作品。两者默认都输出“逐章总结 + 全书总结”；如果输入只覆盖部分章节或节选，必须显式标注覆盖范围。
