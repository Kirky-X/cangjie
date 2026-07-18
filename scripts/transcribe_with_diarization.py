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
