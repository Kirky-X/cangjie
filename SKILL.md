---
name: cangjie
description: "Content transformation & refinement skill with four modes: (1) summarize text/audio/video/transcripts/papers into structured notes or product documents; (2) generate AI video storyboards from articles/ideas; (3) humanize text to remove AI writing traces; (4) create Excalidraw diagrams that argue visually. Triggers: summarize/meeting minutes/paper summary/PRD/BP/TRD/literature review/video script/分镜/humanize/去AI痕迹/画图/流程图/架构图/diagram/visualize"
version: 0.3.0
source: local-skill
triggers:
  # Mode 1: summarization
  - summarize
  - content summary
  - meeting minutes
  - generate minutes
  - report summary
  - learning notes
  - podcast summary
  - video summary
  - paper summary
  - transcription
  - qwen-asr
  - faster-whisper
  - ffmpeg
  - PRD
  - business plan
  - BP
  - technical requirements
  - TRD
  - architecture design
  - competitive analysis report
  - market research
  - literature review
  - chub
  # Mode 2: video script generation
  - video script
  - 视频脚本
  - 分镜
  - 分镜头
  - 拍成短片
  - video prompt
  - text-to-video
  - AI视频生成
  - 文生视频
  # Mode 3: humanization
  - humanize
  - 人性化
  - 去AI痕迹
  - 去AI味
  - 去除AI写作痕迹
  - 去除AI味
  # Mode 4: diagram
  - 画图
  - 流程图
  - 架构图
  - 示意图
  - 图解
  - 绘图
  - diagram
  - visualize
  - excalidraw
requires:
  python: ">=3.8"
  pip: [faster-whisper, qwen-asr, librosa, numpy, torch]
---

# Content Transformation & Refinement Skill - Cangjie

Four content transformation modes, selected by user intent:

| Mode | What it does | Trigger signals | Detail |
| ---- | ------------ | --------------- | ------ |
| **Mode 1: Summarization** (default) | Organizes text/audio/video/transcripts/papers into structured notes or product documents | summarize / meeting minutes / paper summary / PRD / BP / TRD | [modes/summarization.md](modes/summarization.md) |
| **Mode 2: Video Script** | Transforms articles/ideas into shot-by-shot storyboards for text-to-video models | 视频脚本 / 分镜 / video prompt / text-to-video | [modes/video-script.md](modes/video-script.md) |
| **Mode 3: Humanization** | Removes AI writing traces from text | humanize / 去AI痕迹 / 去AI味 | [modes/humanization.md](modes/humanization.md) |
| **Mode 4: Diagram** | Creates `.excalidraw` JSON diagrams that argue visually | 画图 / 流程图 / 架构图 / diagram / visualize | [modes/diagram.md](modes/diagram.md) |

**Mode routing**: scan the trigger signals above. Mode 1 is the default when the user wants to *organize/summarize* content into structured docs; Mode 2 when they want to *turn content into a video*; Mode 3 when they want to *refine/de-AI* existing text; Mode 4 when they want to *visualize concepts as a diagram*. When intent is ambiguous, list candidate modes and ask the user—do not guess.

**After routing, load the corresponding mode file for full workflow details.**

## Shared Resources

| Resource | Path |
| -------- | ---- |
| Template registry | `references/registry.yaml` |
| Template taxonomy | `references/taxonomy.yaml` |
| Template families | `references/families/*.yaml` |
| Template selection guide | `references/guides/template-selection.md` |
| Output skeletons | `references/guides/output-skeletons.md` |
| Detail policy | `references/guides/detail-policy.md` |
| Examples | `references/guides/examples.md` |
| Video prompt guidelines | `references/guides/video-prompt-guidelines.md` |
| Excalidraw color palette | `references/excalidraw/color-palette.md` |
| Excalidraw element templates | `references/excalidraw/element-templates.md` |
| Excalidraw JSON schema | `references/excalidraw/json-schema.md` |

## CLI Tools

```bash
# One-shot pipeline: video → extract audio → transcribe → output
python3 scripts/cangjie.py pipeline input.mp4 --engine faster-whisper

# Individual steps
python3 scripts/cangjie.py extract-audio input.mp4 --keep-audio
python3 scripts/cangjie.py transcribe-diarize input.wav output.txt --num-speakers 3 --language zh
python3 scripts/cangjie.py transcribe-qwen input.wav output.txt
```

| Tool             | Install                                                               | Purpose                    |
| ---------------- | --------------------------------------------------------------------- | -------------------------- |
| `ffmpeg`         | `apt install ffmpeg`                                                  | Extract audio from video   |
| `faster-whisper` | `pip install faster-whisper librosa torch`                            | ASR transcription          |
| `qwen-asr`       | `pip install qwen-asr torch`                                          | ASR alternative            |
| `chub`           | See [`references/guides/api-docs.md`](references/guides/api-docs.md)  | Fetch latest third-party API docs |

GPU check: `python -c "import torch; print('CUDA:', torch.cuda.is_available())"`
