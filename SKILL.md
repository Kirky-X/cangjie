---
name: cangjie
description: "内容转化与精炼技能，四种模式：(1) 将文本/音频/视频/转录稿/论文整理为结构化笔记或产品文档；(2) 将文章/想法转化为文生视频分镜脚本；(3) 去除文本的 AI 写作痕迹；(4) 创建 Excalidraw 可视化图表。触发：总结/会议纪要/论文总结/PRD/BP/TRD/文献综述/视频脚本/分镜/去AI痕迹/画图(excalidraw)/流程图(excalidraw)/架构图(excalidraw)/diagram/visualize。注意：位图/插画类图片与视频画面的生成用 wudaozi（本 skill 的分镜脚本是文字脚本、Excalidraw 是 JSON 图表，均不生成图像视频）；论文检索与下载用 liuxiang（整理文献为结构化笔记归本 skill，写论文用的综述章节归 liuxiang）；决策与方法论分析用 kueiku；飞书文档内容的取回与操作用 lark；产品 UI 设计用 maliang"
version: "0.3.4"
source: local-skill
triggers:
  # 模式 1：内容总结（不含工具名——转录/ASR 属实现细节，经 description 路由即可）
  - 总结
  - 内容总结
  - 会议纪要
  - 生成纪要
  - 报告总结
  - 学习笔记
  - 播客总结
  - 视频总结
  - 论文总结
  - 转录稿
  - PRD
  - 产品需求文档
  - 商业计划书
  - 技术需求文档
  - TRD
  - 架构设计
  - 竞品分析报告
  - 市场调研
  - 文献综述
  # 模式 2：视频脚本生成
  - 视频脚本
  - 分镜
  - 分镜头
  - 拍成短片
  - video script
  - video prompt
  - text-to-video
  - AI视频生成
  - 文生视频
  # 模式 3：去 AI 痕迹
  - 去AI痕迹
  - 去AI味
  - 去除AI写作痕迹
  - 去除AI味
  - humanize
  # 模式 4：Excalidraw 图表（带限定词，避免与 wudaozi 的图片视频生成、maliang 的 UI 设计冲突）
  - excalidraw
  - 画图(excalidraw)
  - 流程图(excalidraw)
  - 架构图(excalidraw)
  - 示意图(excalidraw)
  - 图解(excalidraw)
  - 绘图(excalidraw)
  - diagram
  - visualize
requires:
  python: ">=3.8"
  pip: [faster-whisper, qwen-asr, librosa, numpy, torch]
license: MIT
metadata:
  version: "0.3.4"
  author: "Kirky-X"
  repo: "https://github.com/Kirky-X/cangjie"
  tags: "总结, 会议纪要, 论文总结, PRD, BP, TRD"
---

# 内容转化与精炼技能 · 仓颉 (Cangjie)

四种内容转化模式，根据用户意图选择：

| 模式 | 功能 | 触发信号 | 详情 |
| ---- | ---- | -------- | ---- |
| **模式 1：内容总结**（默认） | 将文本/音频/视频/转录稿/论文整理为结构化笔记或产品文档 | 总结 / 会议纪要 / 论文总结 / PRD / BP / TRD | [modes/summarization.md](modes/summarization.md) |
| **模式 2：视频脚本** | 将文章/想法转化为逐镜头分镜脚本，用于文生视频模型 | 视频脚本 / 分镜 / video prompt / text-to-video | [modes/video-script.md](modes/video-script.md) |
| **模式 3：去 AI 痕迹** | 去除文本的 AI 写作痕迹 | 去AI痕迹 / 去AI味 / humanize | [modes/humanization.md](modes/humanization.md) |
| **模式 4：画图** | 创建 `.excalidraw` JSON 可视化图表，用图形论证 | excalidraw / 画图(excalidraw) / 流程图(excalidraw) / 架构图(excalidraw) / diagram / visualize | [modes/diagram.md](modes/diagram.md) |

**模式路由**：扫描上方触发信号。当用户想要*整理/总结*内容为结构化文档时，走模式 1；想*把内容变成视频*时，走模式 2；想*润色/去 AI 味*已有文本时，走模式 3；想*将概念可视化为图表*时，走模式 4。意图不明确时，列出候选模式让用户选择——不要猜测。

**路由完成后，加载对应模式文件获取完整工作流。**

## 共享资源

| 资源 | 路径 |
| ---- | ---- |
| 模板注册表 | `references/registry.yaml` |
| 模板分类体系 | `references/taxonomy.yaml` |
| 模板族定义 | `references/families/*.yaml` |
| 模板选择指南 | `references/guides/template-selection.md` |
| 模板编写指南 | `references/guides/template-authoring.md` |
| 输出骨架 | `references/guides/output-skeletons.md` |
| 详略策略 | `references/guides/detail-policy.md` |
| 示例集 | `references/guides/examples.md` |
| API 文档查询（chub 用法） | `references/guides/api-docs.md` |
| 影视化提示词规范 | `references/guides/video-prompt-guidelines.md` |
| AI 味模式清单（模式 3 用） | `references/guides/ai-tells-checklist.md` |
| Excalidraw 调色板 | `references/excalidraw/color-palette.md` |
| Excalidraw 元素模板 | `references/excalidraw/element-templates.md` |
| Excalidraw JSON 结构 | `references/excalidraw/json-schema.md` |

**目录语义**：`templates/` 产物模板 ≡ 官方 assets 语义；`scripts/` 确定性任务；`references/` 按需上下文。

## CLI 工具

```bash
# 一键流水线：视频 → 提取音频 → 转录 → 输出
python3 scripts/cangjie.py pipeline input.mp4 --engine faster-whisper

# 单步执行（音频文件默认保留，--cleanup 显式清理）
python3 scripts/cangjie.py extract-audio input.mp4
python3 scripts/cangjie.py transcribe-diarize input.wav output.txt --num-speakers 3 --language zh
python3 scripts/cangjie.py transcribe-qwen input.wav output.txt
```

| 工具 | 安装方式 | 用途 |
| ---- | -------- | ---- |
| `ffmpeg` | `apt install ffmpeg` | 从视频提取音频 |
| `faster-whisper` | `pip install faster-whisper librosa torch` | ASR 语音转录 |
| `qwen-asr` | `pip install qwen-asr torch` | ASR 替代方案 |
| `chub` | `pip install chub` | 获取最新第三方 API 文档 |

GPU 检查：`python -c "import torch; print('CUDA:', torch.cuda.is_available())"`
