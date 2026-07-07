#!/usr/bin/env python3
"""
cangjie - 音频转录工具统一入口
一键调度 extract-audio / transcribe-diarize / transcribe-qwen，免记三条命令。

子命令:
    extract-audio        从视频提取 16kHz 单声道 wav (ffmpeg)
    transcribe-diarize   faster-whisper 转录 + 能量说话人分离
    transcribe-qwen      qwen-asr 转录（中文优化）

典型用法:
    python3 cangjie.py extract-audio input.mp4 --keep-audio
    python3 cangjie.py transcribe-diarize input.wav output.txt 3
    python3 cangjie.py transcribe-qwen input.wav output.txt
"""

import argparse
import sys
from pathlib import Path

# 子脚本与本文件同目录；加入 sys.path 以便延迟 import 能定位到它们
_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))


def _default_output(audio_path: str, suffix: str) -> str:
    """根据音频路径推导默认输出路径（与各子脚本原 main 行为一致）。"""
    return audio_path.replace(".wav", suffix)


def cmd_extract_audio(args) -> int:
    import extract_audio as _extract_audio

    output = _extract_audio.extract_audio(args.video_path, args.audio_output)
    if args.keep_audio:
        print(output)
    else:
        print(f"{output} (已清理临时 wav；如需保留请加 --keep-audio)")
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
        description="音频转录工具统一入口（提取音频 → 转录 + 说话人分离）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "子命令示例:\n"
            "  cangjie.py extract-audio input.mp4 --keep-audio\n"
            "  cangjie.py transcribe-diarize input.wav out.txt 3\n"
            "  cangjie.py transcribe-qwen input.wav out.txt\n"
        ),
    )
    sub = parser.add_subparsers(dest="command", required=True, metavar="<command>")

    p_extract = sub.add_parser(
        "extract-audio", help="从视频提取 16kHz 单声道 wav (ffmpeg)"
    )
    p_extract.add_argument("video_path", help="视频文件路径")
    p_extract.add_argument(
        "audio_output", nargs="?", default=None, help="输出 wav 路径（可选）"
    )
    p_extract.add_argument(
        "--keep-audio",
        action="store_true",
        help="保留提取的 wav（默认在退出前清理以避免磁盘堆积）",
    )
    p_extract.set_defaults(func=cmd_extract_audio)

    p_fw = sub.add_parser(
        "transcribe-diarize", help="faster-whisper 转录 + 能量说话人分离"
    )
    p_fw.add_argument("audio_path", help="音频文件路径")
    p_fw.add_argument("output", nargs="?", default=None, help="输出 .txt 路径（可选）")
    p_fw.add_argument(
        "num_speakers", nargs="?", type=int, default=3, help="说话人数量（默认 3）"
    )
    p_fw.set_defaults(func=cmd_transcribe_diarize)

    p_qwen = sub.add_parser("transcribe-qwen", help="qwen-asr 转录（中文优化）")
    p_qwen.add_argument("audio_path", help="音频文件路径")
    p_qwen.add_argument(
        "output", nargs="?", default=None, help="输出 .txt 路径（可选）"
    )
    p_qwen.set_defaults(func=cmd_transcribe_qwen)

    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except KeyboardInterrupt:
        print("已中断", file=sys.stderr)
        return 130
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
