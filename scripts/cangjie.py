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
        description="Unified entry point for audio transcription tools (extract audio → transcription + speaker diarization)",
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
