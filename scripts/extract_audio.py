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
    --keep-audio: Keep extracted .wav file (default: deleted to avoid disk buildup, 1h audio ≈ 150MB)
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
