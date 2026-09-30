#!/usr/bin/env python3
"""cangjie scripts/utils.py 纯函数离线测试。"""
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from utils import ensure_output_dir, format_timestamp, validate_audio_file


class TestFormatTimestamp(unittest.TestCase):
    def test_zero(self):
        self.assertEqual(format_timestamp(0), "0:00:00")

    def test_sub_minute_fraction_dropped(self):
        self.assertEqual(format_timestamp(59.9), "0:00:59")

    def test_minute_and_hour_boundaries(self):
        self.assertEqual(format_timestamp(60), "0:01:00")
        self.assertEqual(format_timestamp(3599.76), "0:59:59")
        self.assertEqual(format_timestamp(3661), "1:01:01")

    def test_day_folds_into_total_hours(self):
        # str(timedelta) 对 ≥24h 会输出 "1 day, H:MM:SS"，契约要求 HH:MM:SS
        self.assertEqual(format_timestamp(86400), "24:00:00")
        self.assertEqual(format_timestamp(90061), "25:01:01")

    def test_just_below_day(self):
        self.assertEqual(format_timestamp(86399), "23:59:59")


class TestValidateAudioFile(unittest.TestCase):
    def test_existing_file_returns_resolved_path(self):
        with tempfile.NamedTemporaryFile(suffix=".wav") as f:
            p = validate_audio_file(f.name)
            self.assertIsInstance(p, Path)
            self.assertEqual(p, Path(f.name).resolve())

    def test_missing_file_exits_1(self):
        with self.assertRaises(SystemExit) as ctx:
            validate_audio_file("/nonexistent/dir/audio.wav")
        self.assertEqual(ctx.exception.code, 1)

    def test_directory_exits_1(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(SystemExit) as ctx:
                validate_audio_file(d)
            self.assertEqual(ctx.exception.code, 1)


class TestEnsureOutputDir(unittest.TestCase):
    def test_creates_missing_parent_dirs(self):
        with tempfile.TemporaryDirectory() as d:
            out = os.path.join(d, "nested", "deep", "out.txt")
            p = ensure_output_dir(out)
            self.assertTrue(Path(out).parent.is_dir())
            self.assertEqual(p, Path(out).resolve())

    def test_existing_dir_is_noop(self):
        with tempfile.TemporaryDirectory() as d:
            out = os.path.join(d, "out.txt")
            p = ensure_output_dir(out)
            self.assertEqual(p, Path(out).resolve())


if __name__ == "__main__":
    unittest.main()
