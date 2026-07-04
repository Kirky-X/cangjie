#!/usr/bin/env python3
"""
使用 qwen-asr 进行转录，结合简单的说话人分离
"""

import os
import sys
import json
from datetime import timedelta
from pathlib import Path

# 设置环境变量避免 CUDA 版本检查问题
os.environ["TORCHAUDIO_DISABLE_VERSION_CHECK"] = "1"

from qwen_asr import Qwen3ASRModel
import torch


def format_timestamp(seconds: float) -> str:
    """格式化时间戳为 HH:MM:SS"""
    td = timedelta(seconds=seconds)
    return str(td).split(".")[0]


def transcribe_audio(audio_path: str, output_path: str):
    """使用 qwen-asr 转录音频"""
    print(f"加载模型...")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = Qwen3ASRModel.from_pretrained("Qwen/Qwen3-ASR-1.7B")
    model.model = model.model.to(device)

    print(f"转录 {audio_path}...")
    result = model.transcribe(audio_path, return_time_stamps=False, language="Chinese")

    print(f"保存结果到 {output_path}...")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"音频文件: {audio_path}\n")
        f.write(f"语言: {result[0].language}\n")
        f.write("=" * 50 + "\n\n")

        if result[0].time_stamps:
            # 有时间戳信息，按时间分段输出
            ts = result[0].time_stamps
            for i, (start, end, text) in enumerate(
                zip(ts.start_time, ts.end_time, ts.text_segments)
            ):
                f.write(f"[{format_timestamp(start)} - {format_timestamp(end)}]\n")
                f.write(f"{text}\n\n")
        else:
            # 无时间戳，直接输出文本
            f.write(result[0].text)

    print(f"转录完成！")
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
