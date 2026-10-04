# 输出骨架

各模板族的输出骨架（章节结构 + 字段提示）。生成最终输出时按所选模板的 `required_sections` 填充。

> 原始单文件已按族拆分（单文件曾超 500 行），按需加载对应族即可。

## 按族索引

- **[Learning 族](skeletons-learning.md)** — 课程笔记、教程 playbook、书籍总结（非虚构/虚构）、讲座摘要、概念解释
- **[Media 族](skeletons-media.md)** — 播客访谈、视频节目、活动回顾、亮点剪辑（演讲/讲座摘要属 Learning 族的 `learning/lecture-summary`）
- **[Meeting 族](skeletons-meeting.md)** — 决策纪要、讨论纪要、访谈记录、1on1、共创工作坊
- **[Business 族](skeletons-business.md)** — 项目状态、周报、高管简报、事故报告、行动计划
- **[Analysis 族](skeletons-analysis.md)** — 研究简报、论文总结（通用/理论/实验/系统/综述）、决策备忘录、主题综合、竞品扫描

> Product 文档族：骨架直接见 `../../templates/Product/` 下各产物模板文档（产物模板，非指导骨架），索引见 [templates-index.md](../templates-index.md)。

## 使用方式

1. 在 `references/registry.yaml` 查到模板的 `required_sections`
2. 打开对应族文件，定位 `### <模板 ID>` 段
3. 按骨架章节填充，遵循 SKILL.md 的 Output Rules 与 [detail-policy.md](detail-policy.md)
