#!/usr/bin/env python3
"""cangjie 统一入口 CLI（cangjie.py）离线测试：参数解析、分发校验、错误处理。"""
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import cangjie


class TestBuildParser(unittest.TestCase):
    def test_help_lists_all_subcommands(self):
        text = cangjie.build_parser().format_help()
        for sub in ("extract-audio", "transcribe-diarize", "transcribe-qwen", "pipeline"):
            self.assertIn(sub, text)

    def test_extract_audio_defaults(self):
        args = cangjie.build_parser().parse_args(["extract-audio", "v.mp4"])
        self.assertEqual(args.command, "extract-audio")
        self.assertIsNone(args.audio_output)
        self.assertFalse(args.cleanup)

    def test_transcribe_diarize_defaults(self):
        args = cangjie.build_parser().parse_args(["transcribe-diarize", "a.wav"])
        self.assertEqual(args.num_speakers, 3)
        self.assertEqual(args.language, "zh")
        self.assertIsNone(args.output)

    def test_transcribe_diarize_custom(self):
        args = cangjie.build_parser().parse_args(
            ["transcribe-diarize", "a.wav", "out.txt", "--num-speakers", "2", "--language", "auto"]
        )
        self.assertEqual(args.output, "out.txt")
        self.assertEqual(args.num_speakers, 2)
        self.assertEqual(args.language, "auto")

    def test_transcribe_qwen_defaults(self):
        args = cangjie.build_parser().parse_args(["transcribe-qwen", "a.wav"])
        self.assertIsNone(args.output)

    def test_pipeline_positional_mapping(self):
        args = cangjie.build_parser().parse_args(
            ["pipeline", "v.mp4", "out.txt", "inter.wav",
             "--engine", "qwen-asr", "--cleanup", "--language", "en", "--num-speakers", "2"]
        )
        self.assertEqual(args.video_path, "v.mp4")
        self.assertEqual(args.output, "out.txt")
        self.assertEqual(args.audio_output, "inter.wav")
        self.assertEqual(args.engine, "qwen-asr")
        self.assertTrue(args.cleanup)
        self.assertEqual(args.language, "en")
        self.assertEqual(args.num_speakers, 2)

    def test_pipeline_engine_choices(self):
        for engine in ("faster-whisper", "qwen-asr"):
            args = cangjie.build_parser().parse_args(["pipeline", "v.mp4", "--engine", engine])
            self.assertEqual(args.engine, engine)

    def test_missing_command_rejected(self):
        with self.assertRaises(SystemExit) as ctx:
            cangjie.build_parser().parse_args([])
        self.assertEqual(ctx.exception.code, 2)

    def test_unknown_engine_rejected(self):
        with self.assertRaises(SystemExit) as ctx:
            cangjie.build_parser().parse_args(["pipeline", "v.mp4", "--engine", "whisper-x"])
        self.assertEqual(ctx.exception.code, 2)


class TestMainDispatch(unittest.TestCase):
    def test_missing_video_exits_1(self):
        with self.assertRaises(SystemExit) as ctx:
            cangjie.main(["extract-audio", "/nonexistent/video.mp4"])
        self.assertEqual(ctx.exception.code, 1)

    def test_missing_audio_exits_1(self):
        with self.assertRaises(SystemExit) as ctx:
            cangjie.main(["transcribe-diarize", "/nonexistent/audio.wav"])
        self.assertEqual(ctx.exception.code, 1)

    def test_unexpected_error_returns_1(self):
        # func 在 build_parser 时从模块全局取值，patch 模块属性即可拦截分发
        with mock.patch.object(
            cangjie, "cmd_extract_audio", side_effect=RuntimeError("boom")
        ):
            rc = cangjie.main(["extract-audio", "anything.mp4"])
        self.assertEqual(rc, 1)

    def test_existing_video_dispatches_to_extract(self):
        with tempfile.NamedTemporaryFile(suffix=".mp4") as f:
            with mock.patch.object(cangjie, "cmd_extract_audio", return_value=0) as m:
                rc = cangjie.main(["extract-audio", f.name])
            self.assertEqual(rc, 0)
            self.assertEqual(m.call_count, 1)
            # 校验后的路径是绝对化字符串
            self.assertEqual(m.call_args[0][0].video_path, str(Path(f.name).resolve()))


if __name__ == "__main__":
    unittest.main()
