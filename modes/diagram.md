# Mode 4: Diagram (Excalidraw 可视化论证)

生成 `.excalidraw` JSON 文件，做出**视觉论证**，而非仅仅展示信息。输出 `.excalidraw` 源文件 + 渲染后的 `.png` 预览。

## 核心理念

**图表应该 ARGUE（论证），不是 DISPLAY（陈列）。** 图不是格式化的文本，而是用结构表达关系、因果和流动——形状本身就是含义。

- **同构测试**：如果去掉所有文字，仅凭结构能否传达概念？不能就重设计。
- **教育测试**：别人能从图中具体学到东西，还是只是给盒子贴标签？

## 速查表

| 你想画什么 | 推荐内容 | 推荐模式 |
| ---------- | -------- | -------- |
| 简单流程/概念 | Depth Assessment + Design Process + Pattern Library | Assembly Line / Fan-out |
| 技术架构图 | Research Mandate + Large Diagram Strategy + Evidence Artifacts | Multi-Zoom (3 levels) |
| 层级/组织结构 | Pattern Library (Tree) + Shape Meaning | Tree (lines + text) |
| 对比/前后对比 | Pattern Library (Side-by-Side) | Side-by-Side |
| 循环/迭代流程 | Pattern Library (Spiral/Cycle) | Cycle |

## 深度评估（先做这个）

- **简单/概念图**：抽象形状 + 标签，适合心智模型、哲学概念（概念本身就是抽象）。
- **综合/技术图**：具体例子 + 代码片段 + 真实数据，适合真实系统、协议、架构、教学。

**技术图必须先做 Research Mandate**：查阅真实规范、JSON 格式、事件名/方法名/API 端点，用真实术语而非占位符。差："Protocol" → "Frontend"；好："AG-UI streams events (RUN_STARTED, STATE_DELTA)" → "CopilotKit renders via createA2UIMessageRenderer()"。

## 设计流程（生成 JSON 前必做）

| 步骤 | 内容 | 完成标准 |
| ---- | ---- | ------- |
| Step 0 | 评估深度（简单/综合），综合图先做研究 | 深度确定，**CP1** 用户确认 |
| Step 1 | 深度理解：每个概念 DO 什么（不是 IS 什么）、关系、核心转换 | 所有概念识别出 DO-行为 |
| Step 2 | 概念映射到视觉模式（见下表） | 每个概念有匹配的视觉模式 |
| Step 3 | 确保多样性：每个主要概念用不同视觉模式 | 无两个主要概念共用同一模式 |
| Step 4 | 构思视觉流动（眼睛怎么扫过图） | **CP2** 用户确认视觉计划 |
| Step 5 | 生成 JSON（大图分段，见下） | 合法 JSON（能 `jq .`） |
| Step 6 | 渲染验证（render-view-fix 循环） | 渲染 PNG 通过缺陷检查，**CP4** 用户接受 |

## 用户检查点（强制暂停）

| CP | 在哪步后 | 展示什么 |
| -- | -------- | -------- |
| **CP1 深度与范围** | Step 0 | 图类型（简单/综合）、预计区域数、是否需研究 |
| **CP2 视觉计划** | Step 4 | 每个概念的计划视觉模式、布局方向、区域数 |
| **CP3 分段交付** | 每个区域（仅大图） | 当前区域渲染的 PNG |
| **CP4 最终交付** | Step 6 | 最终渲染 PNG |

跳过规则：请求明显简单 → 跳过 CP1；≤3 元素且模式选择明显 → 跳过 CP2；**CP4 始终执行**。

## 视觉模式库

| 概念... | 用这个模式 |
| ------- | ---------- |
| 产生多个输出 | **Fan-out**（中心辐射箭头）|
| 合并多个输入为一个 | **Convergence**（漏斗、箭头汇聚）|
| 有层级/嵌套 | **Tree**（线条 + 自由文字，不需盒子）|
| 步骤序列 | **Timeline**（线 + 点 + 标签）|
| 循环/持续改进 | **Spiral/Cycle**（箭头回到起点）|
| 抽象状态/上下文 | **Cloud**（重叠椭圆）|
| 输入转输出 | **Assembly line**（前 → 处理 → 后）|
| 对比两者 | **Side-by-Side**（平行对比）|
| 分阶段 | **Gap/Break**（区域间视觉分隔）|

**线条作为结构**：优先用 `line`（非 arrow）作主结构元素——Timeline（竖/横线 + 小点 + 自由标签）、Tree（竖干 + 横枝 + 自由文字）、分隔虚线。线条 + 自由文字往往比盒子 + 包裹文字更干净。

## 形状与颜色

- **形状即含义**：标签/描述/细节→无形状（自由文字）；时间轴标记→小椭圆(10-20px)；起点/触发/输入→椭圆；决策→菱形；处理/动作→矩形。**默认无容器**，目标 <30% 文字元素在盒子里。
- **颜色即信息**：每个语义用途有特定填充/描边对，所有颜色选择来自 [`references/excalidraw/color-palette.md`](references/excalidraw/color-palette.md)——这是颜色唯一真相源，不要凭空造色。
- **现代美学**：`roughness: 0`（现代/技术，默认）/ `1`（手绘感）；`opacity: 100`（不用透明度做层次）；字号/字重/颜色做层次而非靠盒子。

## 大图策略（强制分段）

**综合/技术图必须逐区域生成 JSON，禁止一次性输出完整 JSON。** 单次响应有 ~32000 token 输出上限，大图极易超限；即使不超，分段质量也更好。

1. 建基础文件（JSON 包裹 + 第一个区域）。
2. 每次编辑添加一个区域，用描述性字符串 ID（如 `trigger_rect`、`arrow_fan_left`），按区域命名空间化 seed（区域1用100xxx，区域2用200xxx）。
3. 边写边更新跨区域绑定（新区域箭头连旧区域元素时，同时编辑旧元素的 `boundElements`）。
4. 全部区域就位后通读检查跨区域绑定、间距、ID 引用。
5. 然后进入渲染验证循环。

## 渲染验证（强制）

JSON 单看无法判断图的好坏。生成/编辑后**必须**渲染成 PNG 并用 Read 工具实际查看，在循环中修复直到通过：

```bash
# {SKILL_DIR} 为本 skill 的安装目录（如 ~/.zcode/skills/cangjie 或 .claude/skills/cangjie，以实际环境为准），渲染脚本自身用 __file__ 定位，无硬编码路径
# 首次设置（仅一次）
cd {SKILL_DIR}/references/excalidraw && uv sync && uv run playwright install chromium
# 渲染
cd {SKILL_DIR}/references/excalidraw && uv run python render_excalidraw.py <path-to-file.excalidraw>
# 输出 PNG 在 .excalidraw 同目录，然后用 Read 工具查看
```

**循环**：渲染并查看 → 对照原始设计审计（结构是否匹配概念、模式是否如计划、眼睛流动是否正确）→ 检查视觉缺陷（文字被裁切/溢出、元素重叠、箭头穿过元素或落空、标签歧义、间距不均、文字太小、构图失衡）→ 修复 JSON → 重新渲染 → 重复，通常 2-4 轮。不要因为没严重 bug 就停——构图能更好就改。

## 证据构件（技术图）

技术图必须包含证明准确性的具体例子：

| 构件类型 | 何时用 | 怎么渲染 |
| -------- | ------ | ------- |
| 代码片段 | API、集成、实现细节 | 深色矩形 + 语法着色文字 |
| 数据/JSON 示例 | 数据格式、schema、payload | 深色矩形 + 着色文字 |
| 事件/步骤序列 | 协议、工作流、生命周期 | Timeline 模式 |
| UI 模型 | 展示实际输出/结果 | 嵌套矩形模拟真实 UI |
| API/方法名 | 真实函数调用、端点 | 用文档里的真实名字，不用占位符 |

## Multi-Zoom 架构（综合图）

综合图同时在多个缩放层级运作：**Level 1 总结流**（简化概览，常在顶部/底部）+ **Level 2 区域边界**（分组相关组件的标记区域）+ **Level 3 区域内细节**（证据构件、代码片段、具体例子——教育价值所在）。综合图应包含全部三层。

## 容器 vs 自由文字

**默认自由文字，只在服务于目的时加容器。** 用容器当：是区域焦点/需视觉分组/箭头要连它/形状本身承载含义/代表系统中一个独立"东西"。否则用自由文字（标签、描述、元数据、章节标题）——靠字号字重做层次，28px 标题不需要矩形包裹。**容器测试**：每个盒装元素问"作为自由文字可行吗？"，可以就去掉盒子。

## 边界情况

| 情况 | 处理 |
| ---- | ---- |
| 请求模糊无法定图类型 | 问**一个**针对性问题（不是清单）："这图给谁看？技术团队还是管理层？"；用户不说就默认简单图（加细节比删细节容易） |
| `render_excalidraw.py` 崩溃 | Playwright/Chromium 未装 → `uv sync && uv run playwright install chromium` 后重试 |
| 渲染超时(>30s) | 元素过多/复杂 SVG → 减到核心元素重试 |
| 渲染出空白 PNG | JSON 结构无效 → 先 `jq . file.excalidraw` 校验，修复结构错误重渲染 |
| 渲染空白/报 CDN 错（esm.sh 导入失败） | 检查网络与 esm.sh 可达性；离线环境无法完成渲染验证，显性告知用户而非假装成功 |
| 渲染 3 次重试仍失败 | 直接交付 `.excalidraw` JSON，告诉用户去 [excalidraw.com](https://excalidraw.com) 打开 |
| JSON 截断（输出上限） | 文件不以 `}` 结尾 → 立即切分段模式，从最后完整区域续 |
| 元素引用无效 | `boundElements` ID 在 elements 中找不到 → 移除悬空引用，生成目标元素后重新绑定 |
| 文件保存 | 默认当前目录 `{topic}-diagram.excalidraw`；用户指定路径则跟随；总是同时保存 `.excalidraw`（源）和 `.png`（预览） |

## 参考文件

- [`references/excalidraw/color-palette.md`](references/excalidraw/color-palette.md) — 颜色唯一真相源（语义形状色、文字层次色、证据构件色），生成任何图前先读
- [`references/excalidraw/element-templates.md`](references/excalidraw/element-templates.md) — 每种元素类型（text/line/dot/rectangle/arrow）的可复制 JSON 模板
- [`references/excalidraw/json-schema.md`](references/excalidraw/json-schema.md) — Excalidraw JSON 结构规范
- [`references/excalidraw/render_excalidraw.py`](references/excalidraw/render_excalidraw.py) — PNG 渲染脚本（playwright + chromium）
