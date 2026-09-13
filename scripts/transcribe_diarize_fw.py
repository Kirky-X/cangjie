#!/usr/bin/env python3
"""
Transcription using faster-whisper with approximate speaker segmentation based on
audio energy change points.

IMPORTANT: This is NOT true speaker diarization. "SpeakerN" labels are derived from
energy-change heuristics and may misattribute utterances. Output files carry an
explicit disclaimer; downstream summaries must not present speaker attribution as fact.
"""

import os
import sys
import json
import argparse
import logging
from pathlib import Path

os.environ["TORCHAUDIO_DISABLE_VERSION_CHECK"] = "1"

from utils import format_timestamp, validate_audio_file, ensure_output_dir

logger = logging.getLogger(__name__)


def detect_speaker_changes(
    audio_path: str, segment_duration: float = 0.5, threshold: float = 0.3
):
    """
    Detect potential speaker change points based on audio energy variation.
    NOTE: This is energy-based approximation, not true speaker diarization.
    Returns list of time points where speaker changes may occur.
    """
    import librosa
    import numpy as np

    audio, sr = librosa.load(audio_path, sr=16000)

    # Compute short-time energy (vectorized: einsum sums squares per frame in a single C kernel pass)
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

        change_points = []
        for i, change in enumerate(energy_change):
            if change > threshold:
                time_point = (i + 1) * segment_duration
                change_points.append(time_point)

        return change_points
    return []


def transcribe_with_diarization(
    audio_path: str,
    output_path: str,
    num_speakers: int = 3,
    language: str = "zh",
):
    """
    Transcribe using faster-whisper with speaker diarization attempt.

    Args:
        audio_path: Path to audio file
        output_path: Path for output transcript file
        num_speakers: Expected number of speakers
        language: Language code (default: "zh"). Use None for auto-detection.
    """
    audio_path = str(validate_audio_file(audio_path))
    output_path = str(ensure_output_dir(output_path))

    from faster_whisper import WhisperModel

    print(f"Loading faster-whisper model...")
    import torch

    # Pre-initialize before try so the except branch never hits an undefined `device`
    device = "cpu"
    compute_type = "int8"
    try:
        if torch.cuda.is_available():
            device = "cuda"
            compute_type = "float16"
        print(f"Using device={device}, compute_type={compute_type}")
        model = WhisperModel("large-v3", device=device, compute_type=compute_type)
    except Exception as e:
        print(f"Error: Failed to load model: {e}", file=sys.stderr)
        if device == "cuda":
            print("Falling back to CPU...", file=sys.stderr)
            device = "cpu"
            compute_type = "int8"
            model = WhisperModel("large-v3", device=device, compute_type=compute_type)
        else:
            sys.exit(1)

    print(f"Transcribing {audio_path}...")
    try:
        segments, info = model.transcribe(
            audio_path,
            language=language if language else None,
            word_timestamps=True,
            vad_filter=True,
        )
    except Exception as e:
        print(f"Error: Transcription failed: {e}", file=sys.stderr)
        sys.exit(1)

    detected_lang = info.language
    print(f"Detected language: {detected_lang} (probability: {info.language_probability:.2f})")

    # Detect potential speaker change points
    print(f"Analyzing audio energy changes...")
    change_points = detect_speaker_changes(audio_path)

    # Assign speakers based on time and energy changes.
    # If no energy change points were detected, keep a single speaker label —
    # never rotate Speaker1/2/3 for what is likely a single-speaker recording.
    current_speaker = 1
    last_change_time = 0
    speaker_segments = []
    processed_duration = 0.0

    for segment in segments:
        start = segment.start
        end = segment.end
        text = segment.text.strip()

        # Check for energy change points before this segment starts
        if change_points:
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
        processed_duration = end

        # Progress feedback
        if info.duration > 0:
            pct = min(processed_duration / info.duration * 100, 100)
            print(
                f"\rProgress: {format_timestamp(processed_duration)}/{format_timestamp(info.duration)} ({pct:.0f}%)",
                end="",
                flush=True,
            )

    print()  # newline after progress

    # Mandatory disclaimer: labels come from energy-based segmentation, not voiceprint ID
    disclaimer = (
        "说话人标签为基于能量变化的近似分段，非真实声纹识别，仅供对话轮次参考"
        "（检测到 " + str(len(change_points)) + " 个能量突变点），"
        "不应作为说话人归属的确定性结论。"
    )
    if not change_points:
        print("No energy change points detected: keeping a single speaker label (no rotation).")

    # Save results
    print(f"Saving results to {output_path}...")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"Audio file: {audio_path}\n")
        f.write(f"Language: {detected_lang}\n")
        f.write(f"Total duration: {format_timestamp(info.duration)}\n")
        f.write(f"Disclaimer: {disclaimer}\n")
        f.write("=" * 50 + "\n\n")

        for seg in speaker_segments:
            f.write(
                f"[{seg['speaker']}] {format_timestamp(seg['start'])} - {format_timestamp(seg['end'])}\n"
            )
            f.write(f"{seg['text']}\n\n")

    # Save JSON format — use Path.with_suffix for robust path derivation.
    # Wrapped in an object so the disclaimer travels with the data (was a bare array).
    json_path = str(Path(output_path).with_suffix(".json"))
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "disclaimer": disclaimer,
                "speaker_labels_are_approximate": True,
                "audio_file": audio_path,
                "language": detected_lang,
                "total_duration": format_timestamp(info.duration),
                "segments": speaker_segments,
            },
            f,
            ensure_ascii=False,
            indent=2,
        )

    print(f"Transcription complete! {len(speaker_segments)} segments total")
    return speaker_segments


def main():
    parser = argparse.ArgumentParser(
        description="Transcribe audio with faster-whisper + energy-based speaker diarization",
    )
    parser.add_argument("audio_path", help="Audio file path")
    parser.add_argument(
        "output_path",
        nargs="?",
        default=None,
        help="Output transcript path (default: <audio>_diarized.txt)",
    )
    parser.add_argument(
        "--num-speakers",
        type=int,
        default=3,
        help="Expected number of speakers (default: 3)",
    )
    parser.add_argument(
        "--language",
        default="zh",
        help='Language code, e.g. "zh", "en". Use "auto" for auto-detection (default: zh)',
    )

    args = parser.parse_args()

    audio_path = args.audio_path
    output_path = args.output_path or str(
        Path(audio_path).with_suffix("") 
    ) + "_diarized.txt"
    language = None if args.language.lower() == "auto" else args.language

    transcribe_with_diarization(audio_path, output_path, args.num_speakers, language)


if __name__ == "__main__":
    main()
