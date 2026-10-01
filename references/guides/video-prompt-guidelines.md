# 影视化提示词规范（LTX-2 风格）

这份文件是写每个镜头(shot)提示词时的权威参考。先看"核心原则"和"六大要素"，写的时候再去查对应的术语表。

跨镜头的运镜选择（每个运镜术语的情绪域、起承合叙事弧线的运镜序列模板）见 [`camera-movements.md`](camera-movements.md)；本文件只管单个镜头的提示词怎么写。

## 一、核心原则：好提示词 = 完整的故事画面

提示词需要**从头到尾自然流动**，像一个摄影指导在口述分镜表（shot list）一样——具体、按时间顺序、不抽象。涵盖模型生成这一个镜头所需的全部元素，但呈现成一段连贯的文字，而不是罗列的清单。直接从动作开始写，描述要literal（字面、具体），不要用比喻或抽象词。

## 二、六大关键要素（每个镜头都要自然带出）

| 要素 | 说明 | 示例关键词 |
|---|---|---|
| **镜头设定** | 景别、电影类型风格 | wide shot, close-up, cinematic, documentary |
| **场景搭建** | 光线、色彩、纹理、氛围 | golden hour, neon glow, fog, wooden floor |
| **动作描述** | 核心动作的自然时间序列 | walks slowly → stops → turns around |
| **角色定义** | 年龄、发型、服装、情绪、身体语言 | woman in her 30s, nervous, sweating |
| **镜头运动** | 何时移动、如何移动、移动后呈现什么 | pans left, dolly back, zoom in, handheld |
| **音频/对话** | 环境音、音乐、台词（加引号） | "We need to run.", ambient rain, robotic voice |

写的时候建议按这个顺序组织思路（不代表句子顺序要机械照搬）：

1. 用一句话写清楚主要动作
2. 补充具体的动作和手势细节
3. 精确描述角色/物体的外观
4. 描述背景和环境细节
5. 写明镜头角度和运动方式
6. 描述光线和色彩
7. 标注任何变化或突发事件

## 三、最佳实践

- **单一段落**：保持提示词为连贯的流畅段落，不要分点罗列
- **现在时态**：描述动作一律用现在时（walks, not walked）
- **细节匹配景别**：特写(close-up)需要更精确的细节，远景(wide shot)则不必面面俱到
- **镜头运动聚焦主体关系**：明确相机与主体的相对运动，而不是单纯说"镜头移动"
- **长度控制**：4-8 个描述句覆盖所有关键方面，控制在200词以内
- **风格术语前置**：如果有明确的风格定位，放在句首，例如 "sci-fi style cinematic scene, ..."
- **快速迭代心态**：第一版不用追求完美，先写出一版完整的，后续根据反馈再调整某个细节

## 四、风格分类与可用术语

| 类别 | 可用风格 |
|---|---|
| **动画** | stop-motion, 2D/3D animation, claymation, hand-drawn, pixar style |
| **风格化** | comic book, cyberpunk, 8-bit pixel, surreal, minimalist, painterly |
| **电影感** | period drama, film noir, fantasy, epic space opera, thriller, arthouse, documentary |

## 五、技术风格标记词

| 维度 | 可用术语 |
|---|---|
| **镜头语言** | follows, tracks, pans, circles around, tilts, pushes in, pulls back, overhead, handheld, OTS (over-the-shoulder), static |
| **胶片特性** | jittery stop-motion, pixelated edges, lens flares, film grain |
| **空间尺度** | expansive, epic, intimate, claustrophobic |
| **节奏/时间效果** | slow motion, time-lapse, rapid cuts, lingering shot, continuous shot, freeze-frame, fade-in/out |
| **视觉特效** | motion blur, depth of field, particle systems |

## 六、这类模型擅长什么（设计镜头时优先往这些方向靠）

| 优势领域 | 具体说明 |
|---|---|
| 电影构图 | 宽/中/特写镜头，精心设计的光线，浅景深，自然运动 |
| 情感人类时刻 | 单人情绪表达、微妙手势、面部细微变化 |
| 氛围与场景 | 雾、薄雾、黄金时刻光线、软阴影、雨、反射、环境纹理 |
| 清晰的镜头语言 | "slow dolly in"、"handheld tracking"、"over-the-shoulder" 等明确指令 |
| 风格化美学 | 绘画感、黑色电影、模拟胶片、时尚编辑、像素动画、超现实艺术 |
| 光影与情绪控制 | 逆光、调色板、软轮廓光、闪烁灯光——比笼统的情绪词更有效 |
| 语音 | 角色可用多种语言说话和唱歌 |

## 七、避免事项

| 禁忌 | 原因 | 替代方案 |
|---|---|---|
| 纯内心状态标签（"sad"、"confused"） | 模型无法直接生成内心状态 | 用姿势、手势、面部表情描述 |
| 文字和Logo | 模型无法生成可读/一致的文字 | 避免标牌、品牌名、印刷材料 |
| 复杂物理或混乱运动（跳跃、杂耍） | 非线性/快速扭转运动易产生伪影 | 舞蹈通常效果较好 |
| 场景过度复杂 | 过多角色、分层动作、过多物体降低清晰度 | 从简单开始，单个镜头聚焦一件事 |
| 矛盾的光源逻辑 | 冲突光源导致不自然 | 除非有明确动机，否则不混用冷暖光源 |
| 过度复杂的提示词 | 动作/角色/指令越多，遗漏概率越高 | 先简单，需要时再逐步叠加细节 |

## 八、对话格式规范

```
角色名（情绪/语气）："台词内容"
```

可选：注明语言和口音，写在台词描述附近，例如 `with an angry tone` 、`with a low robotic voice` 、`speaking in French`。

对话不要太长，一两句最自然——这是单个镜头里的台词，不是整段对白。

## 九、完整示例

**镜头大纲**：深夜便利店，疲惫的店员看到老朋友突然出现在门口。

**提示词**：
```
A wide cinematic shot of a small convenience store at night, rain streaking
down the front windows and neon signage casting a soft blue-green glow across
the wet pavement outside. A tired store clerk in his 20s, wearing a rumpled
uniform vest, stands behind the counter restocking a shelf, his shoulders
slumped, movements slow and mechanical. The automatic door chimes and slides
open; he glances up sharply. The camera slowly pushes in toward his face as
his expression shifts from exhaustion to disbelief, eyes widening, a faint
smile breaking through. Warm golden light spills in briefly from the open
doorway, contrasting with the cool fluorescent interior. Soft ambient rain
and the low hum of a refrigerator fill the background. He says, "It's really
you?", his voice cracking slightly.
```

可以看到：单段落、现在时、六要素都自然带出（远景转推近的镜头运动、雨夜便利店的场景、店员的外观与动作、光线从冷到暖的对比、对话）、没有内心状态标签（用"耸肩""睁大眼睛""声音哽咽"代替"tired" "surprised"这类直接标签）、没有要求画面文字。

## 十、最终检查清单

写完每个镜头提示词后过一遍：

- [ ] 单一流畅段落，没有分点罗列
- [ ] 现在时态
- [ ] 4-8句描述，控制在200词以内
- [ ] 自然涵盖六大要素（镜头、场景、动作、角色、相机运动、音频/对话）
- [ ] 没有纯情绪标签，用的是可视化的身体语言
- [ ] 没有要求画面里出现文字/Logo
- [ ] 镜头运动与主体的关系写清楚了（不是"camera moves"这种空泛描述）
- [ ] 风格术语放在了句首（如果这个镜头有明确风格定位）
- [ ] 细节程度匹配景别——特写细，远景粗
- [ ] 单个镜头里动作/角色数量克制，没有塞太多东西
- [ ] 光源逻辑自洽，没有无理由的冷暖光混用

这份清单管单镜头写得对不对；跨镜头的结构规则（单镜头时长分档、运镜枚举与连续限制、台词语速折算）不用人工背，交付前跑确定性校验：

```bash
# {SKILL_DIR} 为本 skill 的安装目录（如 ~/.zcode/skills/cangjie）
python3 {SKILL_DIR}/scripts/validate_video_script.py <shots.json 路径>
```

FAIL 必须清零后才渲染交付格式（流程见 `modes/video-script.md` 第四步）；WARN 是建议项，逐条判断。
