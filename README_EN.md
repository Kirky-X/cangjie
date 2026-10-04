# Cangjie — Content Transformation & Refinement Skill

> Four content-transformation modes: summarizing into structured notes / product docs, generating text-to-video storyboard scripts, removing AI writing traces, and creating Excalidraw diagrams. Routing follows user intent; when intent is unclear, candidate modes are listed for the user to choose — no guessing.

English | [中文](README.md)

[![GitHub Release](https://img.shields.io/github/v/release/Kirky-X/cangjie?style=flat-square)](https://github.com/Kirky-X/cangjie/releases)
[![License](https://img.shields.io/github/license/Kirky-X/cangjie?style=flat-square)](LICENSE)

## ✨ Features

**Four-mode routing** (trigger signals in [SKILL.md](SKILL.md)):

| Mode | Function | Mode file |
| ---- | ---- | -------- |
| 1 · Content Summarization (default) | Text/audio/video/transcripts/papers → structured notes or product docs such as PRD/TRD/BP/competitive analysis/literature review | [modes/summarization.md](modes/summarization.md) |
| 2 · Video Script | Articles/ideas → shot-by-shot storyboard scripts (LTX-2 text-to-video prompt spec) | [modes/video-script.md](modes/video-script.md) |
| 3 · AI-Trace Removal | Removes AI writing traces from text | [modes/humanization.md](modes/humanization.md) |
| 4 · Diagram | `.excalidraw` JSON diagrams (flow/architecture/concept), rendered to PNG | [modes/diagram.md](modes/diagram.md) |

**55-template registry** (`references/registry.yaml`, 6 families): product 26 / analysis 9 / learning 6 / meeting 5 / business 5 / media 4. Each template defines required_sections / optional_sections / detection_signals / fallback (the fallback template used when required_sections cannot be filled after generation). When auto-matching hits multiple templates, candidates are listed by signal-hit count for the user to pick; with zero hits it falls back to the default family.

**Quality guardrails**: every summary must be written to disk as a `.md` file — conversation-only display is forbidden; books default to 1 whole-book review + N independent chapter files (the whole-book file must contain book-level synthesis, not stitched chapters); missing material is explicitly marked "material not provided / cannot be confirmed" — padding is forbidden; hierarchical compression is enabled automatically when chapters > 12.

**Three detail levels**: `brief` (conclusion-centric) / `standard-detailed` (default, complete sections + solid factual evidence) / `deep-dive` (deeper hierarchy and denser evidence).

**Transcription disclaimer**: the `SpeakerN` labels of `transcribe-diarize` are **energy-fluctuation-based approximate segmentation** (not voiceprint identification), and the output file header carries a built-in disclaimer; downstream minutes must say "approximate attribution / same speech segment" and must never treat speaker attribution as fact.

## 📦 Installation

```bash
# Option 1: sync to the agent skill dirs (~/.zcode/skills and ~/.claude/skills)
# Note: the script lives at the skills workspace root (../scripts/sync-skills.sh, relative to this repo root), not inside this repo;
# if you cloned this repo from GitHub, use Option 3 below instead
bash ../scripts/sync-skills.sh cangjie

# Option 2: manual copy
cp -r cangjie ~/.zcode/skills/cangjie

# Option 3: Remote install (GitHub repo)
npx skills add Kirky-X/cangjie --agent claude-code -y
```

Requires `Python >= 3.8`. Install the dependencies before using audio transcription (once, on the first run):

```bash
pip install -r requirements.txt   # torch / faster-whisper / librosa / numpy / qwen-asr
apt install ffmpeg                # extract audio from video
```

Diagram rendering (mode 4) additionally requires Python >= 3.11 (`references/excalidraw/pyproject.toml` pins `>=3.11`, higher than the 3.8 baseline of the core dependencies) and Playwright: `cd references/excalidraw && uv sync && uv run playwright install chromium`. GPU check: `python -c "import torch; print('CUDA:', torch.cuda.is_available())"`; without a GPU, faster-whisper automatically falls back to cpu + int8.

## 🚀 Quick Start

```bash
# One-shot pipeline: video → extract audio → transcribe → output
python3 scripts/cangjie.py pipeline input.mp4 --engine faster-whisper

# Single steps; audio is kept by default, --cleanup cleans up explicitly (reverse switch)
python3 scripts/cangjie.py extract-audio input.mp4
python3 scripts/cangjie.py transcribe-diarize input.wav output.txt --num-speakers 3 --language zh
python3 scripts/cangjie.py transcribe-qwen input.wav output.txt

# Render Excalidraw JSON to PNG (2x scale by default)
python3 references/excalidraw/render_excalidraw.py diagram.excalidraw
```

Natural-language trigger examples: `summarize this paper into reading notes`, `generate decision minutes from this meeting recording`, `turn this article into a video storyboard`, `remove the AI flavor from this text`, `draw an (excalidraw) architecture diagram`.

```mermaid
flowchart LR
    A[Video/audio input] --> B[extract-audio<br>ffmpeg 16kHz mono wav]
    B --> C{Transcription engine}
    C -->|Multi-speaker| D[transcribe-diarize<br>faster-whisper + energy-based approximate segmentation]
    C -->|Chinese single track| E[transcribe-qwen<br>qwen-asr]
    D --> F[Transcript .txt<br>header carries disclaimer]
    E --> F
    F --> G[Mode 1 summarization<br>55-template registry matching]
```

## ✅ Tests & Verification

The deterministic validators and the CLI ship with pytest unit tests (`tests/`); the transcription/rendering chain is verified by actually running real commands:

- `python3 -m pytest tests/ -q`: script-level unit tests (CLI argument handling / transcription arguments / video-script validation / summary audit / Excalidraw validation); side-effect scripts (model download / GPU inference / real transcoding) intentionally skip offline fake tests — per-item reasons in `tests/SKIPPED.md`
- `python3 scripts/skill_lint.py .`: repo engineering-baseline lint (SKILL.md frontmatter/version consistency, existence of `.md` paths referenced in docs, JSON asset parseability, CLI-subcommands-vs-docs gate; exit code 0 = no FAIL / 1 = FAIL present)
- Mode-routing eval set: `evals/evals.json`, 11 cases (4 positive + 7 boundary negatives — 6 verifying handoff to wudaozi / maliang / diting / kueiku / liuxiang, 1 out-of-boundary refusal)
- Trigger eval set: `triggers/trigger-queries.json`, 22 queries (expect: trigger 15 / no 7)
- `python3 scripts/cangjie.py --help`: confirm that the 4 subcommands (extract-audio / transcribe-diarize / transcribe-qwen / pipeline) and the `--cleanup` reverse-switch description print correctly
- `python3 references/excalidraw/render_excalidraw.py --help`: renderer flags (--output/--scale/--width) work correctly
- Template count measured: parsing `references/registry.yaml` yields 55 templates (product 26 / analysis 9 / learning 6 / meeting 5 / business 5 / media 4)
- The rendering chain depends on the esm.sh-pinned `@excalidraw/excalidraw@0.17.6` (see `references/excalidraw/render_template.html`), preventing silent rendering failures caused by unpinned version drift; esm.sh must be reachable over the network
- The full transcription/rendering pipeline requires ffmpeg + ASR models + Chromium; on machines without them, the above commands failing with dependency-missing errors is the expected behavior

## 📁 Directory Structure

```
cangjie/
├── SKILL.md                      # Entry point: mode routing table + shared resources index
├── requirements.txt              # ASR dependencies (torch/faster-whisper/librosa/qwen-asr)
├── modes/                        # 4 mode workflows (summarization/video-script/humanization/diagram)
├── references/
│   ├── registry.yaml             # 55-template registry (with fallback)
│   ├── taxonomy.yaml             # Template taxonomy
│   ├── families/*.yaml           # 6 template family definitions
│   ├── guides/                   # Template selection / output skeletons / detail policy / video prompt spec, etc.
│   └── excalidraw/               # Render scripts + palette + JSON structure (esm.sh pinned to 0.17.6)
├── templates/                    # 30 document templates + 1 lifecycle document map (templates/Product/README.md)
├── tests/                        # pytest unit tests (CLI / transcription args / video script / summary audit / Excalidraw validation)
└── scripts/                      # cangjie.py unified CLI + transcription scripts + mode validators + skill_lint.py repo lint
```

## 🔮 Boundaries

- AI drawing/illustration generation belongs to **wudaozi**, and product UI design belongs to **maliang** — "diagram" in this skill refers only to Excalidraw diagrams
- Transcription speaker labels are energy-based approximate segmentation; voiceprint-grade speaker identification is not promised
- No fabrication without material: when required_sections lack material, mark it instead of inventing; do not pass stitched chapters off as a whole-book review, and do not dress discussion minutes up as decision minutes
- Never write third-party API call code from training memory; first use `chub` to fetch the latest documentation

## 📄 License & Attribution

[MIT](LICENSE) © Kirky-X. Install/sync and retirement governance are managed centrally by `scripts/sync-skills.sh` at the repository root.
