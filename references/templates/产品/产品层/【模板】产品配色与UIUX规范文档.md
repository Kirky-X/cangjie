# [产品/系统名称（英文名）] - 产品配色与UIUX规范文档（UI/UX Specification）

> **文档状态：** 🟡 评审中 / 🟢 已通过 / 🔴 驳回
>
> **保密级别：** 机密 / 内部公开 / 公开
>
> **版本：** v0.1.0
>
> **日期：** YYYY-MM-DD
>
> **撰写人：** [姓名/角色]
>
> **评审人：** [姓名/角色]
>
> **阅读对象：** [角色列表]
>
> **适用范围：** Web / iOS / Android / 桌面端
>
> **关联文档：** [产品需求文档 PRD]、[品牌手册 Brand Guidelines]

---

## 0. 文档导读

### 0.1 文档目的与适用范围

[说明本文档的目的、适用场景和不适用场景]

### 0.2 相关文档

| 文档类型 | 文件名 | 相关章节 |
|---------|--------|---------|
| [类型] | [文件名] [行号范围] | [章节描述] |

> **引用格式说明**：关联文档使用 `文件名 行号范围` 格式（如 `【模板】技术需求文档(TRD).md 3-17`），行号随文档更新可能变化，请以实际内容为准。

### 0.3 变更记录

| 版本 | 日期 | 修订人 | 变更内容 | 审核人 |
| :--- | :--- | :--- | :--- | :--- |
| v0.1.0 | YYYY-MM-DD | [姓名] | 初稿发布 | [审核人] |

---

## 1. 设计原则与概述

### 1.1 设计愿景

用 1-2 句话描述产品的视觉气质。例如：
> 以「专业、可信、轻盈」为核心，通过克制的色彩层级与清晰的交互反馈，帮助用户高效完成复杂任务。

### 1.2 核心原则

| 原则 | 描述 | 设计体现 |
|------|------|----------|
| **一致性** | 相同场景使用相同视觉语言 | Token 命名、组件状态、交互动效全局统一 |
| **层级感** | 通过颜色与阴影区分信息优先级 | 分层模型（Layering Model）定义页面深度 |
| **无障碍** | 所有用户均可无障碍使用 | 符合 WCAG 2.1 AA 级对比度标准，双重编码原则 |
| **响应式** | 适配多端与主题切换 | 支持 Light / Dark / High-Contrast 模式 |
| **证据驱动** | 设计决策基于实证而非直觉 | 配色数量、字阶倍率、间距基准均有行业共识支撑 |
| **触控友好** | 最小点击热区 >= 44x44px | 移动端按钮高度 48-52px，确保手指点击舒适 |
| **呼吸感** | 合理使用间距避免拥挤 | 4/8/12/16/24px 间距体系，信息层级清晰 |
| **克制用色** | 主色按行业选择，功能色统一 | 品牌色覆盖面积 <= 10%，中性色构建文字层级 |

> **移动端设计核心结论**：好的排版来自清晰的信息层级，而不是花哨字体。统一性、层级清晰、适配优先、触控友好、呼吸感、克制用色是 APP 设计的 6 大核心原则。

### 1.3 Design Token 架构总览

本规范采用 **三层 Token 架构**，遵循 DTCG（W3C Design Tokens Community Group）规范：

| 层级 | 命名模式 | 示例 | 说明 |
|------|---------|------|------|
| **Primitive（原语层）** | `{color}-{scale}` | `ink-green-700` | 平台无关的原始色值，不直接用于组件 |
| **Semantic（语义层）** | `{purpose}[-variant][-{state}]` | `text-primary`、`bg-surface-hover` | 绑定主题的语义角色，支持 Light/Dark 切换 |
| **Component（组件层）** | `{component}-{property}[-{state}]` | `btn-primary-bg-hover` | 框架特定的组件级 Token |

> **State（状态）作为第四维度**：每个语义 Token 必须定义至少 6 种状态（Default, Hover, Active, Focus, Selected, Disabled），否则组件在不同交互状态下的色彩一致性将无法保证。

**Token 命名规则**：
- 使用小写字母 + 点号/连字符分隔
- 语义 Token 名描述 **用途** 而非 **值**（如 `color.text.primary` 而非 `color.text.black`）
- Token 总数建议控制在 200 以内，超过后管理成本指数增长

---

## 2. 颜色系统（Color System）

> **核心思想**：采用三层 Token 体系，所有颜色不直接使用 Hex 值，而是通过语义化 Token 调用。Token 命名规则：`{category}.{property}.{variant}.{state}`
> 例：`color.background.primary.default`、`color.text.inverse`、`color.border.danger.hovered`

### 2.1 品牌色板（Brand Palette）

采用**单品牌色**策略：仅定义 1 个品牌主色，通过梯度扩展覆盖所有使用场景。单色策略的优势：视觉焦点集中、开发维护成本低、跨平台一致性高。

| Token 名称 | Light 模式值 | Dark 模式值 | 使用场景 |
|------------|--------------|-------------|----------|
| `color.brand` | [主色 Hex] | [主色 Dark Hex] | 主按钮、Logo、导航激活态、链接、图标强调 |

> **设计约束**：辅助强调和图表系列色从语义色板（§2.3）和中性色板（§2.5）中获取，不额外定义品牌色。

**行业品牌色推荐**：

| 行业类型 | 推荐色值 | 说明 |
|---------|---------|------|
| 零售/消费/电商 | `#3B82F6`（蓝色） | 信任、专业、稳定 |
| 直播/社交/内容 | `#8B5CF6`（紫色） | 创意、活力、年轻 |
| 健康/运动/出行 | `#10B981`（绿色） | 健康、自然、活力 |
| 工具/效率/科技 | `#14B8A6`（青色） | 科技、高效、清新 |

> **品牌色选择建议**：根据产品行业属性选择主色，确保品牌色与产品定位一致。品牌色覆盖面积 <= 10%。

**品牌色扩展梯度（Gradient Scale）**：
定义 9 级梯度（50-900），以 **600 色阶为基准色（Base Color）**。600 色阶在白色背景上通常能达到 4.5:1-7:1 的对比度，满足 WCAG AA-AAA 标准。

| 梯度 | 色值（Light） | 色值（Dark） | 用途 |
|------|---------------|--------------|------|
| `brand-50` | [Hex] | [Hex] | 极浅背景、hover 底色 |
| `brand-100` | [Hex] | [Hex] | 轻量背景、选中态底色 |
| `brand-200` | [Hex] | [Hex] | 浅色装饰元素 |
| `brand-300` | [Hex] | [Hex] | 次要图标、辅助文字 |
| `brand-400` | [Hex] | [Hex] | 中等强调 |
| `brand-500` | [Hex] | [Hex] | Hover 状态、图表辅助色 |
| `brand-600` | [Hex] | [Hex] | **基准色（默认）** |
| `brand-700` | [Hex] | [Hex] | Pressed/Active 状态 |
| `brand-800` | [Hex] | [Hex] | 深色文字（on-light） |
| `brand-900` | [Hex] | [Hex] | 极深装饰、深色背景强调 |

> **隐藏规则**：不要以 400 或 500 作为基准色，因为它们的对比度往往不足以覆盖所有使用场景。

### 2.2 色彩面积规则（60-30-10）

| 比例 | 角色 | 说明 |
|------|------|------|
| 60% | 主色/底色 | 页面背景、大面积填充 |
| 30% | 辅助色 | 卡片、侧边栏、次要区域 |
| 10% | 强调色 | CTA 按钮、关键图标、焦点元素 |

**色彩面积审计清单**：

- [ ] 页面背景色覆盖面积 >= 60%
- [ ] 卡片/面板色覆盖面积 ~30%
- [ ] 品牌强调色覆盖面积 <= 10%
- [ ] 每屏品牌色 CTA 按钮 <= 1 个
- [ ] 品牌色仅用于可交互元素（按钮、链接、图标），不用于大面积背景

### 2.3 语义色板（Semantic / Functional Palette）

用于传达状态、反馈和紧急程度，独立于品牌色。行业共识：4 种核心语义色（Success/Warning/Error/Info）。

| 语义 | Token | Light | Dark | 使用场景 |
|------|-------|-------|------|----------|
| **成功 Success** | `color.semantic.success` | `#22C58B` | `#34D399` | 成功提示、完成状态、正向指标 |
| **警告 Warning** | `color.semantic.warning` | `#FFB020` | `#FBBF24` | 警告提示、需关注事项 |
| **错误 Error** | `color.semantic.error` | `#FF5A6B` | `#F87171` | 错误提示、删除确认、表单校验失败 |
| **信息 Info** | `color.semantic.info` | `color.brand-600` | `color.brand-400` | 信息提示、中性通知（复用品牌色） |

**语义色浅色背景变体**：

| 语义 | 浅色背景 Token | 浅色背景值 | 用途 |
|------|--------------|-----------|------|
| **成功** | `color.semantic.success.subtle` | `#CFF5E7` | 成功提示背景 |
| **警告** | `color.semantic.warning.subtle` | `#FFE8B5` | 警告提示背景 |
| **错误** | `color.semantic.error.subtle` | `#FFD7DC` | 错误提示背景 |
| **信息** | `color.semantic.info.subtle` | `#D9E7FF` | 信息提示背景 |

> **单品牌色策略下的语义色复用**：Info 语义色直接复用品牌色梯度，不额外定义。品牌色 600（Light）和 400（Dark）分别作为信息提示的默认色值。

**语义色扩展规则**：每个语义色至少包含 5 个变体：

| 变体 | 命名后缀 | 用途 |
|------|---------|------|
| `default` | `color.semantic.error` | 默认态 |
| `hovered` | `color.semantic.error.hovered` | 鼠标悬停 |
| `pressed` | `color.semantic.error.pressed` | 按下/激活 |
| `subtle` | `color.semantic.error.subtle` | 浅色背景（如错误输入框底色） |
| `contrast` | `color.semantic.error.contrast` | 文字/图标色（确保在 subtle 背景上可读） |

### 2.4 色彩语义与心理学考量

> 填写品牌色选择的心理含义与文化考量。色彩语义并非普适，而是深度受文化建构影响。**注意力是生理的，含义是文化的**——红色在所有文化中都吸引注意力（波长决定），但红色传递的含义因文化而异。详见 `UI设计规范系统性研究报告.md` §5.1。

[填写本产品品牌色的心理含义、文化差异考量、饱和度/明度策略]

**关键原则**：永远不要让颜色成为语义的唯一载体。如果错误状态仅通过红色传达"错误"，它在跨文化场景中会失效。必须配合图标、文本、形状等双重编码。

### 2.5 中性色板（Neutral Palette）

构建界面骨架、文字、边框、分割线。使用蓝灰（Blue-Gray）或暖灰，避免纯黑 `#000000`。

| Token | Light 模式 | Dark 模式 | 使用场景 |
|-------|-----------|-----------|----------|
| `color.neutral-50` | `#F3F6FB` | [Hex] | 页面全局背景（Global Background） |
| `color.neutral-100`| [Hex] | [Hex] | 卡片背景、输入框背景 |
| `color.neutral-200`| `#E5E7EB` | [Hex] | Hover 背景、分割线 |
| `color.neutral-300`| `#D1D5DB` | [Hex] | 禁用边框、次要分割线 |
| `color.neutral-400`| `#9CA3AF` | [Hex] | 占位符文字、禁用文字 |
| `color.neutral-500`| `#6B7280` | [Hex] | 正文文字（次要）、图标默认态 |
| `color.neutral-600`| `#374151` | [Hex] | 辅助文字（深色正文） |
| `color.neutral-700`| `#1A1B27` | [Hex] | 标题文字、主图标 |
| `color.neutral-800`| [Hex] | [Hex] | 次要标题 |
| `color.neutral-900`| [Hex] | [Hex] | 标题文字、主图标 |

**中性色文字层级规范**：

| 用途 | 色值 | 说明 |
|------|------|------|
| 标题 | `#1A1B27` | 最深，用于页面核心主题 |
| 深色正文 | `#374151` | 重要段落正文 |
| 正文 | `#6B7280` | 页面主要信息内容 |
| 辅助文字 | `#9CA3AF` | 补充说明、次要信息 |
| 分割线 | `#D1D5DB` | 内容分隔 |
| 边框 | `#E5E7EB` | 组件边框 |
| 页面背景 | `#F3F6FB` | 页面底色（非纯白，减少视觉疲劳） |

### 2.6 分层模型（Layering Model）

定义界面元素的「深度」与「堆叠逻辑」，确保在复杂页面中视觉层级清晰。

**Light 模式分层**：
- **Layer 0（Base）**：`neutral-50` — 页面最底层背景
- **Layer 1（Surface）**：`neutral-100` — 卡片、弹窗、侧边栏
- **Layer 2（Raised）**：`neutral-0`（纯白）— 下拉菜单、浮层、Tooltip
- **Layer 3（Overlay）**：带透明度的黑色遮罩 `rgba(0,0,0,0.45)` — 模态框背景

**Dark 模式分层**（非对称映射，非简单反转）：
- **Layer 0**：`neutral-50`（最深）
- **Layer 1**：`neutral-100` — 比底层略浅（向上凸起感）
- **Layer 2**：`neutral-200` — 浮层继续提亮
- **Layer 3**：`rgba(0,0,0,0.75)` — 遮罩更深

> **核心原则**：Dark Mode 不是 Light Mode 的"反色"，而是独立的色彩空间。每个 Token 的 Dark 值需要独立设计和验证，不能通过算法反转。

### 2.7 颜色角色映射（Color Roles）

将 Token 映射到具体 UI 元素，确保「背景-文字-图标」对比度合规。

| 角色 | 背景 Token | 文字/图标 Token | 用途 |
|------|-----------|----------------|------|
| **Primary** | `color.brand-600` | `color.text.on-brand` | 主按钮、FAB、关键行动点 |
| **Secondary** | 透明 | `color.brand-600` | 次级按钮、筛选标签 |
| **Surface** | `color.background.surface` | `color.text.primary` | 卡片、面板 |
| **Inverse** | `color.background.inverse` | `color.text.inverse` | 深色横幅、Toast |
| **Danger** | `color.semantic.error` | `color.text.on-danger` | 删除按钮、强警示 |
| **Disabled** | `color.background.disabled` | `color.text.disabled` | 禁用态元素 |

### 2.8 暗/亮模式映射表（Theme Mapping）

| Token | Light | Dark | 映射逻辑 |
|-------|-------|------|---------|
| `color.background.default` | [Hex] | [Hex] | 页面底色，暗模式非纯黑保留深度感 |
| `color.background.surface` | [Hex] | [Hex] | 卡片底色，暗模式 Elevated 更亮 |
| `color.brand-600` | [主色 Hex] | [主色 Dark Hex] | 主按钮背景，暗模式提亮至 400 色阶 |
| `color.text.primary` | [Hex] | [Hex] | 主标题/正文，暗模式非纯白减少 Halation 眩光 |
| `color.text.secondary`| [Hex] | [Hex] | 次要说明文字 |
| `color.text.disabled` | [Hex] | [Hex] | 禁用态文字 |
| `color.border.default` | [Hex] | [Hex] | 默认边框 |
| `color.border.focus` | `color.brand-600` | `color.brand-400` | 聚焦态边框（2px） |

> **暗色模式品牌色映射**：Light 模式使用 600 色阶，Dark 模式提亮至 400 色阶，确保在深色背景上对比度充足。

### 2.9 色彩对比度标准

#### 2.9.1 WCAG 2.1 对比度要求

| 等级 | 正常文字（<18px / 非 bold <14px） | 大文字（>=18px / bold >=14px） | UI 组件 / 图形对象 |
|------|------|------|------|
| **AA（最低）** | >= 4.5:1 | >= 3:1 | >= 3:1 |
| **AAA（增强）** | >= 7:1 | >= 4.5:1 | 未定义 |

#### 2.9.2 APCA 对比度算法（WCAG 3.0 候选）

APCA 是 WCAG 2.x 对比度算法的继任者，考虑文字颜色和背景颜色的方向性、字体大小和字重的交互效应：

| 对比度等级 | APCA 最低值（Lc） | 用途 |
|-----------|-------------------|------|
| 正文文字 | Lc >= 60 | 正文可读性 |
| 大文字 | Lc >= 45 | 标题、大字号 |
| 最低可感知 | Lc >= 15 | 装饰性文字 |
| 最佳可读性 | Lc >= 75 | 长篇阅读正文 |

#### 2.9.3 暗色模式对比度策略

| 策略 | 行业建议 | 理论依据 |
|------|---------|---------|
| 底色不用纯黑 | 使用 `#121212` 或带色调的深灰 | 暖灰底比纯黑底视觉舒适度更高 |
| 文字不用冷白 | 使用 `#E0E0E0` 或暖白 | Halation 效应：高亮度文字在深色背景上产生光晕扩散 |
| 品牌色提亮 | 暗色模式提亮 1-2 色阶 | 保持视觉权重一致 |
| 状态色提亮 | 暗色模式使用 400 色阶 | 400 色阶在深色背景上对比度更优 |
| 阴影加重 | 暗色模式通过边框替代阴影 | 暗色模式下阴影效果减弱 |

### 2.10 色觉缺陷（CVD）无障碍

约 8% 的男性和 0.5% 的女性存在色觉缺陷。关键规范：

- 语义色不能仅通过颜色区分，必须辅以图标、文字、形状（WCAG SC 1.4.1）
- Error（红）和 Success（绿）在 Deuteranopia 模式下可能混淆，需确保图标+文字辅助
- 色板应通过 CVD 模拟验证：Protanopia / Deuteranopia / Tritanopia 三种模式
- 推荐工具：Sim Daltonism（macOS）、Color Oracle（跨平台）、Chrome DevTools 模拟

### 2.11 高对比度模式

- 高对比度模式下阴影完全失效，必须依赖 **边框（Border）** 和 **轮廓（Outline）** 区分层级
- Focus 颜色在深色背景上可能需要自定义
- 所有状态变化不能仅依赖颜色，必须配合 **图标、文本标签或形状变化**
- 适配 `prefers-contrast: more` 媒体查询

---

## 3. 排版系统（Typography）

> 所有文字使用 Token 管理：`font.family`、`font.size`、`font.weight`、`line.height`、`letter.spacing`

### 3.1 字体栈

| 场景 | 字体栈 | Token |
|------|--------|-------|
| 西文/数字 | `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto` | `font.family.base` |
| 中文 | `"PingFang SC", "Microsoft YaHei", "Noto Sans SC"` | `font.family.chinese` |
| 代码 | `"SF Mono", "Fira Code", Consolas` | `font.family.code` |

**字体加载策略**：

- 使用 `font-display: swap` 避免 FOIT（Flash of Invisible Text），确保文字立即可见
- 关键字体预加载：`<link rel="preload" as="font" crossorigin href="...">`
- 中文字体按需加载（`unicode-range` 分片），减少首次加载体积
- 字体加载失败时回退到系统字体栈，不阻塞渲染

**字体配对规则**：
1. 最多 2 个字体家族：1 个标题字体 + 1 个正文字体，第 3 个仅用于代码
2. 对比原则：衬线 + 无衬线配对最经典（如 Noto Serif SC + Noto Sans SC）
3. x-height 匹配：配对字体的 x-height 应接近
4. 中文配对：标题用宋体/衬线（文化感），正文用黑体/无衬线（可读性）

### 3.2 字阶倍率体系

| 倍率名称 | 比值 | 适用场景 |
|----------|------|----------|
| Minor Second | 1.067 | 紧凑信息架构、数据密集型 |
| Major Second | 1.125 | 微妙层级、企业后台 |
| **Minor Third** | **1.2** | **移动端、紧凑布局** |
| **Major Third** | **1.25** | **通用、平衡（推荐）** |
| Perfect Fourth | 1.333 | 宽松层级、品牌展示 |
| Augmented Fourth | 1.414 | 戏剧性对比、创意类 |
| Perfect Fifth | 1.5 | 极端对比、大屏展示 |

> **推荐**：1.25x（Major Third）倍率与 IBM Carbon 一致，属于行业通用平衡选择。

### 3.3 字号层级（Type Scale）

| Token | 字号 | 行高 | 字重 | 用途 |
|-------|------|------|------|------|
| `font.heading.xxl` | 28-32px | 1.2 | 700 | 页面大标题（移动端 H1） |
| `font.heading.xl` | 22-24px | 1.3 | 600 | 模块标题（移动端 H2） |
| `font.heading.lg` | 18-20px | 1.35 | 600 | 卡片标题 |
| `font.body.large` | 16px | 1.5 | 400 | 正文（移动端默认，行长 25-35 字） |
| `font.body.base` | 14px | 1.5 | 400 | **默认正文（桌面端）** |
| `font.body.small`| 12px | 1.4 | 400 | 辅助文字、时间戳、注释 |
| `font.label` | 14px | 1.2 | 500 | 按钮文字、标签 |

> **移动端字号规范**：主标题与正文要有明显区分；正文与辅助文字至少拉开 2px；不靠花哨字体代替信息层级。核心结论：好的排版来自清晰的信息层级。

### 3.4 中文排版特殊性

| 规范项 | 推荐值 | 说明 |
|--------|--------|------|
| 正文字号 | 14-16px | 14px 适合信息密集型，16px 适合阅读型 |
| 最小字号 | 12px | 低于 12px 阅读速度显著下降 |
| 行高（中文正文） | 1.6-1.8 | 中文字符无升部/降部，行间视觉密度更高 |
| letter-spacing | 0 | 中文等宽，无需额外间距 |
| 标题 letter-spacing | 0-0.05em | 可微增呼吸感 |
| 中英混排 | 西文字号比中文小 1-2px | 西文字母 x-height 通常小于中文字面 |
| 中文字重 | 最低使用 Regular（400） | Light（300）在中文场景下可读性极差 |

### 3.5 行高推荐值

| 字号范围 | 推荐行高倍数 | 说明 |
|----------|-------------|------|
| 32px+ | 1.1-1.25 | 大标题，行间距紧凑 |
| 24-31px | 1.25-1.35 | 中标题 |
| 18-23px | 1.35-1.45 | 小标题 |
| 14-17px | 1.5-1.7 | 正文（中文偏高） |
| 10-13px | 1.4-1.6 | 辅助文字 |

### 3.6 跨平台排版映射

同一语义 Token 在不同平台的具体映射需要独立定义，不能简单地将 px=pt=sp：

| Token | iOS | Android | Web |
|-------|-----|---------|-----|
| `font.body.large` | [N]pt / [N] / [N]pt 行高 | [N]sp / [N] / [N]sp 行高 | [N]px / [N] / [N] 行高 |
| `font.body.base` | [N]pt / [N] / [N]pt 行高 | [N]sp / [N] / [N]sp 行高 | [N]px / [N] / [N] 行高 |
| `font.label` | [N]pt / [N] / [N]pt 行高 | [N]sp / [N] / [N]sp 行高 | [N]px / [N] / [N] 行高 |

### 3.7 响应式排版缩放

| 断点 | 标题缩放 | 正文缩放 | 说明 |
|------|---------|---------|------|
| Mobile (<640px) | -2px | 不变 | 仅标题缩小 |
| Tablet (640-1024px) | -1px | 不变 | 过渡 |
| Desktop (>1024px) | 基准 | 基准 | 完整尺寸 |
| Large (>1440px) | +2-4px | +1-2px | 大屏放大 |

推荐使用 CSS `clamp()` 实现标题流式缩放：`font-size: clamp(1.5rem, 1.5rem + 0.5vw, 2.5rem)`。

### 3.8 Dynamic Type 阶梯式缩放

移动端需支持系统级字号缩放（Apple Dynamic Type / Android Font Size）。缩放不是简单的线性放大，而是 **阶梯式（Stepped）缩放**：

| Accessibility Size | 缩放比例 | 设计约束 |
|-------------------|---------|---------|
| XS（默认） | 1.0x | 基准布局 |
| L | 1.35x | 测试布局是否溢出 |
| XL | 1.65x | 文字可能需要截断 |
| XXXL | 2.35x | 所有 UI 布局必须支持文字截断或自动换行 |
| AX5（最大） | 4.59x | 触摸目标必须仍然可用 |

> **关键规则**：超过 AX3 后，所有 UI 布局必须支持 **文字截断（Truncation）** 或 **自动换行（Wrapping）**。

---

## 4. 间距与网格系统（Spacing & Grid）

> 基于 4px / 8px 基准单位，行业共识：4px 最小单位 + 8px 常用基准。

### 4.1 间距刻度

| Token | 值 | 用途 |
|-------|-----|------|
| `space.0` | 0px | 无间距 |
| `space.1` | 4px | 图标与文字间隙、标签内间距 |
| `space.2` | 8px | 紧凑内边距、列表项间距 |
| `space.3` | 12px | 按钮内部横向 padding、同组内容次级分隔 |
| `space.4` | 16px | 卡片内边距、表单间距、独立模块分隔 |
| `space.5` | 20px | 模块间距 |
| `space.6` | 24px | 段落间距、页面大区块分隔 |
| `space.8` | 32px | 区块间距 |
| `space.10` | 40px | 大区块间距 |
| `space.12`| 48px | 页面级间距 |
| `space.16`| 64px | 大模块分隔 |

**移动端间距规范**：

| 间距值 | 适用场景 |
|--------|---------|
| 4px | 图标、标签、数字与文字之间的细小内间距调整 |
| 8px | 列表项、按钮组、信息行等常见组件之间的标准间距 |
| 12px | 同组内容里的次级分隔，让内容切换更顺畅 |
| 16px | 独立模块之间的常规分隔，兼顾清晰度与页面密度 |
| 24px | 页面大区块之间，拉开主次层级，让信息呼吸感更强 |

> **呼吸感原则**：合理使用间距（4/8/12/16/24px），避免页面拥挤。间距比 >= 3:1 时分组感知显著增强。

### 4.2 间距语义分层

Nathan Curtis 提出的三层间距策略已成为行业最佳实践：

| 层级 | 间距范围 | 用途 | 示例 |
|------|---------|------|------|
| **组件内**（intra-component） | 4/8/12px | 元素内部间距 | 按钮内 padding、图标与文字间距 |
| **组件间**（inter-component） | 16/24px | 同组组件间距 | 表单字段间距、列表项间距 |
| **布局级**（layout） | 32/48/64px | 区块/页面级间距 | 卡片间距、区块间距 |

### 4.3 间距语义命名策略

数值命名适合 Primitive 层，语义命名适合 Semantic 层（推荐）：

| 语义 Token | Compact 模式 | Default 模式 | Comfortable 模式 | 用途 |
|-----------|-------------|-------------|-----------------|------|
| `space.compact` | 4px | 8px | 12px | 紧凑模式 |
| `space.default` | 12px | 16px | 20px | 默认模式 |
| `space.comfortable` | 20px | 24px | 32px | 舒适模式 |
| `space.loose` | 28px | 32px | 40px | 宽松模式 |

> **密度是场景属性而非平台属性**：同一平台的不同页面可以使用不同密度（如 Dashboard 用 Compact，详情页用 Comfortable）。

### 4.4 格式塔邻近性量化

| 元素间距 | 感知分组 | 应用场景 |
|---------|---------|---------|
| < 8px | 同一组 | 图标+文字、标签+值 |
| 8-16px | 关联组 | 表单字段、列表项 |
| > 24px | 独立组 | 区块分隔、卡片间距 |

> 间距比 >= 3:1 时分组感知显著增强。

### 4.5 响应式断点标准

| 断点名称 | 宽度范围 | 列数 | Gutter | Margin | 触控目标 |
|----------|---------|------|--------|--------|---------|
| **xs** | < 480px | 4 | 16px | 16px | 44-48px |
| **sm** | 480-639px | 4 | 16px | 16px | 44-48px |
| **md** | 640-767px | 8 | 16-24px | 24px | 44-48px |
| **lg** | 768-1023px | 8 | 24px | 24px | 36-44px |
| **xl** | 1024-1439px | 12 | 24px | 32px | 36-44px |
| **2xl** | >= 1440px | 12 | 24-32px | 32px | 36-44px |

> **768px（lg）是所有体系的共识断点**，对应 iPad 竖屏。学术研究支持 3-5 个断点为最优。

### 4.6 布局模式分类

组件在网格系统中的排列遵循 6 种基本布局模式：

| 模式 | 描述 | 适用场景 | 代表组件 |
|------|------|---------|---------|
| **Stack** | 垂直/水平等距排列 | 列表、按钮组 | VStack / HStack |
| **Inline** | 水平排列，自动换行 | 标签、筛选器 | Tag Group / Breadcrumb |
| **Grid** | 二维网格布局 | 卡片列表、图库 | Data Table / Gallery |
| **Box** | 固定宽高比容器 | 图片、视频 | Aspect Ratio Box |
| **Center** | 水平垂直居中 | 空状态、加载页 | Empty State / Spinner |
| **Bleed** | 突破容器边距 | 全宽 Banner、Hero 图 | Hero Banner / Full-width CTA |

### 4.7 非对称边距与最大宽度约束

| 断点 | 左/右边距 | 实际行为 |
|------|----------|---------|
| Mobile | 16px | 固定边距 |
| Tablet | 24px | 固定边距 |
| Desktop | 32px | 固定边距 |
| Large Desktop | 32px | 固定边距 |
| Max (>1440px) | 自动居中 | 内容区最大宽度 [如 1200px]，两侧自动留白 |

> **关键规则**：最大宽度限制是网格系统的隐性约束，超过后内容不再扩展。这是 **"受限响应式"（Constrained Responsive）**。

### 4.8 页面布局心理学指引

> 以下为布局设计的心理学依据摘要，详细论述见 `UI设计规范系统性研究报告.md` §4.8。

| 心理学原理 | 布局启示 |
|-----------|---------|
| 认知负荷理论 | 渐进式披露、分块（每组 4-7 项）、一致性降低外在负荷 |
| F 型阅读模式 | 核心信息放左上角和前两行；每行开头放关键词 |
| Z 型阅读模式 | Logo 左上，CTA 右上，核心视觉居中，次级 CTA 右下 |
| 席克定律 | 主导航项限制在 3-5 项，每屏仅 1 个主要 CTA |
| 费茨定律 | 移动端触摸目标 >= 44x44pt，高频操作靠近手指自然位置 |
| 冯·雷斯托夫效应 | 重要元素通过颜色/大小/位置与周围形成对比以突出 |

---

## 5. 组件规范与交互逻辑（Components & Interaction）

> 每个组件必须定义：**解剖结构（Anatomy）**、**所有状态（States）**、**交互行为（Behavior）**、**使用的 Token**、**Do & Don't**

### 5.1 组件状态机规范

每个交互组件必须定义完整的状态机，确保行为的确定性和可测试性。

**标准状态矩阵**：

| 状态 | 视觉表现 | 触发条件 | 退出条件 | 无障碍要求 |
|------|---------|---------|---------|-----------|
| **Default** | 基础样式 | 初始态 | 任何交互 | 可聚焦 |
| **Hover** | 背景叠加 5%（Light）/ 5%（Dark） | 鼠标进入 | 鼠标离开 | 仅桌面端 |
| **Pressed** | 背景叠加 10%（Light）/ 10%（Dark） | 按下 | 释放 | — |
| **Focus** | 2px 聚焦环 | Tab/点击 | Tab 移出/Escape | 必须可见，对比度 >= 3:1 |
| **Disabled** | 38% 透明度 | `disabled=true` | `disabled=false` | `aria-disabled="true"` |
| **Loading** | Spinner + 禁用交互 | `isLoading=true` | 请求完成/失败 | `aria-busy="true"` |
| **Error** | 红色边框 + 错误信息 | 验证失败 | 修正输入 | `aria-invalid="true"` |
| **Success** | 绿色边框/图标 | 操作成功 | 2s 后自动恢复 | `aria-live="polite"` |

**全局交互叠加层（Global Interaction Overlay）**：

所有组件的 hover/active 状态使用统一的透明度叠加，确保视觉一致性：

| 状态 | Light 模式 | Dark 模式 | CSS 实现 |
|------|-----------|----------|---------|
| **Hover** | `rgba(0,0,0,0.05)` | `rgba(255,255,255,0.05)` | `background-color: color-mix(in srgb, currentColor 5%, transparent)` |
| **Active** | `rgba(0,0,0,0.1)` | `rgba(255,255,255,0.1)` | `background-color: color-mix(in srgb, currentColor 10%, transparent)` |
| **Focus** | `2px solid var(--color-border-focus)` | 同左 | 轮廓线，非背景叠加 |

> **即时反馈规则**：Hover 响应延迟 0ms（无 `transition-delay`），Focus 环显示 0ms。仅位移/缩放类动画允许 150-200ms 过渡。

**状态转换规则**：
- Disabled 状态下仅允许 `Disabled → Default` 转换，禁止其他交互
- Loading 状态下禁止 Hover/Pressed 转换
- Error 状态必须提供具体错误信息，禁止仅显示"操作失败"
- 状态转换必须有对应的视觉反馈，无静默转换

### 5.2 按钮（Button）

#### 解剖结构（Anatomy）
```
[图标(可选)] + [文字标签] + [加载图标(可选)]
```
- 高度规范：`size.sm` = 32-36px（文字按钮），`size.md` = 40-44px（辅助按钮），`size.lg` = 48-52px（主按钮）
- 圆角：`radius.md` = 8px（移动端最常用），品牌调性决定，也可 4px/6px/999px
- 最小点击热区：>= 44 x 44px（触控设备强制要求）

**按钮尺寸规范**：

| 按钮类型 | 高度 | 圆角 | 用途 |
|---------|------|------|------|
| **主按钮（Primary）** | 48-52px | 8px | 页面核心 CTA，每页最多 1 个 |
| **辅助按钮（Secondary）** | 40-44px | 8px | 次级操作、取消 |
| **文字按钮（Text）** | 32-36px | 0-4px | 低优先级、工具栏 |

> **移动端按钮规范**：主按钮高度 48-52px，确保手指点击舒适；辅助按钮 40-44px，文字按钮 32-36px。所有按钮最小点击热区 >= 44x44px。

#### 类型变体（Type Variants）
| 类型 | 背景 Token | 文字 Token | 边框 Token | 使用场景 |
|------|-----------|-----------|-----------|----------|
| **Primary（实心）** | `color.brand-600` | `color.text.on-brand` | 无 | 页面主行动点，每页最多 1 个 |
| **Secondary（描边）**| 透明 | `color.brand-600` | `color.brand-600` | 次级操作、取消 |
| **Tertiary（幽灵）** | 透明 | `color.brand-600` | 无 | 低优先级、工具栏 |
| **Danger（危险）** | `color.semantic.error` | `color.text.on-danger` | 无 | 删除、不可逆操作 |
| **Text（纯文本）** | 透明 | `color.brand-600` | 无 | 链接、表格内操作 |

#### 交互状态（States）
所有按钮必须定义以下 7 种状态：

| 状态 | 视觉表现 | Token 变化 | 触发条件 |
|------|----------|-----------|----------|
| **Default** | 默认样式 | `color.brand-600` | 无交互 |
| **Hover** | 背景叠加 5%（使用全局叠加层） | `color.brand-500` | 鼠标悬停 |
| **Pressed / Active** | 背景叠加 10%（使用全局叠加层），Y轴向下偏移 1px | `color.brand-700` | 鼠标按下/触控按下 |
| **Focus** | 外框 2px 聚焦环（Focus Ring），offset 2px | `color.border.focus` | 键盘 Tab 聚焦 |
| **Disabled** | 背景变浅灰，文字变 `text.disabled`，无 Hover 效果 | `color.background.disabled` | 不可点击时 |
| **Loading** | 背景保持，文字隐藏，显示 Spinner（不响应点击）| — | 异步请求中 |
| **Success** | 短暂变为绿色背景 + 对勾图标，1.5s 后恢复或跳转 | `color.semantic.success` | 操作成功反馈 |

#### 交互细节（Interaction Details）
- **Hover 延迟**：无延迟，即时响应（0ms）
- **Pressed 反馈**：提供 `transform: translateY(1px)` 物理按压感
- **Focus 可见性**：必须满足 3:1 对比度，禁止隐藏 outline
- **Loading 状态**：按钮宽度不变，防止布局抖动；Spinner 尺寸 = 文字高度 x 0.8
- **防抖**：连续点击时，仅首次触发，直至状态变更

---

### 5.3 输入框（Input / TextField）

#### 状态定义
| 状态 | 边框 | 背景 | 提示文字 |
|------|------|------|----------|
| **Default** | `color.border.default` | `color.background.surface` | `color.text.placeholder` |
| **Hover** | `color.border.hover`（加深） | 不变 | 不变 |
| **Focus** | `color.brand-600`（2px，品牌色） | `color.background.default` | 不变 |
| **Filled** | `color.border.default` | 不变 | 上移/缩小作为 Label（Floating Label 模式） |
| **Error** | `color.semantic.error` | `color.semantic.error.subtle` | 显示错误图标 + 错误文案 |
| **Disabled**| `color.border.disabled` | `color.background.disabled` | `color.text.disabled` |
| **Read-only** | 虚线边框 `border-dashed` | 不变 | 不变 |

#### 交互逻辑
- **Focus 动效**：边框颜色过渡 `transition: border-color 200ms ease-out`
- **错误态**：失去焦点（Blur）时触发校验；错误文案出现在输入框下方，字号 `font.body.small`，颜色 `color.semantic.error`
- **清除按钮**：Hover 输入框时，右侧显示清除图标（仅限有内容且非 Disabled 状态）
- **密码可见性切换**：点击眼睛图标切换 `type="password/text"`，图标颜色在 Active 时变为 `color.brand-600`

---

### 5.4 卡片（Card）

#### 分层与阴影
| 层级 | 背景 Token | 阴影 Token | 用途 |
|------|-----------|-----------|------|
| **Rest** | `color.background.surface` | `shadow.sm`（`0 1px 2px rgba(0,0,0,0.05)`）| 默认展示 |
| **Hover** | 不变 | `shadow.md`（`0 4px 12px rgba(0,0,0,0.1)`）| 可点击卡片悬停 |
| **Pressed**| 不变 | `shadow.sm` + 向下位移 1px | 按下 |
| **Selected** | `color.background.selected` | `shadow.md` + 边框 `color.brand-600` | 选中态 |

#### 交互逻辑
- **Hover 抬升**：阴影加深 + 轻微放大 `scale(1.01)`，过渡 200ms ease-out
- **点击区域**：整张卡片为点击热区时，必须包含清晰的焦点环（Focus Ring）
- **内部操作**：若卡片内有独立按钮（如"编辑"），需使用 `z-index` 确保事件不冒泡

---

### 5.5 导航（Navigation）

#### 顶部导航（Top Nav）
- **高度**：56px / 64px（桌面端）
- **背景**：`color.background.surface`（Light）或 `color.neutral-100`（Dark）
- **Logo 区域**：左侧，宽度 `space.16`（64px）
- **菜单项**：
  - Default：`color.text.secondary`
  - Hover：`color.text.primary` + 底部 2px 指示条（`color.brand-600`）
  - Active/Selected：`color.text.primary` + 指示条常驻
  - Focus：外框聚焦环
- **导航项数量**：限制在 3-5 项（席克定律甜蜜点）

#### 侧边导航（Side Nav）
- **宽度**：200px（展开）/ 64px（收起）
- **背景**：`color.background.surface`（比页面底色深一层，遵循 Layering Model）
- **选中项**：背景 `color.background.selected`，文字 `color.text.primary`，左侧 3px 竖条 `color.brand-600`
- **Hover**：背景 `color.background.hover`，无左侧竖条
- **折叠动画**：宽度变化 `transition: width 250ms cubic-bezier(0.4, 0, 0.2, 1)`

---

### 5.6 反馈组件（Feedback）

#### Toast / Notification
| 类型 | 背景 | 左侧竖条/图标 | 停留时间 |
|------|------|--------------|----------|
| **Info** | `color.background.surface` | `color.semantic.info` | 3s |
| **Success** | `color.background.surface` | `color.semantic.success` | 3s |
| **Warning** | `color.background.surface` | `color.semantic.warning` | 5s（需用户注意） |
| **Error** | `color.background.surface` | `color.semantic.error` | 不自动消失（需手动关闭） |

#### 交互逻辑
- **入场**：从右侧滑入（`translateX(100%) → 0`），300ms，`cubic-bezier(0.4, 0, 0.2, 1)`
- **出场**：向上淡出（`translateY(-10px) + opacity 0`），200ms
- **悬停暂停**：鼠标悬停时，倒计时暂停；移出后继续
- **堆叠**：最多显示 3 条，新 Toast 向上推移旧 Toast，间距 `space.3`

---

## 6. 图标系统（Iconography）

### 6.1 图标规范

| 规范项 | 标准 | 说明 |
|--------|------|------|
| 图标风格 | [线性（Outline）/ 填充（Filled）] | 同一功能图标提供 Outline + Filled 两种变体 |
| 默认尺寸 | 24px | 图标网格 24dp bounding box |
| 描边宽度 | 2dp | Material Design 标准 |
| 命名规则 | `{category}-{name}-{variant}` | 如 `nav-arrow-left-filled` |
| 实现方式 | SVG sprite 优于 icon font | 性能/可访问性/可维护性 |

### 6.2 图标尺寸 Token

| Token | 值 | 用途 |
|-------|-----|------|
| `icon.size.xs` | 12px | 紧凑内联图标 |
| `icon.size.sm` | 16px | 表格内图标、辅助图标 |
| `icon.size.md` | 20px | 按钮内图标 |
| `icon.size.lg` | 24px | 默认图标（导航栏、列表） |
| `icon.size.xl` | 32px | 空状态图标 |
| `icon.size.2xl` | 48px | 引导页图标 |
| `icon.size.3xl` | 64px | 大尺寸展示图标 |

> **移动端图标规范**：常用尺寸 16/20/24/32/48/64px，可根据实际场景在导航栏、列表、按钮与提示等位置灵活使用。

### 6.3 绘制栅格

- 图标绘制前应先确定栅格与安全区域
- 推荐使用外框、中心线与圆形基准辅助绘制
- 保持图形比例与视觉平衡，减少重心偏移
- 确保在不同尺寸下依然清晰稳定

### 6.3 Live Area 与 Trim Area

| 画布尺寸 | Live Area | Trim Area | 说明 |
|---------|-----------|-----------|------|
| 16x16px | 14x14px | 1px | 高密度图标 |
| 20x20px | 16x16px | 2px | Font Awesome 7 |
| 24x24px | 20x20px | 2px | Material Design |
| 32x32px | 28x28px | 2px | IBM |

- **Live Area** 是图标内容的实际绘制区域
- **Trim Area** 是安全边距，防止图标被裁剪
- 所有图标元素必须 **对齐到像素网格**（使用整数坐标）

### 6.4 currentColor 策略

图标应使用 `currentColor` 或语义 Token 填充，而非硬编码颜色：

```css
.icon {
  fill: var(--icon-color-primary, currentColor);
}
```

### 6.5 图标无障碍

- 装饰图标：`aria-hidden="true"`
- 功能图标：需 `aria-label` 描述功能
- 图标按钮最小尺寸：24x24px（WCAG 2.2 AA），推荐 32x32px

---

## 7. 阴影与层级系统（Elevation）

### 7.1 Elevation 层级

| Elevation 层级 | 阴影值 | 用途 |
|----------------|--------|------|
| 0dp | 无阴影 | 页面底色、平面内容 |
| 1dp | `0 1px 2px rgba(0,0,0,0.1)` | 卡片（默认态） |
| 3dp | `0 2px 4px rgba(0,0,0,0.1)` | 卡片（悬浮态）、输入框 |
| 8dp | `0 4px 8px rgba(0,0,0,0.12)` | 弹出菜单、下拉框 |
| 12dp | `0 6px 12px rgba(0,0,0,0.15)` | 浮动按钮 |
| 24dp | `0 12px 24px rgba(0,0,0,0.2)` | 模态框、对话框 |

### 7.2 Shadow + Surface 双重表达

Shadow 和 Surface 必须成对使用，不能混用不同层级的 Shadow 和 Surface：

| Elevation 层级 | Surface Token | Shadow Token | 用途 |
|-------------|--------------|-------------|------|
| **Sunken** | `elevation.surface.sunken` | 无 | 最低层，如 Kanban 列背景 |
| **Default** | `elevation.surface` | 无 | 基准层，如页面内容 |
| **Raised** | `elevation.surface.raised` | `elevation.shadow.raised` | 可移动卡片 |
| **Overlay** | `elevation.surface.overlay` | `elevation.shadow.overlay` | 模态框、下拉菜单 |

> **暗色模式**：Shadow 几乎不可见，因此 **Surface 颜色必须随层级变亮** 来补偿。

### 7.3 Z-index Token 体系

| Token | 值 | 用途 |
|-------|-----|------|
| `--z-base` | 0 | 默认内容 |
| `--z-dropdown` | 100 | 下拉菜单 |
| `--z-sticky` | 200 | 粘性头部 |
| `--z-overlay` | 300 | 遮罩层 |
| `--z-modal` | 400 | 模态框 |
| `--z-toast` | 500 | Toast 通知 |

> **关键规则**：z-index 值应跳跃式递增（每次至少 +50 或 +100），为中间层级预留空间。

---

## 8. 形状与圆角系统（Shape）

### 8.1 圆角 Token

| Token | 值 | 用途 |
|-------|-----|------|
| `--radius-none` | 0 | 表格、分割容器、强秩序信息区 |
| `--radius-xs` | 2px | 小型元素 |
| `--radius-sm` | 4px | 输入框、标签、轻量按钮等细小组件 |
| `--radius-md` | 8px | 按钮、卡片、小弹层（**移动端最常用**） |
| `--radius-lg` | 12px | 内容卡片、浮层面板、信息模块容器 |
| `--radius-xl` | 16px | 大卡片、底部弹窗、强调型展示区域 |
| `--radius-full` | 9999px | 圆形头像、胶囊按钮 |
| `--radius-pill` | 9999px | 胶囊按钮（`--radius-full` 别名） |

> **移动端圆角规范**：8px 是移动端最常用圆角值，适用于按钮、卡片、小弹层。12px 用于内容卡片和浮层面板，16px 用于大卡片和底部弹窗。

### 8.2 嵌套圆角黄金公式

`Inner Radius = Outer Radius - Padding`

```css
.parent {
  --radius: 24px;
  --padding: 12px;
  border-radius: var(--radius);
  padding: var(--padding);
}

.child {
  border-radius: calc(var(--radius) - var(--padding)); /* = 12px */
}
```

> **关键规则**：如果计算结果为负数，子元素应保持自身的圆角 Token，不强行套用公式。

---

## 9. 微交互与动效规范（Motion & Micro-interactions）

### 9.1 缓动曲线（Easing）

#### Productive vs Expressive 双轨制

| 场景 | Productive Easing（功能性） | Expressive Easing（情感性） |
|------|--------------------------|---------------------------|
| Standard | `cubic-bezier(0.2, 0, 0.38, 0.9)` | `cubic-bezier(0.4, 0.14, 0.3, 1)` |
| Entrance | `cubic-bezier(0, 0, 0.38, 0.9)` | `cubic-bezier(0, 0, 0.3, 1)` |
| Exit | `cubic-bezier(0.2, 0, 1, 0.9)` | `cubic-bezier(0.4, 0.14, 1, 1)` |

- **Productive** 用于功能性动画（快速、直接、不分散注意力）
- **Expressive** 用于情感性动画（流畅、有品牌个性）
- 同一组件的"进入"和"退出"应使用不同的 Easing：进入用 Expressive，退出用 Productive

### 9.2 时长规范（Duration）

| Token | 值 | 用途 |
|-------|-----|------|
| `duration.fast-01` | 70ms | 微交互（按钮、开关） |
| `duration.fast-02` | 110ms | 微交互（淡入淡出） |
| `duration.moderate-01` | 150ms | 小展开、短距离移动 |
| `duration.moderate-02` | 240ms | 展开、系统通知、Toast |
| `duration.slow-01` | 400ms | 大展开、重要系统通知 |
| `duration.slow-02` | 700ms | 背景变暗 |

### 9.3 Duration Scalar 全局调速机制

所有 Duration Token 必须乘以 `duration-scalar`，这是实现 `prefers-reduced-motion` 的唯一正确方式：

```css
:root {
  --duration-scalar: 1; /* 正常速度 */
}

@media (prefers-reduced-motion: reduce) {
  :root {
    --duration-scalar: 0; /* 完全禁用 */
  }
}
```

> 手动设置固定时长而不使用 scalar 的组件，将无法响应用户的减少动画偏好。

### 9.4 响应时间阈值

| 阈值 | 用户感知 | 设计策略 |
|------|---------|---------|
| < 100ms | 即时 | 无需等待指示 |
| 100-300ms | 流畅 | 微动画反馈 |
| 300ms-1s | 可接受延迟 | Spinner / 进度指示 |
| 1-5s | 明显等待 | 骨架屏 + 进度条 |
| > 5s | 长时间等待 | 百分比进度 + 预估时间 |

### 9.5 骨架屏 vs Spinner 决策树

| 等待时间 | 策略 |
|---------|------|
| 0-300ms | 无等待指示 |
| 300ms-1s | 按钮内 Spinner / 微型进度指示 |
| 1s-5s | 骨架屏 + 顶部进度条 |
| > 5s | 骨架屏 + 百分比进度 + 预估时间 |

### 9.6 触觉反馈标准（移动端）

| 场景 | 时长 | 类型 |
|------|------|------|
| 按钮确认 | 10-15ms | Impact Light |
| 选择变化 | 5-10ms | Selection |
| 长按触发 | 15-20ms | Impact Medium |
| 成功通知 | 50-100ms | Notification Success |
| 错误通知 | 100-200ms | Notification Error |

### 9.7 常见动效模式

| 模式 | 规则 | 示例 |
|------|------|------|
| **Fade** | Opacity 0 → 1，配合 Enter/Exit 缓动 | Toast 入场、Tooltip |
| **Slide** | TranslateY/X ±8-16px | 下拉菜单、抽屉展开 |
| **Scale** | Scale 0.95 → 1.0，配合 Fade | 模态框弹出、菜单 |
| **Ripple** | 点击位置水波纹扩散，主色 20% 透明度 | Material 风格按钮（可选） |

### 9.8 动画参数补充

| 属性 | 推荐值 | 说明 |
|------|-------|------|
| 位移距离 | 4-8px | 轻微移动反馈 |
| 缩放比例 | 0.95-1.05 | 按压/释放效果 |
| 弹性动画 | Spring（damping: 0.7-0.9） | 下拉刷新、拖拽释放 |
| 性能约束 | 仅对 `transform` 和 `opacity` 做动画 | 避免 layout thrashing |

---

## 10. 可访问性规范（Accessibility）

### 10.1 对比度标准

- **正文文字（< 18px 或非粗体）**：与背景对比度 >= 4.5:1（WCAG AA）
- **大文字（>= 18px 或粗体 >= 14px）**：与背景对比度 >= 3:1
- **UI 组件/图标**：与相邻颜色对比度 >= 3:1
- **Focus 环**：与背景对比度 >= 3:1，厚度 >= 2px

### 10.2 双重编码原则（强制要求）

所有状态变化必须至少使用 **两种编码方式**（颜色+图标、颜色+文本、颜色+形状）。这是 **Level A 合规的强制要求**，不是可选最佳实践。

| 场景 | 错误做法 | 正确做法 |
|------|---------|---------|
| 错误状态 | 仅红色边框 | 红色边框 + 错误图标 + 错误文本 |
| 成功状态 | 仅绿色背景 | 绿色背景 + 勾选图标 + 成功文本 |
| 禁用状态 | 仅灰色 | 灰色 + 降低透明度 + 禁用光标 |
| 链接 | 仅蓝色 | 蓝色 + 下划线 + 悬停状态 |

### 10.3 焦点管理（Focus Management）

- 所有可交互元素必须有可见的焦点指示器（Focus Indicator）
- 焦点环样式：`2px solid color.brand-600`（Light）/ `color.brand-400`（Dark），`offset: 2px`，圆角跟随组件
- **禁止**：仅使用颜色变化表示焦点，必须配合轮廓线
- 在深色背景上，默认 Focus 颜色可能不可见，需要切换到白色 Focus
- 模态框打开时焦点陷阱（focus trap），关闭后焦点返回触发元素

### 10.4 Halation 效应处理

散光用户在深色背景上阅读白色文字时，文字会出现"光晕"，使文字看起来更粗、更模糊。解决方案：

- 使用 **非纯白的文字色**（`#E0E0E0` 而非 `#FFFFFF`）
- 增加 **字重**（从 400 增加到 500）
- 增加 **行高**（从 1.5 增加到 1.6-1.7）

### 10.5 键盘导航

- 所有交互元素可通过 Tab / Enter / Space / Esc 操作
- 动态内容使用 `aria-live="polite"` 或 `"assertive"`
- 自定义组件使用 `role` + `aria-*` 标注
- 所有图像有 `alt`，图标有 `aria-label`，表单有 `<label>`

### 10.6 减少动画偏好

- 适配 `prefers-reduced-motion: reduce` 媒体查询
- 通过 Duration Scalar 机制实现（见 §9.3）
- 高对比度模式适配 `prefers-contrast: more` 媒体查询

### 10.7 触控目标（Touch Target）

| 平台 | 最小触控区域 | 相邻间距 |
|------|------------|---------|
| iOS | 44 x 44pt | >= 8px |
| Android | 48 x 48dp | >= 8px |
| Web（移动端） | 44 x 44px | >= 8px |
| Web（桌面端） | 24-32px | >= 4px |

### 10.8 文字缩放

- 支持 200% 文字缩放不丢失内容（WCAG 2.1 SC 1.4.4）
- 测试 Dynamic Type 最大字号下的布局是否仍然可用

---

## 11. 跨平台适配规范（Cross-Platform）

### 11.1 跨平台策略

推荐 **"品牌一致 + 交互原生"** 的混合策略：

1. **品牌层一致**：色彩、字体、图标风格、间距比例跨平台统一
2. **交互层原生**：导航范式、手势操作、弹窗形式、返回逻辑遵循各平台规范
3. **组件层适配**：同一组件在不同平台保持视觉一致但交互方式适配平台

### 11.2 设计稿基准尺寸

| 平台 | 画板宽度 | 说明 |
|------|---------|------|
| **iOS** | 375px（iPhone 标准） | @1x 基准，@2x/@3x 适配 |
| **Android** | 360px（主流机型） | mdpi 基准，xxxhdpi 适配 |
| **Web** | 1440px（桌面端） | 响应式基准，向下适配移动端 |

> **核心原则**：一套稿适配多端，优先保证布局适配能力。iOS 和 Android 画板宽度差异仅 15px，通过流式布局（Flex/Grid）自动适配。

**固定组件高度规范**：

| 组件 | iOS 高度 | Android 高度 | 说明 |
|------|---------|-------------|------|
| 状态栏 | 44pt | 24dp | 顶部系统状态栏 |
| 导航栏 | 44pt | 56dp | 页面导航标题栏 |
| 底部 Tab 栏 | 50pt | 56dp | 底部标签导航 |
| 底部安全区域 | 34pt | 48dp | Home Indicator / 手势导航区 |

### 11.3 移动端 vs 桌面端尺寸规范

| 维度 | 移动端 | 桌面端 | 说明 |
|------|-------|--------|------|
| 最小触摸目标 | 44-48px | 24-32px | 鼠标精度高于手指 |
| 元素间距 | 8-16px | 4-8px | 移动端需防误触 |
| 按钮高度 | 48-56px | 32-40px | 移动端需更大触控区 |
| 输入框高度 | 48-56px | 36-44px | 移动端需更大点击区 |
| 列表项高度 | 56-72px | 40-48px | 移动端需更大行高 |
| 导航深度 | 3 层以内 | 多层嵌套 | 移动端认知负荷限制 |
| 内容展示 | 单列、垂直滚动 | 多列、网格、侧边栏 | 屏幕空间差异 |
| 操作暴露 | 隐藏（菜单、更多） | 直接暴露（工具栏） | 空间约束差异 |
| 表单设计 | 分步、单页少字段 | 长表单、多列布局 | 移动端输入成本高 |
| 模态使用 | 全屏模态为主 | 居中弹窗、侧边抽屉 | 屏幕空间差异 |

### 11.4 交互差异

| 维度 | iOS | Android | Web |
|------|-----|---------|-----|
| Hover 状态 | 无（触控设备） | 无（触控设备） | 有（鼠标悬停） |
| 按压反馈 | 高亮减淡 70% | Ripple 水波纹 | 背景加深 + Y偏移 |
| 触觉反馈 | Taptic Engine | HapticFeedback | Vibration API（有限） |
| 返回手势 | 边缘右滑（全系统） | 预测性返回（Android 14+） | 浏览器后退（无手势） |
| 长按反馈 | 上下文菜单 + 触觉 | 上下文菜单 + Ripple | 右键菜单（无触觉） |

> **关键规则**：触摸设备没有 Hover 状态，因此 **所有功能不能依赖 Hover 暴露**。DS 必须为每种输入模式提供 **等效的操作路径**。

### 11.5 安全区域约束

| 平台 | 顶部安全区 | 底部安全区 | 侧边安全区 |
|------|-----------|-----------|-----------|
| iOS (刘海屏) | 44pt | 34pt (Home Indicator) | 0pt |
| iOS (灵动岛) | 59pt | 34pt | 0pt |
| Android (全面屏) | 24dp | 48dp (手势导航) | 0dp |
| Android (三键导航) | 24dp | 0dp | 0dp |

> 底部固定按钮必须位于 **安全区之上**。Web 端的 `env(safe-area-inset-*)` CSS 变量可以自动处理。

### 11.6 密度 Token 化控制

| 密度模式 | 移动端 | 桌面端 | 适用场景 |
|---------|-------|--------|---------|
| **Compact** | 不推荐 | 数据密集型后台 | 键鼠设备推荐 |
| **Default** | 推荐 | 通用场景 | 通用推荐 |
| **Comfortable** | 阅读类应用 | 展示类页面 | 触控设备推荐 |

> 密度变化影响 **间距、字体大小、组件尺寸** 三个维度，不能只改间距。

---

## 12. Brand Token Mapping

> 本章节为项目强制要求，定义品牌色系到 Design Token 的映射关系。采用单品牌色策略。

### 12.1 品牌色系定义

| 品牌色 | Hex 值 | 语义 | 使用场景 |
|--------|--------|------|---------|
| [品牌主色名] | [Hex] | 品牌识别、行动召唤 | 主按钮、Logo、导航激活态、链接、图标强调 |

> **单品牌色约束**：仅定义 1 个品牌色，辅助强调从语义色板和中性色板获取。品牌色覆盖面积 <= 10%。

### 12.2 品牌色梯度扩展

> 为品牌色定义 9 级梯度（50-900），以 600 色阶为基准色。

#### [品牌主色名]梯度

| 梯度 | Hex 值 | 用途 |
|------|--------|------|
| `[主色]-50` | [Hex] | 极浅背景、hover 底色 |
| `[主色]-100` | [Hex] | 轻量背景、选中态底色 |
| `[主色]-200` | [Hex] | 浅色装饰元素 |
| `[主色]-300` | [Hex] | 次要图标、辅助文字 |
| `[主色]-400` | [Hex] | 中等强调 |
| `[主色]-500` | [Hex] | Hover 状态、图表辅助色 |
| `[主色]-600` | [Hex] | **基准色（默认）** |
| `[主色]-700` | [Hex] | Pressed/Active 状态 |
| `[主色]-800` | [Hex] | 深色文字（on-light） |
| `[主色]-900` | [Hex] | 极深装饰、深色背景强调 |

### 12.3 CSS 变量映射

品牌 Token（`--sin-s-*`）映射到组件 Token（`--sin-c-{module}-*`）：

```css
:root {
  /* ===== Brand Tokens (Semantic Layer) ===== */
  --sin-s-brand: [主色 Hex];
  --sin-s-brand-hover: [主色-500 Hex];
  --sin-s-brand-pressed: [主色-700 Hex];
  --sin-s-brand-subtle: [主色-50 Hex];
  --sin-s-brand-contrast: [主色-800 Hex];

  /* ===== Component Tokens (Component Layer) ===== */
  /* --sin-c-{module}-* naming convention */

  /* Button */
  --sin-c-btn-primary-bg: var(--sin-s-brand);
  --sin-c-btn-primary-bg-hover: var(--sin-s-brand-hover);
  --sin-c-btn-primary-bg-pressed: var(--sin-s-brand-pressed);
  --sin-c-btn-primary-text: [on-brand Hex];
  --sin-c-btn-secondary-bg: transparent;
  --sin-c-btn-secondary-border: var(--sin-s-brand);
  --sin-c-btn-secondary-text: var(--sin-s-brand);
  --sin-c-btn-danger-bg: var(--sin-s-semantic-error);
  --sin-c-btn-danger-text: [on-danger Hex];

  /* Navigation */
  --sin-c-nav-active-indicator: var(--sin-s-brand);
  --sin-c-nav-bg: var(--sin-s-brand-subtle);

  /* Input */
  --sin-c-input-border-focus: var(--sin-s-brand);

  /* Card */
  --sin-c-card-bg: [Hex];
  --sin-c-card-bg-surface: var(--sin-s-brand-subtle);

  /* Text */
  --sin-c-text-primary: [Hex];
  --sin-c-text-secondary: [Hex];
  --sin-c-text-on-brand: [on-brand Hex];
  --sin-c-text-link: var(--sin-s-brand);

  /* Border */
  --sin-c-border-default: [Hex];
  --sin-c-border-focus: var(--sin-s-brand);

  /* Background */
  --sin-c-bg-default: [Hex];
  --sin-c-bg-surface: var(--sin-s-brand-subtle);
  --sin-c-bg-page: var(--sin-s-brand-subtle);

  /* Shadow */
  --sin-c-shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
  --sin-c-shadow-md: 0 4px 12px rgba(0,0,0,0.1);

  /* Spacing */
  --sin-c-space-1: 4px;
  --sin-c-space-2: 8px;
  --sin-c-space-4: 16px;
  --sin-c-space-6: 24px;

  /* Radius */
  --sin-c-radius-sm: 4px;
  --sin-c-radius-md: 8px;
  --sin-c-radius-full: 9999px;
  --sin-c-radius-pill: var(--sin-c-radius-full);
}

[data-theme="dark"] {
  --sin-s-brand: [主色 Dark Hex];
  --sin-s-brand-hover: [主色-400 Dark Hex];
  --sin-s-brand-pressed: [主色-600 Dark Hex];
  --sin-s-brand-subtle: [主色-900 Dark Hex];
  --sin-s-brand-contrast: [主色-200 Dark Hex];

  --sin-c-text-primary: [Hex];
  --sin-c-bg-default: [Hex];
  --sin-c-bg-surface: [Hex];
  --sin-c-bg-page: [Hex];
  --sin-c-border-default: [Hex];
  --sin-c-border-focus: var(--sin-s-brand);
  /* ... 其余 Token 覆盖 */
}

/* 暗色模式自动检测：跟随系统偏好 */
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --sin-s-brand: [主色 Dark Hex];
    --sin-s-brand-hover: [主色-400 Dark Hex];
    --sin-s-brand-pressed: [主色-600 Dark Hex];
    --sin-s-brand-subtle: [主色-900 Dark Hex];
    --sin-s-brand-contrast: [主色-200 Dark Hex];

    --sin-c-text-primary: [Hex];
    --sin-c-bg-default: [Hex];
    --sin-c-bg-surface: [Hex];
    --sin-c-bg-page: [Hex];
    --sin-c-border-default: [Hex];
    --sin-c-border-focus: var(--sin-s-brand);
    /* ... 其余 Token 覆盖 */
  }
}
```

---

## 13. 视觉范例：Do & Don't

### 13.1 颜色使用

| Do | Don't |
|----|-------|
| 主按钮每页仅出现 1 个，用于最核心的 CTA | 同一页面出现 3 个以上实心品牌色按钮 |
| 错误文字配合错误图标 + 错误文本使用（双重编码） | 仅用红色文字表示错误，无其他提示 |
| 在深色背景上使用 `color.text.inverse`（非纯白，避免 Halation） | 在深色背景上继续使用深色文字或纯白 `#FFFFFF` |
| 遵循 Layering Model，卡片使用 Surface 色 | 在白色背景上叠纯白卡片，无层级区分 |
| 品牌色仅用于可交互元素（按钮、链接、图标） | 品牌色用于大面积背景或非交互装饰 |
| 品牌色覆盖面积 <= 10% | 品牌色覆盖面积 > 10% 导致视觉过重 |
| 以 600 色阶为基准色 | 以 400 或 500 作为基准色（对比度不足） |

### 13.2 交互设计

| Do | Don't |
|-------|----------|
| 按钮 Disabled 时提供 Tooltip 解释原因 | Disabled 按钮无任何提示，用户困惑 |
| 表单错误在失去焦点时即时反馈 | 提交时才一次性暴露所有错误 |
| 异步操作提供 Loading / Skeleton 状态 | 按钮点击后无反馈，用户不确定是否生效 |
| 破坏性操作二次确认（弹窗/二次点击）| 删除按钮直接执行，无确认 |
| Focus 环使用轮廓线 + 对比度 >= 3:1 | 仅用颜色变化表示焦点 |
| 所有状态变化使用双重编码（颜色+图标/文本） | 仅用颜色传达状态信息 |

### 13.3 跨平台设计

| Do | Don't |
|-------|----------|
| 品牌层一致 + 交互层原生 | 所有平台完全一致的交互方式 |
| 移动端触摸目标 >= 44px | 桌面端尺寸直接用于移动端 |
| 功能不依赖 Hover 暴露 | 关键操作仅在 Hover 态显示 |
| 底部按钮位于安全区之上 | 内容紧贴屏幕边缘 |

---

## 14. 附录

### 14.1 Token 代码参考（CSS Variables）

```css
:root {
  /* Brand (Primitive Layer) */
  --[主色名]-50: [Hex];
  --[主色名]-100: [Hex];
  --[主色名]-200: [Hex];
  --[主色名]-300: [Hex];
  --[主色名]-400: [Hex];
  --[主色名]-500: [Hex];
  --[主色名]-600: [Hex];
  --[主色名]-700: [Hex];
  --[主色名]-800: [Hex];
  --[主色名]-900: [Hex];

  /* Semantic - Brand (Single Brand Color) */
  --color-brand: var(--[主色名]-600);
  --color-brand-hovered: var(--[主色名]-500);
  --color-brand-pressed: var(--[主色名]-700);
  --color-brand-subtle: var(--[主色名]-50);
  --color-brand-contrast: var(--[主色名]-800);

  /* Semantic - Functional */
  --color-semantic-success: [Hex];
  --color-semantic-warning: [Hex];
  --color-semantic-error: [Hex];
  --color-semantic-info: var(--color-brand);

  /* Semantic - Neutral */
  --color-neutral-50: [Hex];
  --color-neutral-100: [Hex];
  --color-neutral-900: [Hex];

  /* Semantic - Text */
  --color-text-primary: [Hex];
  --color-text-secondary: [Hex];
  --color-text-disabled: [Hex];
  --color-text-inverse: [Hex];
  --color-text-on-brand: [Hex];

  /* Semantic - Background */
  --color-background-default: [Hex];
  --color-background-surface: [Hex];

  /* Semantic - Border */
  --color-border-default: [Hex];
  --color-border-focus: var(--color-brand);

  /* Elevation */
  --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
  --shadow-md: 0 4px 12px rgba(0,0,0,0.1);

  /* Spacing */
  --space-1: 4px;
  --space-2: 8px;
  --space-4: 16px;
  --space-6: 24px;

  /* Radius */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-full: 9999px;
  --radius-pill: var(--radius-full);

  /* Z-index */
  --z-base: 0;
  --z-dropdown: 100;
  --z-sticky: 200;
  --z-overlay: 300;
  --z-modal: 400;
  --z-toast: 500;

  /* Motion */
  --duration-fast-01: 70ms;
  --duration-fast-02: 110ms;
  --duration-moderate-01: 150ms;
  --duration-moderate-02: 240ms;
  --duration-slow-01: 400ms;
  --duration-slow-02: 700ms;
  --duration-scalar: 1;

  --easing-productive: cubic-bezier(0.2, 0, 0.38, 0.9);
  --easing-expressive: cubic-bezier(0.4, 0.14, 0.3, 1);
  --easing-enter: cubic-bezier(0, 0, 0.2, 1);
  --easing-exit: cubic-bezier(0.4, 0, 1, 1);
}

[data-theme="dark"] {
  --color-brand: var(--[主色名]-400);
  --color-brand-hovered: var(--[主色名]-300);
  --color-brand-pressed: var(--[主色名]-500);
  --color-brand-subtle: var(--[主色名]-900);
  --color-brand-contrast: var(--[主色名]-200);

  --color-text-primary: [Hex];
  --color-text-secondary: [Hex];
  --color-background-default: [Hex];
  --color-background-surface: [Hex];
  --color-border-default: [Hex];
  --color-border-focus: var(--color-brand);
  /* ... 其余 Token 覆盖 */
}

/* 暗色模式自动检测：跟随系统偏好 */
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --color-brand: var(--[主色名]-400);
    --color-brand-hovered: var(--[主色名]-300);
    --color-brand-pressed: var(--[主色名]-500);
    --color-brand-subtle: var(--[主色名]-900);
    --color-brand-contrast: var(--[主色名]-200);

    --color-text-primary: [Hex];
    --color-text-secondary: [Hex];
    --color-background-default: [Hex];
    --color-background-surface: [Hex];
    --color-border-default: [Hex];
    --color-border-focus: var(--color-brand);
    /* ... 其余 Token 覆盖 */
  }
}

@media (prefers-reduced-motion: reduce) {
  :root {
    --duration-scalar: 0;
  }
}
```

### 14.2 参考资源

- [Material Design 3 - Color](https://m3.material.io/styles/color/roles)
- [IBM Carbon - Color System](https://carbondesignsystem.com/elements/color/overview/)
- [Microsoft Fluent 2 - Color](https://fluent2.microsoft.design/color)
- [Atlassian Design Tokens](https://atlassian.design/tokens/design-tokens)
- [W3C DTCG Specification](https://design-tokens.github.io/community-group/format/)
- [WCAG 2.1 对比度指南](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html)
- [APCA 对比度算法](https://github.com/Myndex/apca-w3)
- [W3C 中文排版需求 (clreq)](https://www.w3.org/TR/clreq/)
- [Style Dictionary v4](https://amzn.github.io/style-dictionary/)
