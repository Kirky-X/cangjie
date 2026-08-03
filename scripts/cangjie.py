#!/usr/bin/env python3
"""
cangjie - Unified entry point for audio transcription tools
One-click dispatch to extract-audio / transcribe-diarize / transcribe-qwen / pipeline.

Subcommands:
    extract-audio        Extract 16kHz mono wav from video (ffmpeg)
    transcribe-diarize   faster-whisper transcription + energy-based speaker diarization
    transcribe-qwen      qwen-asr transcription (Chinese-optimized)
    pipeline             One-shot: extract audio from video → transcribe → output transcript

Typical usage:
    python3 cangjie.py extract-audio input.mp4 --keep-audio
    python3 cangjie.py transcribe-diarize input.wav output.txt --num-speakers 3
    python3 cangjie.py transcribe-qwen input.wav output.txt
    python3 cangjie.py pipeline input.mp4 --engine faster-whisper --num-speakers 3
"""

import argparse
import sys
from pathlib import Path

# Sub-scripts are in the same directory as this file; add to sys.path for delayed import
_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))


def _validate_video(video_path: str) -> str:
    """Validate video file exists."""
    p = Path(video_path).resolve()
    if not p.exists():
        print(f"Error: Video file not found: {p}", file=sys.stderr)
        sys.exit(1)
    if not p.is_file():
        print(f"Error: Not a file: {p}", file=sys.stderr)
        sys.exit(1)
    return str(p)


def _validate_audio(audio_path: str) -> str:
    """Validate audio file exists."""
    p = Path(audio_path).resolve()
    if not p.exists():
        print(f"Error: Audio file not found: {p}", file=sys.stderr)
        sys.exit(1)
    if not p.is_file():
        print(f"Error: Not a file: {p}", file=sys.stderr)
        sys.exit(1)
    return str(p)


def cmd_extract_audio(args) -> int:
    import extract_audio as _extract_audio

    _validate_video(args.video_path)
    output = _extract_audio.extract_audio(args.video_path, args.audio_output)
    if args.keep_audio:
        print(output)
    else:
        print(f"{output} (temp wav cleaned up; use --keep-audio to retain)")
        Path(output).unlink(missing_ok=True)
    return 0


def cmd_transcribe_diarize(args) -> int:
    import transcribe_diarize_fw as _fw

    _validate_audio(args.audio_path)
    output = args.output or str(Path(args.audio_path).with_suffix("")) + "_diarized.txt"
    language = None if args.language.lower() == "auto" else args.language
    _fw.transcribe_with_diarization(args.audio_path, output, args.num_speakers, language)
    return 0


def cmd_transcribe_qwen(args) -> int:
    import transcribe_with_diarization as _qwen

    _validate_audio(args.audio_path)
    output = args.output or str(Path(args.audio_path).with_suffix("")) + "_transcript.txt"
    _qwen.transcribe_audio(args.audio_path, output)
    return 0


def cmd_pipeline(args) -> int:
    """One-shot pipeline: extract audio from video → transcribe → output transcript."""
    import extract_audio as _extract_audio

    video_path = _validate_video(args.video_path)

    # Step 1: Extract audio (always keep for transcription)
    print("=" * 50)
    print("Step 1/2: Extracting audio from video...")
    print("=" * 50)
    wav_path = str(Path(video_path).with_suffix(".wav"))
    if args.audio_output:
        wav_path = args.audio_output
    extracted = _extract_audio.extract_audio(video_path, wav_path)

    try:
        # Step 2: Transcribe
        print("=" * 50)
        print("Step 2/2: Transcribing audio...")
        print("=" * 50)
        output = args.output or str(Path(video_path).with_suffix("")) + "_diarized.txt"

        if args.engine == "faster-whisper":
            import transcribe_diarize_fw as _fw
            language = None if args.language.lower() == "auto" else args.language
            _fw.transcribe_with_diarization(extracted, output, args.num_speakers, language)
        elif args.engine == "qwen-asr":
            import transcribe_with_diarization as _qwen
            _qwen.transcribe_audio(extracted, output)
        else:
            print(f"Error: Unknown engine '{args.engine}'", file=sys.stderr)
            return 1
    finally:
        # Clean up wav unless --keep-audio
        if not args.keep_audio:
            Path(extracted).unlink(missing_ok=True)
            print(f"Cleaned up temporary wav: {extracted}")

    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cangjie",
        description="Unified entry point for audio transcription tools (extract audio → transcription + speaker diarization)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Subcommand examples:\n"
            "  cangjie.py extract-audio input.mp4 --keep-audio\n"
            "  cangjie.py transcribe-diarize input.wav out.txt --num-speakers 3\n"
            "  cangjie.py transcribe-qwen input.wav out.txt\n"
            "  cangjie.py pipeline input.mp4 --engine faster-whisper\n"
        ),
    )
    sub = parser.add_subparsers(dest="command", required=True, metavar="<command>")

    # extract-audio
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

    # transcribe-diarize
    p_fw = sub.add_parser(
        "transcribe-diarize", help="faster-whisper transcription + energy-based speaker diarization"
    )
    p_fw.add_argument("audio_path", help="Audio file path")
    p_fw.add_argument("output", nargs="?", default=None, help="Output .txt path (optional)")
    p_fw.add_argument(
        "--num-speakers", type=int, default=3, help="Number of speakers (default: 3)"
    )
    p_fw.add_argument(
        "--language", default="zh",
        help='Language code, e.g. "zh", "en". Use "auto" for auto-detection (default: zh)',
    )
    p_fw.set_defaults(func=cmd_transcribe_diarize)

    # transcribe-qwen
    p_qwen = sub.add_parser("transcribe-qwen", help="qwen-asr transcription (Chinese-optimized)")
    p_qwen.add_argument("audio_path", help="Audio file path")
    p_qwen.add_argument(
        "output", nargs="?", default=None, help="Output .txt path (optional)"
    )
    p_qwen.set_defaults(func=cmd_transcribe_qwen)

    # pipeline
    p_pipe = sub.add_parser(
        "pipeline", help="One-shot: extract audio from video → transcribe → output transcript"
    )
    p_pipe.add_argument("video_path", help="Video file path")
    p_pipe.add_argument("output", nargs="?", default=None, help="Output .txt path (optional)")
    p_pipe.add_argument(
        "audio_output", nargs="?", default=None, help="Intermediate wav path (optional)"
    )
    p_pipe.add_argument(
        "--engine",
        choices=["faster-whisper", "qwen-asr"],
        default="faster-whisper",
        help="Transcription engine (default: faster-whisper)",
    )
    p_pipe.add_argument(
        "--num-speakers", type=int, default=3, help="Number of speakers (default: 3)"
    )
    p_pipe.add_argument(
        "--language", default="zh",
        help='Language code for faster-whisper (default: zh). Use "auto" for auto-detection.',
    )
    p_pipe.add_argument(
        "--keep-audio",
        action="store_true",
        help="Keep intermediate wav file (default: cleaned up after transcription)",
    )
    p_pipe.set_defaults(func=cmd_pipeline)

    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except KeyboardInterrupt:
        print("Interrupted", file=sys.stderr)
        return 130
    except SystemExit:
        raise
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
