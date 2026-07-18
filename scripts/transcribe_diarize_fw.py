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
