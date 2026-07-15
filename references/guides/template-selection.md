# 模板选择指南

## 决策顺序

1. 用户是否明确指定模板或章节
2. 用户到底要“学会什么”还是“汇报什么”
3. 输入内容是单次材料还是多份材料综合
4. 是否存在决策、待办、指标、权衡等强信号
5. 不确定时回落到对应模板族的默认模板

## 一句话判断法

- 如果目标是“学会”和“复习”，选 `learning/*`
- 如果目标是“回顾内容”和“传播亮点”，选 `media/*`
- 如果目标是“记录讨论”和“追踪责任”，选 `meeting/*`
- 如果目标是“向上汇报”或“跟踪进展”，选 `business/*`
- 如果目标是“归纳多源信息并支持判断”，选 `analysis/*`
- 如果目标是“读懂一篇论文”，优先选 `analysis/paper-summary`
- 如果目标是“总结一本书”，优先在 `learning/nonfiction-book-summary` 和 `learning/fiction-book-summary` 之间分流
- 如果目标是“写产品文档”或“做商业计划”，选 `product/*`
- 如果目标是“写技术方案”或“设计架构”，选 `product/trd` 或 `product/architecture`
- 如果目标是“正式归档的详细会议纪要”（含 ACTION 编号、Parking Lot），选 `product/meeting-minutes-detailed`
- 如果目标是“建立评判框架的文献综述”（含 PRISMA、场景化推荐），选 `product/literature-review`

## 常见歧义

### 课程视频 vs 产品演示

- 想让读者掌握知识：`learning/course-notes`
- 想让读者照着操作：`learning/tutorial-playbook`
- 想回顾节目内容而非教学：`media/video-program-summary`

### 课程笔记 vs 书籍总结

- 重点是课程、训练营、讲授内容：`learning/course-notes`
- 重点是整本非虚构书的结构、论点、逐章内容：`learning/nonfiction-book-summary`
- 重点是整本小说或叙事作品的人物、情节、主题：`learning/fiction-book-summary`

### 播客访谈 vs 访谈记录

- 面向内容消费和观点提炼：`media/podcast-summary`
- 面向研究输入和问答整理：`meeting/interview-record`

### 会议纪要 vs 项目汇报

- 重点是讨论过程、决策、待办：`meeting/decision-minutes`
- 重点是阶段进展、指标、风险：`business/project-status-report`

### 综合材料总结

- 重点是共性主题：`analysis/theme-synthesis`
- 重点是做选择：`analysis/decision-memo`
- 重点是行业和事实扫描：`analysis/research-brief`

### 论文阅读

- 想知道研究主题、方法、公式、实验和缺陷：`analysis/paper-summary`
- 如果论文只是多份证据材料中的一个组成部分，再考虑切到 `analysis/research-brief` 或 `analysis/theme-synthesis`

### 书籍总结

- 非虚构、方法论、商业、心理、历史、科普类书籍：`learning/nonfiction-book-summary`
- 小说、文学、叙事类作品：`learning/fiction-book-summary`
- 默认输出应包含“逐章总结 + 全书总结”，除非用户明确要求只要其中一层
- 默认输出形态是“全书文件 + 章节独立文件目录”，除非用户明确要求单文件合并
- 如果输入只覆盖部分章节或节选，必须在摘要开头说明覆盖范围
- 如果原书有“部分/篇/卷”结构，摘要默认保留这一层，不直接打平成章节长列表
- 章节很多时，不要求每章平均篇幅；优先让关键章节更详细，附录性章节更简洁

### 论文子类型判断

- 如果核心是定理、证明、收敛性、上下界：`analysis/theoretical-paper-summary`
- 如果核心是数据集、实验指标、benchmark、ablation：`analysis/experimental-paper-summary`
- 如果核心是系统架构、吞吐、延迟、扩展性、部署：`analysis/systems-paper-summary`
- 如果核心是分类框架、文献梳理、研究脉络、空白点：`analysis/survey-paper-summary`
- 如果看不出明确子类型：`analysis/paper-summary`

### 产品文档子层选择

- 商业计划书、融资路演：`product/business-plan`
- 商业模式、价值主张、盈利路径：`product/business-model`
- 商业需求、项目立项、战略层：`product/brd`
- 市场调研、行业分析：`product/market-research`
- 市场需求、产品规划：`product/mrd`
- 竞品分析、竞争格局、差异化：`product/competitive-analysis`
- 项目启动、任务书：`product/charter`
- 产品需求、功能设计：`product/prd`
- 功能需求细化：`product/frd`
- UIUX 规范、配色体系：`product/uiux-spec`
- 技术方案、架构选型：`product/trd`
- 系统架构、模块设计：`product/architecture`
- 数据库设计、表结构：`product/db-design`
- 核心算法说明：`product/algorithm-doc`
- 发布计划、上线排期：`product/release-plan`
- 测试报告、质量报告：`product/test-report`
- 灰度发布、分批上线：`product/canary-plan`
- 数据看板、指标体系：`product/dashboard`
- 用户手册、使用说明：`product/user-guide`
- 运营手册、运营流程：`product/operation-guide`
- 不确定子层时：`product/prd`

### 竞品分析 vs 竞品扫描

- 面向产品决策、含差异化策略和护城河：`product/competitive-analysis`
- 面向研究归纳、轻量级同类对比：`analysis/competitive-scan`

### 详细会议纪要 vs 标准决策纪要

- 需要正式归档、含 ACTION/RISK 编号、Parking Lot、FAR 原则：`product/meeting-minutes-detailed`
- 快速记录决策和待办：`meeting/decision-minutes`

### 文献综述报告 vs 综述论文总结

- 需要建立评判框架、含 PRISMA 流程、场景化推荐：`product/literature-review`
- 总结单篇综述论文的分类框架：`analysis/survey-paper-summary`

## 向用户确认时建议说明

最少说明三件事：

1. 选中的模板 ID
2. 核心章节
3. 为什么它比相邻模板更合适

示例：

> 我建议用 `meeting/decision-minutes`，因为你的内容里有明确决策、负责人和截止时间。核心章节会包括讨论摘要、决策、待办和风险。如果你更想看按发言人整理，我可以切到 `meeting/discussion-minutes`。
