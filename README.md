# Cangjie (仓颉) — Content Transformation & Refinement Skill

[![GitHub Release](https://img.shields.io/github/v/release/Kirky-X/cangjie?style=flat-square)](https://github.com/Kirky-X/cangjie/releases)
[![GitHub License](https://img.shields.io/github/license/Kirky-X/cangjie?style=flat-square)](LICENSE)

Cangjie is an AI agent skill with **four content transformation modes**, selected by user intent:

1. **Summarization (default)** — Organizes **text, audio, video, transcripts, and papers** into archivable structured documents: learning notes, book summaries, podcast recaps, meeting minutes, project reports, research analyses, paper reading notes, and product documents like PRD / TRD / BP / competitive analysis / literature review.
2. **Video Script** — Transforms articles/news/blogs/policy docs or a one-line idea into a ready-to-use shot-by-shot storyboard for text-to-video models (LTX-2 prompt spec).
3. **Humanization** — Removes AI writing traces from text, making it sound natural and human.
4. **Diagram** — Creates `.excalidraw` JSON diagrams that argue visually (workflows, architectures, concepts), rendered to PNG.

Core principle (Mode 1): **Identify user intent first, then select a template, then extract high-density information**. User-specified templates always take priority; when no "brief/ultra-short" version is requested, the default output is a `standard-detailed` version rather than just an outline. See [SKILL.md](SKILL.md) for the full routing table, mode selection, and workflow documentation.

## Features

### 6 Template Families

| Family     | Representative Templates                                                                          | Purpose                         |
| ---------- | ------------------------------------------------------------------------------------------------- | ------------------------------- |
| `learning` | `course-notes` / `nonfiction-book-summary` / `fiction-book-summary`                              | Learning, review, knowledge distillation |
| `media`    | `podcast-summary` / `video-program-summary`                                                       | Program recaps, highlight distribution |
| `meeting`  | `decision-minutes` / `interview-record`                                                           | Minutes, interviews, co-creation records |
| `business` | `project-status-report` / `executive-brief`                                                       | Reporting, risk, action tracking |
| `analysis` | `research-brief` / `decision-memo` / `paper-summary` (with theoretical/experimental/systems/survey subtypes) | Research synthesis, decision support, paper reading |
| `product`  | `prd` / `trd` / `business-plan` / `competitive-analysis` / `literature-review`                    | Product docs, business plans, technical design |

### Multi-Modal Input Processing

- **Text**: Directly identify intent and structure; long books auto-detect "full book / section / chapter" hierarchy
- **Audio**: Auto-detect single/multi speaker; meetings and interviews use diarization transcription with speaker identification
- **Video**: Extract audio first then transcribe; visual chapters added for screen/PPT/demo-dependent content
- **Paper**: Auto-detect type (theoretical / experimental / systems / survey) and match sub-template

### Output Quality Guardrails

- **Mandatory file output**: All summary outputs must be written to `.md` files; display-only in conversation is prohibited
- **Books default to multi-file**: 1 full-book overview + N independent chapter files; full-book file must have book-level distillation (not chapter summary concatenation)
- **Controllable density**: `brief` / `standard-detailed` (default) / `deep-dive` three levels
- **No fabrication**: Missing information explicitly marked as "material not provided / cannot confirm"; no assumptions
- **Hierarchical compression**: Chapters >12 auto-enable `hierarchical-compression`; >20 weighted by core chapters

## Installation

### Option 1: Install via `skills` package (recommended)

Requires [Node.js](https://nodejs.org/) 18+ and the `skills` npm package (v1.5.12+).

```bash
# Install to Claude Code
npx skills add https://github.com/Kirky-X/cangjie.git --agent claude-code -y

# Equivalent shorthand (owner/repo)
npx skills add Kirky-X/cangjie --agent claude-code -y

# Install to Trae
npx skills add Kirky-X/cangjie --agent trae -y

# List all discoverable skills in the repo (without installing)
npx skills add https://github.com/Kirky-X/cangjie.git --list
```

After installation, skill files are located in the corresponding agent's skills directory (e.g., `.claude/skills/cangjie/`).

### Option 2: Traditional git clone

```bash
git clone https://github.com/Kirky-X/cangjie.git
# Symlink or copy SKILL.md + references/ + scripts/ to agent skills directory
# Example skills directory paths for various runtimes (pick one):
#   Claude Code:  ~/.claude/skills/cangjie/
#   Trae:         ~/.trae-cn/skills/cangjie/
#   Cursor:       ~/.cursor/skills/cangjie/
#   Codex:        ~/.codex/skills/cangjie/
```

## Usage Examples

Cangjie is loaded as a skill by the agent and triggered via natural language intent, no explicit commands needed. Trigger words by mode:

- **Mode 1 (Summarization)**: "summarize", "content summary", "meeting minutes", "report summary", "learning notes", "podcast summary", "paper summary", "transcription", "PRD", "BP", "TRD", "competitive analysis", "market research", "literature review"
- **Mode 2 (Video Script)**: "视频脚本", "分镜", "分镜头", "拍成短片", "video prompt", "text-to-video", "AI视频生成"
- **Mode 3 (Humanization)**: "humanize", "人性化", "去AI痕迹", "去AI味", "去除AI写作痕迹"
- **Mode 4 (Diagram)**: "画图", "流程图", "架构图", "示意图", "图解", "diagram", "visualize", "excalidraw"

### Course Video → Learning Notes

```text
Summarize this Python beginner course video into learning notes
```

Recommended template: `learning/course-notes` (for hands-on content, add `learning/tutorial-playbook`)

### Non-Fiction Book → Full Book + Chapter Files

```text
Summarize this business book, give me a chapter-by-chapter summary plus a full-book core argument summary
```

Recommended template: `learning/nonfiction-book-summary` (default output: 1 full-book overview + N independent chapter files)

### Project Meeting → Decision Minutes

```text
Generate minutes from this project meeting recording, including decisions and action items
```

Recommended template: `meeting/decision-minutes`

### Paper Reading → Auto-Subtype Matching

```text
Summarize this paper, tell me the research topic, main contributions, key formulas, and limitations
```

Recommended template: `analysis/paper-summary`, auto-subdivides based on content signals:
- Theorems/proofs/formula derivations → `analysis/theoretical-paper-summary`
- Datasets/metrics/experimental comparisons → `analysis/experimental-paper-summary`
- System architecture/throughput/latency → `analysis/systems-paper-summary`
- Literature survey/taxonomy → `analysis/survey-paper-summary`

### Product Requirements Document

```text
Help me write a PRD including user journey, feature details, acceptance criteria, and non-functional requirements
```

Recommended template: `product/prd`

## Toolchain

| Tool             | Install Command                                      | Purpose                |
| ---------------- | ---------------------------------------------------- | ---------------------- |
| `ffmpeg`         | `apt install ffmpeg`                                 | Extract audio from video |
| `faster-whisper` | `pip install faster-whisper librosa torch`           | ASR transcription (primary) |
| `qwen-asr`       | `pip install qwen-asr torch`                         | ASR transcription (alternative) |
| `chub`           | See [`references/guides/api-docs.md`](references/guides/api-docs.md) | Fetch latest third-party API docs |

GPU check:

```bash
python -c "import torch; print('CUDA:', torch.cuda.is_available())"
```

### Scripts

| Script                              | Purpose                          |
| ----------------------------------- | -------------------------------- |
| `scripts/extract_audio.py`        | Extract audio from video         |
| `scripts/transcribe_with_diarization.py`  | Single-speaker course/lecture transcription |
| `scripts/transcribe_diarize_fw.py`        | Multi-speaker meeting/interview transcription (with speaker diarization) |

## Directory Structure

```
cangjie/
├── SKILL.md                  # Main entry: routing table / workflow / output rules
├── references/
│   ├── registry.yaml         # Template registry
│   ├── taxonomy.yaml         # Template taxonomy
│   ├── families/*.yaml       # 6 template family definitions
│   ├── guides/               # Template selection / authoring / output skeleton guides
│   └── templates-index.md    # Template index (points to ../templates/)
├── templates/                # All document templates (Product / Strategy / Delivery / Operations / Technology / General)
└── scripts/                  # ASR / audio extraction scripts
```

## Output Density Strategy

| Mode                | Use Case                         | Content Coverage                             |
| ------------------- | -------------------------------- | -------------------------------------------- |
| `brief`             | User explicitly requests quick-read version | Conclusions only + few key points + minimal action items |
| `standard-detailed` | **Default**                      | All required sections + sufficient facts and evidence |
| `deep-dive`         | User requests "detailed breakdown / complete notes / comprehensive" | Increased section-level hierarchy and evidence density (including formulas/experiments) |

## Anti-Patterns (Do Not Do)

- Do not treat "section header + one sentence" as a "standard detailed summary"
- Do not treat "chapter-by-chapter summary concatenation" as a "full book summary" (full book file must have book-level distillation)
- Do not write third-party API call code from training memory (must use `chub get` first)
- Do not disguise "discussion minutes" as "decision minutes" (do not fabricate responsible persons when ACTION items are missing)
- Do not disguise excerpted input as complete full-book reading results
- Do not force-fill content for short chapters (should mark "material not provided / cannot confirm")

## License

MIT
