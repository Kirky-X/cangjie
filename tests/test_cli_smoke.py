#!/usr/bin/env python3
"""四个 CLI 入口的子进程冒烟测试：--help 可用、缺文件路径退出码正确。

均在子进程中运行真实脚本，验证模块可导入（含函数内延迟导入前的顶层）与
argparse/校验行为；不触发任何模型下载或 ffmpeg 转码。
"""
import os
import subprocess
import sys
import unittest

SCRIPTS_DIR = os.path.join(os.path.dirname(__file__), "..", "scripts")

CANGJIE = os.path.join(SCRIPTS_DIR, "cangjie.py")
EXTRACT = os.path.join(SCRIPTS_DIR, "extract_audio.py")
FW = os.path.join(SCRIPTS_DIR, "transcribe_diarize_fw.py")
QWEN = os.path.join(SCRIPTS_DIR, "transcribe_with_diarization.py")


def run_cli(*argv):
    return subprocess.run(
        [sys.executable, "-B", *argv],
        capture_output=True,
        text=True,
        timeout=60,
    )


class TestHelpSmoke(unittest.TestCase):
    def test_cangjie_help_lists_subcommands(self):
        r = run_cli(CANGJIE, "--help")
        self.assertEqual(r.returncode, 0)
        for sub in ("extract-audio", "transcribe-diarize", "transcribe-qwen", "pipeline"):
            self.assertIn(sub, r.stdout)

    def test_cangjie_subcommand_help(self):
        for sub in ("extract-audio", "transcribe-diarize", "transcribe-qwen", "pipeline"):
            r = run_cli(CANGJIE, sub, "--help")
            self.assertEqual(r.returncode, 0, f"{sub} --help 失败: {r.stderr}")

    def test_extract_audio_help(self):
        r = run_cli(EXTRACT, "--help")
        self.assertEqual(r.returncode, 0)
        self.assertIn("video_path", r.stdout)

    def test_transcribe_fw_help(self):
        r = run_cli(FW, "--help")
        self.assertEqual(r.returncode, 0)
        self.assertIn("audio_path", r.stdout)

    def test_transcribe_qwen_help(self):
        r = run_cli(QWEN, "--help")
        self.assertEqual(r.returncode, 0)
        self.assertIn("audio_path", r.stdout)


class TestExitCodes(unittest.TestCase):
    def test_cangjie_without_command_exits_2(self):
        r = run_cli(CANGJIE)
        self.assertEqual(r.returncode, 2)

    def test_cangjie_missing_video_exits_1(self):
        r = run_cli(CANGJIE, "extract-audio", "/nonexistent/video.mp4")
        self.assertEqual(r.returncode, 1)
        self.assertIn("not found", r.stderr)

    def test_cangjie_missing_audio_exits_1(self):
        r = run_cli(CANGJIE, "transcribe-diarize", "/nonexistent/audio.wav")
        self.assertEqual(r.returncode, 1)
        self.assertIn("not found", r.stderr)

    def test_extract_audio_missing_video_exits_1(self):
        r = run_cli(EXTRACT, "/nonexistent/video.mp4")
        self.assertEqual(r.returncode, 1)
        self.assertIn("Error", r.stderr)

    def test_transcribe_fw_missing_audio_exits_1(self):
        # 校验发生在 faster-whisper 导入之前，缺文件路径不触发模型加载
        r = run_cli(FW, "/nonexistent/audio.wav")
        self.assertEqual(r.returncode, 1)
        self.assertIn("not found", r.stderr)

    def test_transcribe_qwen_missing_audio_exits_1(self):
        r = run_cli(QWEN, "/nonexistent/audio.wav")
        self.assertEqual(r.returncode, 1)
        self.assertIn("not found", r.stderr)


if __name__ == "__main__":
    unittest.main()
