# References Template System

本目录定义内容总结 skill 的模板体系。目标不是存放大量孤立 Markdown，而是提供一套可自动选择、可人工覆盖、可持续扩展的结构化模板库。

## 目录说明

```text
references/
  README.md
  registry.yaml
  taxonomy.yaml
  families/
    learning.yaml
    media.yaml
    meeting.yaml
    business.yaml
    analysis.yaml
    product.yaml
  guides/
    template-selection.md
    template-authoring.md
    output-skeletons.md
    api-docs.md
  templates/                # 完整 Markdown 文档模板（product 族引用）
    【模板】商业计划书.md
    【模板】商业模式文档.md
    【模板】会议纪要.md
    【模板】论文研究报告.md
    产品/
      战略层/               # BRD/MRD/竞品分析/项目任务书/市场调研
      产品层/               # PRD/FRD/UIUX规范
      技术层/               # TRD/架构/数据库/算法
      交付层/               # 发布计划/测试报告/灰度方案
      运营层/               # 数据看板/用户手册/运营手册
```

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
