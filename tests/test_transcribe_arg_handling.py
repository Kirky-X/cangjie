#!/usr/bin/env python3
"""两个转写脚本的参数处理离线测试（mock 转写函数，不加载 ML 模型）。

重依赖（faster-whisper / qwen-asr / librosa）均为函数内延迟导入，
模块导入本身离线安全，因此可对 main() 的参数默认值与 auto 语言处理做真实测试。
"""
import os
import sys
import unittest
from unittest import mock

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import transcribe_diarize_fw
import transcribe_with_diarization


class TestTranscribeDiarizeFwArgs(unittest.TestCase):
    def test_defaults_num_speakers_and_zh(self):
        with mock.patch.object(
            transcribe_diarize_fw, "transcribe_with_diarization"
        ) as fn, mock.patch.object(
            sys, "argv", ["prog", "a.wav"]
        ):
            transcribe_diarize_fw.main()
        fn.assert_called_once_with("a.wav", "a_diarized.txt", 3, "zh")

    def test_explicit_output_and_auto_language_passes_none(self):
        with mock.patch.object(
            transcribe_diarize_fw, "transcribe_with_diarization"
        ) as fn, mock.patch.object(
            sys, "argv", ["prog", "a.wav", "out.txt", "--num-speakers", "2", "--language", "AUTO"]
        ):
            transcribe_diarize_fw.main()
        fn.assert_called_once_with("a.wav", "out.txt", 2, None)


class TestTranscribeQwenArgs(unittest.TestCase):
    def test_default_output_suffix(self):
        with mock.patch.object(
            transcribe_with_diarization, "transcribe_audio"
        ) as fn, mock.patch.object(sys, "argv", ["prog", "a.wav"]):
            transcribe_with_diarization.main()
        fn.assert_called_once_with("a.wav", "a_transcript.txt")

    def test_explicit_output_passthrough(self):
        with mock.patch.object(
            transcribe_with_diarization, "transcribe_audio"
        ) as fn, mock.patch.object(
            sys, "argv", ["prog", "a.wav", "result.txt"]
        ):
            transcribe_with_diarization.main()
        fn.assert_called_once_with("a.wav", "result.txt")


if __name__ == "__main__":
    unittest.main()
