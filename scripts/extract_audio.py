#!/usr/bin/env python3
"""
视频转音频提取脚本
使用 ffmpeg 从视频文件中提取音频轨道

用法:
    python3 extract_audio.py <video_path> [audio_output_path] [--keep-audio]

参数:
    video_path: 视频文件路径 (支持 mp4, mkv, avi, mov, webm 等格式)
    audio_output_path: 输出音频路径 (可选, 默认为 video_path 同目录下的 .wav 文件)

选项:
    --keep-audio: 保留提取的 .wav 文件 (默认删除以避免磁盘堆积, 1h 音频 ≈ 150MB)
"""

import argparse
import subprocess
import sys
from pathlib import Path


def extract_audio(video_path: str, audio_output: str = None) -> str:
    """
    从视频中提取音频

    Args:
        video_path: 视频文件路径
        audio_output: 输出音频路径（可选）

    Returns:
        输出音频文件路径
    """
    video_path = Path(video_path).resolve()

    if not video_path.exists():
        raise FileNotFoundError(f"视频文件不存在: {video_path}")

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

    print(f"正在从视频提取音频...")
    print(f"输入: {video_path}")
    print(f"输出: {audio_output}")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"音频提取完成: {audio_output}")
        return str(audio_output)
    except subprocess.CalledProcessError as e:
        print(f"ffmpeg 执行失败: {e.stderr}")
        raise RuntimeError(f"音频提取失败: {e.stderr}")
    except FileNotFoundError:
        raise RuntimeError(
            "ffmpeg 未安装，请先安装: apt install ffmpeg 或 brew install ffmpeg"
        )


def main():
    parser = argparse.ArgumentParser(
        description="从视频提取 16kHz 单声道 wav (ffmpeg)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="默认在退出前清理生成的 .wav 以避免磁盘堆积；如需保留请加 --keep-audio。",
    )
    parser.add_argument("video_path", help="视频文件路径")
    parser.add_argument(
        "audio_output",
        nargs="?",
        default=None,
        help="输出音频路径（可选，默认为视频同目录下的 .wav）",
    )
    parser.add_argument(
        "--keep-audio",
        action="store_true",
        help="保留提取的 .wav 文件（默认在退出前删除以节省磁盘）",
    )
    args = parser.parse_args()

    try:
        output = extract_audio(args.video_path, args.audio_output)
        if args.keep_audio:
            print(output)
        else:
            print(f"{output} (已清理临时 wav；如需保留请加 --keep-audio)")
            Path(output).unlink(missing_ok=True)
    except Exception as e:
        print(f"错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
