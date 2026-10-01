#!/usr/bin/env python3
"""cangjie scripts/audit_summary.py 离线测试：覆盖率地板 / 退化重复 / deep-dive 下限。"""
import json
import os
import random
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import audit_summary as A

random.seed(7)
_WORDS = ["网络", "延迟", "缓存", "分片", "索引", "队列", "线程", "信号", "采样", "矩阵",
          "阈值", "吞吐", "抖动", "回滚", "熔断", "灰度", "埋点", "拓扑", "路由", "限流"]


def rich_text(sentences: int) -> str:
    """生成 8-gram 多样性接近 1 的确定性中文文本（随机词组合，句子间几乎无重复窗口）。"""
    parts = []
    for _ in range(sentences):
        body = "".join(random.choice(_WORDS) for _ in range(10))
        parts.append(f"关于{body}的讨论记录。")
    return "".join(parts)


class TestStripNoise(unittest.TestCase):
    def test_frontmatter_removed(self):
        text = "---\ntitle: 演示\nauthor: 某人\n---\n\n这是正文。"
        self.assertEqual(A.strip_noise(text).strip(), "这是正文。")

    def test_fenced_code_removed(self):
        text = "前文\n```python\nprint('secret-code')\n```\n后文"
        out = A.strip_noise(text)
        self.assertIn("前文", out)
        self.assertIn("后文", out)
        self.assertNotIn("secret-code", out)

    def test_image_url_timestamp_removed(self):
        text = "[00:01:30] 看这张图 ![截图](https://example.com/a.png) 与 <img src='https://x/y.png'> 的说明"
        out = A.strip_noise(text)
        self.assertNotIn("example.com", out)
        self.assertNotIn("00:01:30", out)
        self.assertIn("看这张图", out)
        self.assertIn("的说明", out)

    def test_leading_timestamp_and_html_comment_removed(self):
        self.assertEqual(A.strip_noise("00:15 开场白").strip(), "开场白")
        self.assertEqual(A.strip_noise("<!-- 核对项 -->正文").strip(), "正文")

    def test_multiline_html_comment_removed(self):
        text = "正文<!--\n灌水内容灌水内容\n-->结尾"
        out = A.strip_noise(text)
        self.assertNotIn("灌水", out)
        self.assertEqual(A.effective_chars(text), len("正文结尾"))

    def test_unclosed_comment_strips_rest_of_text(self):
        out = A.strip_noise("前文<!--未闭合\n中间不算")
        self.assertEqual(out.strip(), "前文")

    def test_multiple_comments_on_one_line(self):
        self.assertEqual(A.strip_noise("a<!--x-->b<!--y-->c").strip(), "abc")

    def test_comment_inside_fence_ignored_without_state_leak(self):
        out = A.strip_noise("```\n<!-- 围栏内\n```\n后文")
        self.assertIn("后文", out)
        self.assertNotIn("围栏内", out)

    def test_effective_chars_ignores_whitespace_and_noise(self):
        text = "[00:10]  访问 https://example.com/x 获取\n更多内容。"
        self.assertEqual(A.effective_chars(text), len("访问获取更多内容。"))


class TestCoverage(unittest.TestCase):
    def test_high_ratio_passes(self):
        results = A.audit(rich_text(50), rich_text(100))
        cov = next(r for r in results if r["name"] == "coverage")
        self.assertEqual(cov["status"], "PASS")

    def test_low_ratio_warns_with_counts(self):
        results = A.audit(rich_text(2), rich_text(100))
        cov = next(r for r in results if r["name"] == "coverage")
        self.assertEqual(cov["status"], "WARN")
        self.assertIn("0.0", cov["detail"])
        self.assertIn("有效字符", cov["detail"])

    def test_exempt_coverage_skips(self):
        results = A.audit(rich_text(2), rich_text(100), exempt=("coverage",))
        cov = next(r for r in results if r["name"] == "coverage")
        self.assertEqual(cov["status"], "SKIP")

    def test_empty_input_skips_without_division_error(self):
        results = A.audit(rich_text(5), "")
        cov = next(r for r in results if r["name"] == "coverage")
        self.assertEqual(cov["status"], "SKIP")


class TestRepetition(unittest.TestCase):
    def test_line_repeated_4_times_warns(self):
        summary = "同一段内容原样出现\n" * 4 + rich_text(20)
        rep = next(r for r in A.audit(summary, rich_text(100)) if r["name"] == "repetition")
        self.assertEqual(rep["status"], "WARN")
        self.assertIn("同一段内容原样出现", rep["detail"])

    def test_line_repeated_3_times_passes(self):
        summary = "同一段内容原样出现\n" * 3 + rich_text(20)
        rep = next(r for r in A.audit(summary, rich_text(100)) if r["name"] == "repetition")
        self.assertEqual(rep["status"], "PASS")

    def test_table_divider_lines_not_counted(self):
        summary = "| --- | --- |\n" * 6 + rich_text(5)
        rep = next(r for r in A.audit(summary, rich_text(50)) if r["name"] == "repetition")
        self.assertEqual(rep["status"], "PASS")

    def test_low_gram_diversity_warns(self):
        summary = "abcdefgh" * 12 + rich_text(5)
        rep = next(r for r in A.audit(summary, rich_text(50)) if r["name"] == "repetition")
        self.assertEqual(rep["status"], "WARN")
        self.assertIn("8-gram", rep["detail"])

    def test_short_text_skips_gram_check(self):
        self.assertEqual(A.gram_diversity("很短"), (1.0, 0))

    def test_exempt_repetition_skips(self):
        summary = "同一段内容原样出现\n" * 4 + rich_text(20)
        rep = next(r for r in A.audit(summary, rich_text(100), exempt=("repetition",))
                   if r["name"] == "repetition")
        self.assertEqual(rep["status"], "SKIP")


class TestDeepDive(unittest.TestCase):
    def test_below_floor_warns(self):
        results = A.audit(rich_text(10), rich_text(100), density="deep-dive")
        dd = next(r for r in results if r["name"] == "deep-dive")
        self.assertEqual(dd["status"], "WARN")

    def test_above_floor_passes(self):
        results = A.audit(rich_text(150), rich_text(300), density="deep-dive")
        dd = next(r for r in results if r["name"] == "deep-dive")
        self.assertEqual(dd["status"], "PASS")

    def test_exempt_deep_dive_skips(self):
        results = A.audit(rich_text(10), rich_text(100), density="deep-dive", exempt=("deep-dive",))
        dd = next(r for r in results if r["name"] == "deep-dive")
        self.assertEqual(dd["status"], "SKIP")

    def test_non_deep_dive_has_no_entry(self):
        results = A.audit(rich_text(10), rich_text(100), density="brief")
        self.assertFalse(any(r["name"] == "deep-dive" for r in results))
        results = A.audit(rich_text(10), rich_text(100))
        self.assertFalse(any(r["name"] == "deep-dive" for r in results))


class TestCli(unittest.TestCase):
    script = Path(__file__).resolve().parent.parent / "scripts" / "audit_summary.py"

    def run_cli(self, *cli_args):
        return subprocess.run(
            [sys.executable, str(self.script), *cli_args],
            capture_output=True, text=True,
        )

    def test_json_smoke_pass(self):
        with tempfile.TemporaryDirectory() as d:
            summary = os.path.join(d, "s.md")
            inp = os.path.join(d, "i.md")
            Path(summary).write_text(rich_text(50), encoding="utf-8")
            Path(inp).write_text(rich_text(100), encoding="utf-8")
            proc = self.run_cli(summary, inp, "--json")
            self.assertEqual(proc.returncode, 0, proc.stderr)
            payload = json.loads(proc.stdout)
            self.assertEqual(payload["warn_count"], 0)
            self.assertEqual(payload["fail_count"], 0)
            self.assertIn("summary_effective_chars", payload)
            self.assertIn("input_effective_chars", payload)
            names = {c["name"] for c in payload["checks"]}
            self.assertEqual(names, {"coverage", "repetition"})
            for check in payload["checks"]:
                self.assertIn(check["status"], {"PASS", "WARN", "SKIP", "FAIL"})

    def test_json_deep_dive_warn_still_exit_zero(self):
        with tempfile.TemporaryDirectory() as d:
            summary = os.path.join(d, "s.md")
            inp = os.path.join(d, "i.md")
            Path(summary).write_text(rich_text(10), encoding="utf-8")
            Path(inp).write_text(rich_text(100), encoding="utf-8")
            proc = self.run_cli(summary, inp, "--density", "deep-dive", "--json")
            self.assertEqual(proc.returncode, 0, proc.stderr)
            payload = json.loads(proc.stdout)
            self.assertEqual(payload["warn_count"], 1)
            self.assertTrue(any(c["name"] == "deep-dive" and c["status"] == "WARN"
                                for c in payload["checks"]))

    def test_missing_file_exits_1(self):
        with tempfile.TemporaryDirectory() as d:
            inp = os.path.join(d, "i.md")
            Path(inp).write_text(rich_text(5), encoding="utf-8")
            proc = self.run_cli(os.path.join(d, "no-such-summary.md"), inp)
            self.assertEqual(proc.returncode, 1)

    def test_human_output_lists_checks(self):
        with tempfile.TemporaryDirectory() as d:
            summary = os.path.join(d, "s.md")
            inp = os.path.join(d, "i.md")
            Path(summary).write_text(rich_text(50), encoding="utf-8")
            Path(inp).write_text(rich_text(100), encoding="utf-8")
            proc = self.run_cli(summary, inp)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertIn("[PASS] coverage", proc.stdout)
            self.assertIn("结论", proc.stdout)


if __name__ == "__main__":
    unittest.main()
