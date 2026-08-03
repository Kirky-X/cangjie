#!/usr/bin/env python3
"""
Transcription using qwen-asr with simple speaker diarization
"""

import os
import sys
import json
import argparse
import logging
from pathlib import Path

# Set environment variable to avoid CUDA version check issues
os.environ["TORCHAUDIO_DISABLE_VERSION_CHECK"] = "1"

from utils import format_timestamp, validate_audio_file, ensure_output_dir

logger = logging.getLogger(__name__)


def transcribe_audio(audio_path: str, output_path: str):
    """Transcribe audio using qwen-asr"""
    audio_path = str(validate_audio_file(audio_path))
    output_path = str(ensure_output_dir(output_path))

    print(f"Loading model...")
    import torch
    from qwen_asr import Qwen3ASRModel

    try:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model = Qwen3ASRModel.from_pretrained("Qwen/Qwen3-ASR-1.7B")
        model.model = model.model.to(device)
    except Exception as e:
        print(f"Error: Failed to load model: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Transcribing {audio_path}...")
    try:
        result = model.transcribe(audio_path, return_time_stamps=False, language="Chinese")
    except Exception as e:
        print(f"Error: Transcription failed: {e}", file=sys.stderr)
        sys.exit(1)

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
    parser = argparse.ArgumentParser(
        description="Transcribe audio using qwen-asr (Chinese-optimized)",
    )
    parser.add_argument("audio_path", help="Audio file path")
    parser.add_argument(
        "output_path",
        nargs="?",
        default=None,
        help="Output transcript path (default: <audio>_transcript.txt)",
    )

    args = parser.parse_args()

    audio_path = args.audio_path
    output_path = args.output_path or str(
        Path(audio_path).with_suffix("")
    ) + "_transcript.txt"

    transcribe_audio(audio_path, output_path)


if __name__ == "__main__":
    main()
