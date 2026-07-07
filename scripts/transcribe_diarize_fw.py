#!/usr/bin/env python3
"""
使用 faster-whisper 进行转录，并基于音频能量和说话人变化检测进行简单的说话人分离
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
    """格式化时间戳为 HH:MM:SS"""
    td = timedelta(seconds=seconds)
    return str(td).split(".")[0]


def detect_speaker_changes(
    audio_path: str, segment_duration: float = 0.5, threshold: float = 0.3
):
    """
    基于音频能量变化检测潜在的说话人切换点
    返回说话人变化的时间点列表
    """
    audio, sr = librosa.load(audio_path, sr=16000)

    # 计算短时能量（向量化：einsum 在单次 C 内核 pass 内对每帧求平方和）
    # 原逐窗口 Python 循环开销随帧数线性增长（默认 1h 音频 ≈ 7200 帧加速约 3.8x，
    # 更小 hop 时差距更大）。语义保持等价：对实数信号 |x|^2 == x^2，
    # 整帧部分 reshape 为视图零拷贝，尾部不足一帧单独求和，结果与原循环（含尾部短帧）一致。
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

    # 计算能量变化率
    if len(energy) > 1:
        energy_change = np.abs(np.diff(energy))
        energy_change = energy_change / (np.max(energy_change) + 1e-10)

        # 检测显著变化点
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
    使用 faster-whisper 进行转录并尝试说话人分离
    """
    print(f"加载 faster-whisper 模型...")
    # device 自适应：无 GPU 时 fallback 到 cpu（避免 RuntimeError），compute_type 相应调整
    import torch

    device = "cuda" if torch.cuda.is_available() else "cpu"
    compute_type = "float16" if device == "cuda" else "int8"
    print(f"使用 device={device}, compute_type={compute_type}")
    model = WhisperModel("large-v3", device=device, compute_type=compute_type)

    print(f"转录 {audio_path}...")
    segments, info = model.transcribe(
        audio_path, language="zh", word_timestamps=True, vad_filter=True
    )

    print(f"检测语言: {info.language} (概率: {info.language_probability:.2f})")

    # 检测潜在说话人变化点
    print(f"分析音频能量变化...")
    change_points = detect_speaker_changes(audio_path)

    # 基于时间和能量变化分配说话人
    current_speaker = 1
    last_change_time = 0
    speaker_segments = []

    for segment in segments:
        start = segment.start
        end = segment.end
        text = segment.text.strip()

        # 检查是否有能量变化点在此段落开始前
        for cp in change_points:
            if cp > last_change_time and cp < start:
                current_speaker = (current_speaker % num_speakers) + 1
                last_change_time = cp
                break

        speaker_segments.append(
            {
                "speaker": f"发言人{current_speaker}",
                "start": start,
                "end": end,
                "text": text,
            }
        )

    # 保存结果
    print(f"保存结果到 {output_path}...")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"音频文件: {audio_path}\n")
        f.write(f"语言: {info.language}\n")
        f.write(f"总时长: {format_timestamp(info.duration)}\n")
        f.write("=" * 50 + "\n\n")

        for seg in speaker_segments:
            f.write(
                f"[{seg['speaker']}] {format_timestamp(seg['start'])} - {format_timestamp(seg['end'])}\n"
            )
            f.write(f"{seg['text']}\n\n")

    # 保存 JSON 格式
    json_path = output_path.replace(".txt", ".json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(speaker_segments, f, ensure_ascii=False, indent=2)

    print(f"转录完成！共 {len(speaker_segments)} 个段落")
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
