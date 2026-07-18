#!/bin/bash
# Translation script - writes translated files
set -e

cd /home/kirky/projects/skills/cangjie

# README.md
cat > README.md << 'EOF'
# Cangjie (仓颉) — Content Structuring & Summarization Skill

[![GitHub Release](https://img.shields.io/github/v/release/Kirky-X/cangjie?style=flat-square)](https://github.com/Kirky-X/cangjie/releases)
[![GitHub License](https://img.shields.io/github/license/Kirky-X/cangjie?style=flat-square)](LICENSE)

Cangjie is an AI agent skill for content structuring and summarization that organizes **text, audio, video, transcripts, and papers** into archivable structured documents: learning notes, book summaries, podcast recaps, meeting minutes, project reports, research analyses, paper reading notes, as well as product documents like PRD / TRD / BP / competitive analysis / literature review.

Core principle: **Identify user intent first, then select a template, then extract high-density information**. User-specified templates always take priority; when no "brief/ultra-short" version is requested, the default output is a `standard-detailed` version rather than just an outline. See [SKILL.md](SKILL.md) for the full routing table and workflow documentation.

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

Cangjie is loaded as a skill by the agent and triggered via natural language intent, no explicit commands needed. Trigger words include "summarize", "content summary", "meeting minutes", "report summary", "learning notes", "podcast summary", "video summary", "paper summary", "transcription", "PRD", "BP", "TRD", "competitive analysis", "market research", "literature review", etc.

### Course Video -> Learning Notes

```text
Summarize this Python beginner course video into learning notes
```

Recommended template: `learning/course-notes` (for hands-on content, add `learning/tutorial-playbook`)

### Non-Fiction Book -> Full Book + Chapter Files

```text
Summarize this business book, give me a chapter-by-chapter summary plus a full-book core argument summary
```

Recommended template: `learning/nonfiction-book-summary` (default output: 1 full-book overview + N independent chapter files)

### Project Meeting -> Decision Minutes

```text
Generate minutes from this project meeting recording, including decisions and action items
```

Recommended template: `meeting/decision-minutes`

### Paper Reading -> Auto-Subtype Matching

```text
Summarize this paper, tell me the research topic, main contributions, key formulas, and limitations
```

Recommended template: `analysis/paper-summary`, auto-subdivides based on content signals:
- Theorems/proofs/formula derivations -> `analysis/theoretical-paper-summary`
- Datasets/metrics/experimental comparisons -> `analysis/experimental-paper-summary`
- System architecture/throughput/latency -> `analysis/systems-paper-summary`
- Literature survey/taxonomy -> `analysis/survey-paper-summary`

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
EOF

echo "README.md done"

# requirements.txt
cat > requirements.txt << 'EOF'
# cangjie · ML dependency lock file (ASR transcription)
# Install: pip install -r requirements.txt
# GPU users: torch selects matching CUDA version (see https://pytorch.org/get-started/locally/)
# Device auto-adapt: without GPU, faster-whisper automatically falls back to cpu + int8 (see transcribe_diarize_fw.py)

torch>=2.0.0
faster-whisper>=1.0.0
librosa>=0.10.0
numpy>=1.24.0

# qwen-asr (SenseVoice/Paraformer): install per official repo instructions, PyPI availability unconfirmed
# See SKILL.md frontmatter requires.pip for details
EOF

echo "requirements.txt done"

# scripts/cangjie.py
cat > scripts/cangjie.py << 'PYEOF'
#!/usr/bin/env python3
"""
cangjie - Unified entry point for audio transcription tools
One-click dispatch to extract-audio / transcribe-diarize / transcribe-qwen, no need to remember three commands.

Subcommands:
    extract-audio        Extract 16kHz mono wav from video (ffmpeg)
    transcribe-diarize   faster-whisper transcription + energy-based speaker diarization
    transcribe-qwen      qwen-asr transcription (Chinese-optimized)

Typical usage:
    python3 cangjie.py extract-audio input.mp4 --keep-audio
    python3 cangjie.py transcribe-diarize input.wav output.txt 3
    python3 cangjie.py transcribe-qwen input.wav output.txt
"""

import argparse
import sys
from pathlib import Path

# Sub-scripts are in the same directory as this file; add to sys.path for delayed import
_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))


def _default_output(audio_path: str, suffix: str) -> str:
    """Derive default output path from audio path (consistent with each sub-script's original main behavior)."""
    return audio_path.replace(".wav", suffix)


def cmd_extract_audio(args) -> int:
    import extract_audio as _extract_audio

    output = _extract_audio.extract_audio(args.video_path, args.audio_output)
    if args.keep_audio:
        print(output)
    else:
        print(f"{output} (temp wav cleaned up; use --keep-audio to retain)")
        Path(output).unlink(missing_ok=True)
    return 0


def cmd_transcribe_diarize(args) -> int:
    import transcribe_diarize_fw as _fw

    output = args.output or _default_output(args.audio_path, "_diarized.txt")
    _fw.transcribe_with_diarization(args.audio_path, output, args.num_speakers)
    return 0


def cmd_transcribe_qwen(args) -> int:
    import transcribe_with_diarization as _qwen

    output = args.output or _default_output(args.audio_path, "_transcript.txt")
    _qwen.transcribe_audio(args.audio_path, output)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cangjie",
        description="Unified entry point for audio transcription tools (extract audio -> transcription + speaker diarization)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Subcommand examples:\n"
            "  cangjie.py extract-audio input.mp4 --keep-audio\n"
            "  cangjie.py transcribe-diarize input.wav out.txt 3\n"
            "  cangjie.py transcribe-qwen input.wav out.txt\n"
        ),
    )
    sub = parser.add_subparsers(dest="command", required=True, metavar="<command>")

    p_extract = sub.add_parser(
        "extract-audio", help="Extract 16kHz mono wav from video (ffmpeg)"
    )
    p_extract.add_argument("video_path", help="Video file path")
    p_extract.add_argument(
        "audio_output", nargs="?", default=None, help="Output wav path (optional)"
    )
    p_extract.add_argument(
        "--keep-audio",
        action="store_true",
        help="Keep extracted wav (default: cleaned up before exit to avoid disk buildup)",
    )
    p_extract.set_defaults(func=cmd_extract_audio)

    p_fw = sub.add_parser(
        "transcribe-diarize", help="faster-whisper transcription + energy-based speaker diarization"
    )
    p_fw.add_argument("audio_path", help="Audio file path")
    p_fw.add_argument("output", nargs="?", default=None, help="Output .txt path (optional)")
    p_fw.add_argument(
        "num_speakers", nargs="?", type=int, default=3, help="Number of speakers (default: 3)"
    )
    p_fw.set_defaults(func=cmd_transcribe_diarize)

    p_qwen = sub.add_parser("transcribe-qwen", help="qwen-asr transcription (Chinese-optimized)")
    p_qwen.add_argument("audio_path", help="Audio file path")
    p_qwen.add_argument(
        "output", nargs="?", default=None, help="Output .txt path (optional)"
    )
    p_qwen.set_defaults(func=cmd_transcribe_qwen)

    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except KeyboardInterrupt:
        print("Interrupted", file=sys.stderr)
        return 130
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
PYEOF

echo "scripts/cangjie.py done"

# scripts/extract_audio.py
cat > scripts/extract_audio.py << 'PYEOF'
#!/usr/bin/env python3
"""
Video-to-audio extraction script
Uses ffmpeg to extract audio track from video files

Usage:
    python3 extract_audio.py <video_path> [audio_output_path] [--keep-audio]

Parameters:
    video_path: Video file path (supports mp4, mkv, avi, mov, webm, etc.)
    audio_output_path: Output audio path (optional, defaults to .wav file in same directory as video)

Options:
    --keep-audio: Keep extracted .wav file (default: deleted to avoid disk buildup, 1h audio approx 150MB)
"""

import argparse
import subprocess
import sys
from pathlib import Path


def extract_audio(video_path: str, audio_output: str = None) -> str:
    """
    Extract audio from video

    Args:
        video_path: Video file path
        audio_output: Output audio path (optional)

    Returns:
        Output audio file path
    """
    video_path = Path(video_path).resolve()

    if not video_path.exists():
        raise FileNotFoundError(f"Video file does not exist: {video_path}")

    if audio_output is None:
        audio_output = video_path.with_suffix(".wav")
    else:
        audio_output = Path(audio_output).resolve()

    audio_output.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        "ffmpeg",
        "-i",
        str(video_path),
        "-vn",
        "-acodec",
        "pcm_s16le",
        "-ar",
        "16000",
        "-ac",
        "1",
        "-y",
        str(audio_output),
    ]

    print(f"Extracting audio from video...")
    print(f"Input: {video_path}")
    print(f"Output: {audio_output}")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"Audio extraction complete: {audio_output}")
        return str(audio_output)
    except subprocess.CalledProcessError as e:
        print(f"ffmpeg execution failed: {e.stderr}")
        raise RuntimeError(f"Audio extraction failed: {e.stderr}")
    except FileNotFoundError:
        raise RuntimeError(
            "ffmpeg not installed, please install first: apt install ffmpeg or brew install ffmpeg"
        )


def main():
    parser = argparse.ArgumentParser(
        description="Extract 16kHz mono wav from video (ffmpeg)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Default: cleans up generated .wav before exit to avoid disk buildup; use --keep-audio to retain.",
    )
    parser.add_argument("video_path", help="Video file path")
    parser.add_argument(
        "audio_output",
        nargs="?",
        default=None,
        help="Output audio path (optional, defaults to .wav in same directory as video)",
    )
    parser.add_argument(
        "--keep-audio",
        action="store_true",
        help="Keep extracted .wav file (default: deleted before exit to save disk space)",
    )
    args = parser.parse_args()

    try:
        output = extract_audio(args.video_path, args.audio_output)
        if args.keep_audio:
            print(output)
        else:
            print(f"{output} (temp wav cleaned up; use --keep-audio to retain)")
            Path(output).unlink(missing_ok=True)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
PYEOF

echo "scripts/extract_audio.py done"

# scripts/transcribe_with_diarization.py
cat > scripts/transcribe_with_diarization.py << 'PYEOF'
#!/usr/bin/env python3
"""
Transcription using qwen-asr with simple speaker diarization
"""

import os
import sys
import json
from datetime import timedelta
from pathlib import Path

# Set environment variable to avoid CUDA version check issues
os.environ["TORCHAUDIO_DISABLE_VERSION_CHECK"] = "1"

from qwen_asr import Qwen3ASRModel
import torch


def format_timestamp(seconds: float) -> str:
    """Format timestamp as HH:MM:SS"""
    td = timedelta(seconds=seconds)
    return str(td).split(".")[0]


def transcribe_audio(audio_path: str, output_path: str):
    """Transcribe audio using qwen-asr"""
    print(f"Loading model...")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = Qwen3ASRModel.from_pretrained("Qwen/Qwen3-ASR-1.7B")
    model.model = model.model.to(device)

    print(f"Transcribing {audio_path}...")
    result = model.transcribe(audio_path, return_time_stamps=False, language="Chinese")

    print(f"Saving results to {output_path}...")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"Audio file: {audio_path}\n")
        f.write(f"Language: {result[0].language}\n")
        f.write("=" * 50 + "\n\n")

        if result[0].time_stamps:
            # Has timestamp info, output by time segments
            ts = result[0].time_stamps
            for i, (start, end, text) in enumerate(
                zip(ts.start_time, ts.end_time, ts.text_segments)
            ):
                f.write(f"[{format_timestamp(start)} - {format_timestamp(end)}]\n")
                f.write(f"{text}\n\n")
        else:
            # No timestamps, output text directly
            f.write(result[0].text)

    print(f"Transcription complete!")
    return result


def main():
    if len(sys.argv) < 2:
        print("Usage: python transcribe_with_diarization.py <audio_file> [output_file]")
        sys.exit(1)

    audio_path = sys.argv[1]
    output_path = (
        sys.argv[2]
        if len(sys.argv) > 2
        else audio_path.replace(".wav", "_transcript.txt")
    )

    transcribe_audio(audio_path, output_path)


if __name__ == "__main__":
    main()
PYEOF

echo "scripts/transcribe_with_diarization.py done"

# scripts/transcribe_diarize_fw.py
cat > scripts/transcribe_diarize_fw.py << 'PYEOF'
#!/usr/bin/env python3
"""
Transcription using faster-whisper with simple speaker diarization based on audio energy and speaker change detection
"""

import os
import sys
import json
from datetime import timedelta
from pathlib import Path
import numpy as np

os.environ["TORCHAUDIO_DISABLE_VERSION_CHECK"] = "1"

from faster_whisper import WhisperModel
import librosa


def format_timestamp(seconds: float) -> str:
    """Format timestamp as HH:MM:SS"""
    td = timedelta(seconds=seconds)
    return str(td).split(".")[0]


def detect_speaker_changes(
    audio_path: str, segment_duration: float = 0.5, threshold: float = 0.3
):
    """
    Detect potential speaker change points based on audio energy variation
    Returns list of time points where speaker changes occur
    """
    audio, sr = librosa.load(audio_path, sr=16000)

    # Compute short-time energy (vectorized: einsum sums squares per frame in a single C kernel pass)
    # Original per-window Python loop cost grew linearly with frame count (default 1h audio approx 7200 frames, ~3.8x speedup,
    # larger gap with smaller hops). Semantic equivalence preserved: for real signals |x|^2 == x^2,
    # full frames reshaped to view zero-copy, tail shorter than one frame summed separately, results match original loop.
    hop_length = int(sr * segment_duration)
    total = len(audio)
    n_full = total // hop_length
    if n_full > 0:
        frames = audio[: n_full * hop_length].reshape(n_full, hop_length)
        energy = np.einsum("ij,ij->i", frames, frames)
    else:
        energy = np.zeros(0, dtype=audio.dtype)
    remainder = total - n_full * hop_length
    if remainder > 0:
        tail = np.square(audio[n_full * hop_length :]).sum()
        energy = np.append(energy, tail) if n_full > 0 else np.array([tail])
    energy = energy.astype(audio.dtype, copy=False)

    # Compute energy change rate
    if len(energy) > 1:
        energy_change = np.abs(np.diff(energy))
        energy_change = energy_change / (np.max(energy_change) + 1e-10)

        # Detect significant change points
        change_points = []
        for i, change in enumerate(energy_change):
            if change > threshold:
                time_point = (i + 1) * segment_duration
                change_points.append(time_point)

        return change_points
    return []


def transcribe_with_diarization(
    audio_path: str, output_path: str, num_speakers: int = 3
):
    """
    Transcribe using faster-whisper with speaker diarization attempt
    """
    print(f"Loading faster-whisper model...")
    # Device auto-adapt: falls back to cpu without GPU (avoids RuntimeError), compute_type adjusted accordingly
    import torch

    device = "cuda" if torch.cuda.is_available() else "cpu"
    compute_type = "float16" if device == "cuda" else "int8"
    print(f"Using device={device}, compute_type={compute_type}")
    model = WhisperModel("large-v3", device=device, compute_type=compute_type)

    print(f"Transcribing {audio_path}...")
    segments, info = model.transcribe(
        audio_path, language="zh", word_timestamps=True, vad_filter=True
    )

    print(f"Detected language: {info.language} (probability: {info.language_probability:.2f})")

    # Detect potential speaker change points
    print(f"Analyzing audio energy changes...")
    change_points = detect_speaker_changes(audio_path)

    # Assign speakers based on time and energy changes
    current_speaker = 1
    last_change_time = 0
    speaker_segments = []

    for segment in segments:
        start = segment.start
        end = segment.end
        text = segment.text.strip()

        # Check for energy change points before this segment starts
        for cp in change_points:
            if cp > last_change_time and cp < start:
                current_speaker = (current_speaker % num_speakers) + 1
                last_change_time = cp
                break

        speaker_segments.append(
            {
                "speaker": f"Speaker{current_speaker}",
                "start": start,
                "end": end,
                "text": text,
            }
        )

    # Save results
    print(f"Saving results to {output_path}...")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"Audio file: {audio_path}\n")
        f.write(f"Language: {info.language}\n")
        f.write(f"Total duration: {format_timestamp(info.duration)}\n")
        f.write("=" * 50 + "\n\n")

        for seg in speaker_segments:
            f.write(
                f"[{seg['speaker']}] {format_timestamp(seg['start'])} - {format_timestamp(seg['end'])}\n"
            )
            f.write(f"{seg['text']}\n\n")

    # Save JSON format
    json_path = output_path.replace(".txt", ".json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(speaker_segments, f, ensure_ascii=False, indent=2)

    print(f"Transcription complete! {len(speaker_segments)} segments total")
    return speaker_segments


def main():
    if len(sys.argv) < 2:
        print(
            "Usage: python transcribe_diarize_fw.py <audio_file> [output_file] [num_speakers]"
        )
        sys.exit(1)

    audio_path = sys.argv[1]
    output_path = (
        sys.argv[2]
        if len(sys.argv) > 2
        else audio_path.replace(".wav", "_diarized.txt")
    )
    num_speakers = int(sys.argv[3]) if len(sys.argv) > 3 else 3

    transcribe_with_diarization(audio_path, output_path, num_speakers)


if __name__ == "__main__":
    main()
PYEOF

echo "scripts/transcribe_diarize_fw.py done"
echo "All core files translated!"
