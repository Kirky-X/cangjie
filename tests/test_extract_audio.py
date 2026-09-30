#!/usr/bin/env python3
"""extract_audio.py 离线测试：mock 掉 ffmpeg 子进程，验证命令构造与错误分支。"""
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import extract_audio


class TestExtractAudio(unittest.TestCase):
    def test_missing_video_raises_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            extract_audio.extract_audio("/nonexistent/video.mp4")

    def test_default_output_is_wav_alongside_video(self):
        with tempfile.NamedTemporaryFile(suffix=".mp4") as f:
            with mock.patch.object(
                extract_audio.subprocess, "run", return_value=mock.Mock(returncode=0)
            ) as run:
                out = extract_audio.extract_audio(f.name)
        expected = str(Path(f.name).resolve().with_suffix(".wav"))
        self.assertEqual(out, expected)

    def test_ffmpeg_args_16k_mono_pcm(self):
        with tempfile.NamedTemporaryFile(suffix=".mp4") as f:
            with mock.patch.object(
                extract_audio.subprocess, "run", return_value=mock.Mock(returncode=0)
            ) as run:
                extract_audio.extract_audio(f.name, "/tmp/out.wav")
        cmd = run.call_args[0][0]
        self.assertEqual(cmd[0], "ffmpeg")
        self.assertIn("-vn", cmd)
        # 输出参数与目标格式逐项核对
        for flag, val in (("-acodec", "pcm_s16le"), ("-ar", "16000"), ("-ac", "1")):
            self.assertIn(flag, cmd)
            self.assertEqual(cmd[cmd.index(flag) + 1], val)
        self.assertEqual(cmd[-1], "/tmp/out.wav")
        self.assertIn("-y", cmd)

    def test_custom_output_creates_parent_dirs(self):
        with tempfile.NamedTemporaryFile(suffix=".mp4") as f:
            with tempfile.TemporaryDirectory() as d:
                out = os.path.join(d, "nested", "a.wav")
                with mock.patch.object(
                    extract_audio.subprocess, "run", return_value=mock.Mock(returncode=0)
                ):
                    result = extract_audio.extract_audio(f.name, out)
                self.assertTrue(Path(out).parent.is_dir())
                self.assertEqual(result, str(Path(out).resolve()))

    def test_ffmpeg_failure_wrapped_as_runtime_error(self):
        err = subprocess.CalledProcessError(1, "ffmpeg", stderr="bad input")
        with tempfile.NamedTemporaryFile(suffix=".mp4") as f:
            with mock.patch.object(extract_audio.subprocess, "run", side_effect=err):
                with self.assertRaises(RuntimeError) as ctx:
                    extract_audio.extract_audio(f.name)
        self.assertIn("Audio extraction failed", str(ctx.exception))

    def test_missing_ffmpeg_binary_gives_install_hint(self):
        with tempfile.NamedTemporaryFile(suffix=".mp4") as f:
            with mock.patch.object(
                extract_audio.subprocess, "run", side_effect=FileNotFoundError()
            ):
                with self.assertRaises(RuntimeError) as ctx:
                    extract_audio.extract_audio(f.name)
        self.assertIn("ffmpeg", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
