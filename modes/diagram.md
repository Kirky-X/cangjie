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

| 维度 | 简单/概念图 | 综合/技术图 |
| ---- | ---------- | ---------- |
| 视觉语言 | 抽象形状 + 标签 | 真实数据格式 + 代码片段 + 具体例子 |
| 适合场景 | 心智模型、哲学概念（概念本身就是抽象） | 真实系统、协议、架构、教学 |
| 讲解量 | 30 秒能讲完 | 2-3 分钟教学量，值得逐层展开 |

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
| Step 6 | 静态校验 → 渲染验证（render-view-fix 循环） | 静态校验零 FAIL，渲染 PNG 通过终检清单，**CP4** 用户接受 |

## 用户检查点（强制暂停）

| CP | 在哪步后 | 展示什么 |
| -- | -------- | -------- |
| **CP1 深度与范围** | Step 0 | 图类型（简单/综合）、预计区域数、是否需研究 |
| **CP2 视觉计划** | Step 4 | 每个概念的计划视觉模式、布局方向、区域数 |
| **CP3 分段交付** | 每个区域（仅大图） | 当前区域渲染的 PNG |
| **CP4 最终交付** | Step 6 | 最终渲染 PNG |

跳过规则：请求明显简单 → 跳过 CP1；≤3 元素且模式选择明显 → 跳过 CP2；**CP4 始终执行**——图是视觉产物，只有用户看过渲染效果才算交付。

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

## 尺寸与留白

**层级靠尺寸锚点表达**：同级元素保持同一尺寸，不同层级用尺寸区分——视觉重量必须与重要性一致：

| 层级 | 尺寸锚点 | 用途 |
| ---- | ------- | ---- |
| Hero | 300×150 | 全图最重要的一个元素，视觉锚点 |
| Primary | 180×90 | 主要概念 |
| Secondary | 120×60 | 次要概念、支撑细节 |
| Small | 60×40 | 标记、点缀、小节点 |

- **留白即重要性**：最重要的元素周围留白最多（200px+）——用空间而非颜色或加粗强调核心，留白是层级最安静的信号。
- **有关系必须有箭头**：位置邻近不表达关系——读者无法从摆放距离区分"相关"和"碰巧挨着"，A 与 B 相关就连箭头。

## 大图策略（强制分段）

**综合/技术图必须逐区域生成 JSON，禁止一次性输出完整 JSON。** 单次响应有 ~32000 token 输出上限，大图极易超限；即使不超，分段质量也更好。

1. 建基础文件（JSON 包裹 + 第一个区域）。
2. 每次编辑添加一个区域，用描述性字符串 ID（如 `trigger_rect`、`arrow_fan_left`），按区域命名空间化 seed（区域1用100xxx，区域2用200xxx）。
3. 边写边更新跨区域绑定（新区域箭头连旧区域元素时，同时编辑旧元素的 `boundElements`）。
4. 全部区域就位后通读检查跨区域绑定、间距、ID 引用。
5. 然后进入渲染验证循环。

## 静态校验（强制）

`jq .` 只保证语法合法，管不了结构缺陷。生成/编辑 JSON 后、渲染之前，先跑静态校验脚本（纯标准库，无需 uv 环境）：

```bash
# {SKILL_DIR} 含义同渲染命令；脚本用 __file__ 定位调色板，任意工作目录可跑
python3 {SKILL_DIR}/references/excalidraw/validate_excalidraw.py <path-to-file.excalidraw>
```

- **FAIL 必须修复后才能渲染**：顶层结构非法（type 非 excalidraw、elements 缺失或为空）、重复 id、悬空引用（boundElements / startBinding / endBinding / containerId / frameId）、绑定文字溢出容器、frame 子元素溢出——这些在渲染图上必然可见，脚本拦截比人眼在 PNG 里找可靠。
- **WARN 结合设计意图判断**：元素重叠（Cloud 模式的重叠椭圆属有意设计，忽略对应告警）、非调色板色值、字号超过 4 种、绑定关系单向缺失（只改了一侧 boundElements / containerId 回指）——可能是有意为之，拿不准就交给渲染视检确认。
- 大图每追加一个区域就跑一次：悬空引用在边写边绑定时当场暴露，不要攒到最后一起修。

## 渲染验证（强制）

静态校验通过后，渲染成 PNG 并用 Read 工具实际查看——脚本只认结构，图好不好只能看渲染结果。渲染循环是**最终确认**，不是发现结构问题的手段：

```bash
# {SKILL_DIR} 为本 skill 的安装目录（如 ~/.zcode/skills/cangjie 或 .claude/skills/cangjie，以实际环境为准），渲染脚本自身用 __file__ 定位，无硬编码路径
# 首次设置（仅一次）
cd {SKILL_DIR}/references/excalidraw && uv sync && uv run playwright install chromium
# 渲染
cd {SKILL_DIR}/references/excalidraw && uv run python render_excalidraw.py <path-to-file.excalidraw>
# 输出 PNG 在 .excalidraw 同目录，然后用 Read 工具查看
```

**循环**：渲染并查看 → 对照原始设计审计（结构是否匹配概念、模式是否如计划、眼睛流动是否正确）→ 对照下方终检清单逐项核对 → 修复 JSON → 重新渲染 → 重复，通常 2-4 轮。不要因为没严重 bug 就停——构图能更好就改。

**终检清单**（交付前逐项过，全部通过才进 CP4）：

1. 文字无裁切、无溢出
2. 无意外元素重叠（Cloud 重叠椭圆、徽标压框等有意分层除外）
3. 箭头不穿过元素、不落空，起落点明确
4. 标签无歧义
5. 文字大小可读
6. 间距均匀，同层元素对齐
7. 无密度失衡——警惕"一框一图标"的稀疏布局
8. 构图不空洞也不过挤，最重要的元素周围留白最多

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
| 元素引用无效 | 跑静态校验脚本定位全部悬空引用 → 逐条修复（移除引用或补建目标元素后重新绑定）→ 重跑确认零 FAIL，再继续渲染 |
| 文件保存 | 默认当前目录 `{topic}-diagram.excalidraw`；用户指定路径则跟随；总是同时保存 `.excalidraw`（源）和 `.png`（预览） |

## 参考文件

- [`references/excalidraw/color-palette.md`](references/excalidraw/color-palette.md) — 颜色唯一真相源（语义形状色、文字层次色、证据构件色），生成任何图前先读
- [`references/excalidraw/element-templates.md`](references/excalidraw/element-templates.md) — 每种元素类型（text/line/dot/rectangle/arrow）的可复制 JSON 模板
- [`references/excalidraw/json-schema.md`](references/excalidraw/json-schema.md) — Excalidraw JSON 结构规范
- [`references/excalidraw/validate_excalidraw.py`](references/excalidraw/validate_excalidraw.py) — 静态校验脚本（渲染前拦截重复 id/悬空引用/溢出，附美学告警）
- [`references/excalidraw/render_excalidraw.py`](references/excalidraw/render_excalidraw.py) — PNG 渲染脚本（playwright + chromium）
