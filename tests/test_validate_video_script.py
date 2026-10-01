#!/usr/bin/env python3
"""validate_video_script.py 校验门测试：每道门正/反用例 + 词表同步 tripwire。"""
import json
import os
import re
import sys
import tempfile
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import validate_video_script as vvs

GUIDELINES = Path(__file__).resolve().parent.parent / "references" / "guides" / "video-prompt-guidelines.md"
CAMERA_MOVEMENTS = Path(__file__).resolve().parent.parent / "references" / "guides" / "camera-movements.md"


def make_shot(**overrides):
    shot = {
        "id": "shot-1",
        "summary": "雨夜便利店全景，店员在补货",
        "seconds": 8,
        "shot_size": "wide shot",
        "camera_motion": "static",
        "dialogue": "无",
        "prompt": "A wide cinematic shot of a small convenience store at night, rain streaking down the windows.",
    }
    shot.update(overrides)
    return shot


def make_script(shots=None, **top):
    script = {
        "title": "深夜便利店的旧友",
        "logline": "疲惫的店员在雨夜与突然出现的旧友重逢",
        "style": "写实电影感，冷暖光对比",
        "shots": shots if shots is not None else [make_shot()],
    }
    script.update(top)
    return script


def gate(gates, name):
    for entry in gates:
        if entry["gate"] == name:
            return entry
    raise AssertionError(f"找不到门 {name}")


def run(script):
    return vvs.validate_script(script)


class TestSchemaGate(unittest.TestCase):
    def test_valid_script_passes_all_fail_gates(self):
        gates, stats = run(make_script())
        for entry in gates:
            if entry["level"] == "fail":
                self.assertTrue(entry["passed"], f"{entry['gate']} 不应失败：{entry['messages']}")
        self.assertEqual(vvs.verdict_of(gates), "pass")
        self.assertEqual(stats["shot_count"], 1)
        self.assertEqual(stats["total_seconds"], 8)

    def test_missing_shot_field_fails_with_field_name(self):
        shot = make_shot()
        del shot["dialogue"]
        gates, _ = run(make_script([shot]))
        messages = gate(gates, "schema")["messages"]
        self.assertFalse(gate(gates, "schema")["passed"])
        self.assertTrue(any("dialogue" in m for m in messages))

    def test_non_numeric_seconds_fails(self):
        gates, _ = run(make_script([make_shot(seconds="8")]))
        self.assertFalse(gate(gates, "schema")["passed"])

    def test_zero_and_negative_seconds_fail(self):
        for seconds in (0, -3):
            with self.subTest(seconds=seconds):
                gates, _ = run(make_script([make_shot(seconds=seconds)]))
                messages = gate(gates, "schema")["messages"]
                self.assertTrue(any("大于 0" in m for m in messages))

    def test_boolean_seconds_fails(self):
        gates, _ = run(make_script([make_shot(seconds=True)]))
        self.assertFalse(gate(gates, "schema")["passed"])

    def test_empty_prompt_fails(self):
        gates, _ = run(make_script([make_shot(prompt="  ")]))
        messages = gate(gates, "schema")["messages"]
        self.assertTrue(any("prompt" in m for m in messages))

    def test_duplicate_shot_id_fails(self):
        gates, _ = run(make_script([make_shot(), make_shot(id="shot-1", camera_motion="pans")]))
        messages = gate(gates, "schema")["messages"]
        self.assertTrue(any("id 重复" in m for m in messages))

    def test_missing_top_level_fields_fail(self):
        script = make_script()
        del script["title"]
        gates, _ = run(script)
        messages = gate(gates, "schema")["messages"]
        self.assertTrue(any("title" in m for m in messages))

    def test_top_level_without_shots_fails(self):
        gates, _ = run({"title": "t", "logline": "l", "style": "s"})
        self.assertFalse(gate(gates, "schema")["passed"])

    def test_segments_reference_unknown_shot_fails(self):
        segments = [{"id": "seg-1", "shot_ids": ["shot-x"]}]
        gates, _ = run(make_script(segments=segments))
        messages = gate(gates, "schema")["messages"]
        self.assertTrue(any("shot-x" in m for m in messages))

    def test_segments_overlay_attaches_to_shots(self):
        segments = [{"id": "seg-1", "shot_ids": ["shot-1"]}]
        ctx = vvs.prepare(make_script(segments=segments))
        self.assertEqual(ctx["shots"][0]["segment"], "seg-1")
        self.assertEqual(ctx["schema_errors"], [])

    def test_missing_shot_fields_reported_once_not_duplicated(self):
        gates, _ = run(make_script([{}]))
        messages = gate(gates, "schema")["messages"]
        self.assertEqual(len(messages), 7)
        self.assertTrue(all("缺少字段" in m for m in messages))


class TestDurationCap(unittest.TestCase):
    def test_short_film_uses_12s_cap(self):
        shots = [
            make_shot(id="shot-1", seconds=10),
            make_shot(id="shot-2", seconds=10, camera_motion="pans"),
            make_shot(id="shot-3", seconds=12.5, camera_motion="tilts"),
        ]
        gates, stats = run(make_script(shots))
        self.assertEqual(stats["duration_cap"], 12)
        messages = gate(gates, "duration-cap")["messages"]
        self.assertEqual(len(messages), 1)
        self.assertIn("shot-3", messages[0])
        self.assertIn("12s", messages[0])

    def test_12s_exactly_passes_in_short_film(self):
        shots = [make_shot(id="shot-1", seconds=12)]
        gates, stats = run(make_script(shots))
        self.assertEqual(stats["duration_cap"], 12)
        self.assertTrue(gate(gates, "duration-cap")["passed"])

    def test_longer_film_uses_15s_cap(self):
        shots = [
            make_shot(id="shot-1", seconds=14),
            make_shot(id="shot-2", seconds=14, camera_motion="pans"),
            make_shot(id="shot-3", seconds=14, camera_motion="tilts"),
            make_shot(id="shot-4", seconds=14, camera_motion="follows"),
            make_shot(id="shot-5", seconds=15.5, camera_motion="handheld"),
        ]
        gates, stats = run(make_script(shots))
        self.assertEqual(stats["duration_cap"], 15)
        messages = gate(gates, "duration-cap")["messages"]
        self.assertEqual(len(messages), 1)
        self.assertIn("shot-5", messages[0])
        self.assertIn("15s", messages[0])

    def test_total_exactly_60_treated_as_short_film(self):
        shots = [make_shot(id=f"shot-{i}", seconds=20) for i in range(1, 4)]
        gates, stats = run(make_script(shots))
        self.assertEqual(stats["total_seconds"], 60)
        self.assertEqual(stats["duration_cap"], 12)
        self.assertEqual(len(gate(gates, "duration-cap")["messages"]), 3)

    def test_invalid_seconds_do_not_break_cap_calculation(self):
        shots = [make_shot(id="shot-1", seconds="bad"), make_shot(id="shot-2", seconds=20, camera_motion="pans")]
        gates, stats = run(make_script(shots))
        self.assertEqual(stats["total_seconds"], 20)
        self.assertEqual(stats["duration_cap"], 12)
        self.assertFalse(gate(gates, "schema")["passed"])


class TestCameraEnum(unittest.TestCase):
    def test_every_motion_word_passes(self):
        for word in vvs.CAMERA_MOTIONS:
            with self.subTest(word=word):
                gates, _ = run(make_script([make_shot(camera_motion=word)]))
                self.assertTrue(gate(gates, "camera-enum")["passed"], word)

    def test_unknown_word_fails_with_allowed_list(self):
        gates, _ = run(make_script([make_shot(camera_motion="spins around")]))
        entry = gate(gates, "camera-enum")
        self.assertFalse(entry["passed"])
        self.assertIn("spins around", entry["messages"][0])
        self.assertIn("pushes in", entry["messages"][0])

    def test_case_insensitive_match(self):
        gates, _ = run(make_script([make_shot(camera_motion="  Pushes In ")]))
        self.assertTrue(gate(gates, "camera-enum")["passed"])

    def test_non_string_camera_motion_skips_enum_gate(self):
        gates, _ = run(make_script([make_shot(camera_motion=3)]))
        self.assertFalse(gate(gates, "schema")["passed"])
        self.assertTrue(gate(gates, "camera-enum")["passed"])


class TestCameraVariation(unittest.TestCase):
    def test_three_same_word_fails(self):
        shots = [make_shot(id=f"shot-{i}", camera_motion="static") for i in range(1, 4)]
        gates, _ = run(make_script(shots))
        entry = gate(gates, "camera-variation")
        self.assertFalse(entry["passed"])
        self.assertIn("固定", entry["messages"][0])

    def test_two_same_word_passes(self):
        shots = [
            make_shot(id="shot-1", camera_motion="static"),
            make_shot(id="shot-2", camera_motion="static"),
            make_shot(id="shot-3", camera_motion="pushes in"),
        ]
        gates, _ = run(make_script(shots))
        self.assertTrue(gate(gates, "camera-variation")["passed"])

    def test_same_family_different_words_fails(self):
        shots = [
            make_shot(id="shot-1", camera_motion="pans"),
            make_shot(id="shot-2", camera_motion="tilts"),
            make_shot(id="shot-3", camera_motion="pans"),
        ]
        gates, _ = run(make_script(shots))
        entry = gate(gates, "camera-variation")
        self.assertFalse(entry["passed"])
        self.assertIn("摇转", entry["messages"][0])

    def test_four_consecutive_report_two_windows(self):
        shots = [make_shot(id=f"shot-{i}", camera_motion="static") for i in range(1, 5)]
        gates, _ = run(make_script(shots))
        self.assertEqual(len(gate(gates, "camera-variation")["messages"]), 2)

    def test_adjacency_checked_across_segment_boundaries(self):
        shots = [make_shot(id=f"shot-{i}", camera_motion="static") for i in range(1, 4)]
        segments = [{"id": "seg-1", "shot_ids": ["shot-1", "shot-2", "shot-3"]}]
        gates, _ = run(make_script(shots, segments=segments))
        self.assertFalse(gate(gates, "camera-variation")["passed"])

    def test_unknown_motion_skips_family_check(self):
        shots = [make_shot(id=f"shot-{i}", camera_motion="spins around") for i in range(1, 4)]
        gates, _ = run(make_script(shots))
        self.assertTrue(gate(gates, "camera-variation")["passed"])
        self.assertFalse(gate(gates, "camera-enum")["passed"])


class TestSpeechUnits(unittest.TestCase):
    def test_hangul_counts_one_per_syllable(self):
        self.assertEqual(vvs.speech_units("안녕하세요"), 5)

    def test_fullwidth_latin_counts_as_word(self):
        self.assertEqual(vvs.speech_units("ＡＢＣ"), 2)
        self.assertEqual(vvs.speech_units("ｈｅｌｌｏ ｗｏｒｌｄ"), 4)

    def test_fullwidth_digits_still_counted(self):
        self.assertEqual(vvs.speech_units("１２３"), 2)

    def test_mixed_script_adds_across_categories(self):
        self.assertEqual(vvs.speech_units("abc 123 你好"), 2 + 2 + 1 + 1)


class TestDialogueRate(unittest.TestCase):
    def test_chinese_within_budget_passes(self):
        gates, _ = run(make_script([make_shot(seconds=4, dialogue="店员（惊讶）：“真的吗”")]))
        self.assertTrue(gate(gates, "dialogue-rate")["passed"])

    def test_chinese_over_budget_fails(self):
        dialogue = "店员（惊讶）：“我真的不敢相信眼前发生的这一切啊”"
        gates, _ = run(make_script([make_shot(seconds=2, dialogue=dialogue)]))
        entry = gate(gates, "dialogue-rate")
        self.assertFalse(entry["passed"])
        self.assertIn("shot-1", entry["messages"][0])
        self.assertIn("2s", entry["messages"][0])

    def test_exact_budget_boundary_passes(self):
        dialogue = "店员：“一二三四五六七八九十”"
        gates, _ = run(make_script([make_shot(seconds=2, dialogue=dialogue)]))
        self.assertTrue(gate(gates, "dialogue-rate")["passed"])

    def test_english_words_convert_to_two_units(self):
        gates, _ = run(make_script([make_shot(seconds=2, dialogue='He says, "We need to run now"')]))
        self.assertTrue(gate(gates, "dialogue-rate")["passed"])

    def test_english_over_budget_fails(self):
        gates, _ = run(make_script([make_shot(seconds=1.5, dialogue='He says, "We need to run now"')]))
        self.assertFalse(gate(gates, "dialogue-rate")["passed"])

    def test_unquoted_dialogue_uses_full_string(self):
        dialogue = "店员说他真的已经很累很累很累了"
        gates, _ = run(make_script([make_shot(seconds=2, dialogue=dialogue)]))
        self.assertFalse(gate(gates, "dialogue-rate")["passed"])

    def test_role_prefix_not_counted_when_quoted(self):
        long_role = "一个名字特别特别长的角色名（情绪非常复杂）"
        quoted = long_role + "：“好”"
        gates, _ = run(make_script([make_shot(seconds=1, dialogue=quoted)]))
        self.assertTrue(gate(gates, "dialogue-rate")["passed"])

    def test_wu_marker_skips_rate_check(self):
        gates, _ = run(make_script([make_shot(dialogue="无")]))
        self.assertTrue(gate(gates, "dialogue-rate")["passed"])


class TestDialoguePresence(unittest.TestCase):
    def test_empty_dialogue_warns(self):
        gates, _ = run(make_script([make_shot(dialogue="")]))
        entry = gate(gates, "dialogue-presence")
        self.assertEqual(entry["level"], "warn")
        self.assertFalse(entry["passed"])
        self.assertEqual(vvs.verdict_of(gates), "warn")

    def test_blank_dialogue_warns(self):
        gates, _ = run(make_script([make_shot(dialogue="   ")]))
        self.assertFalse(gate(gates, "dialogue-presence")["passed"])

    def test_non_string_dialogue_is_schema_fail_not_warn(self):
        gates, _ = run(make_script([make_shot(dialogue=None)]))
        self.assertFalse(gate(gates, "schema")["passed"])
        self.assertTrue(gate(gates, "dialogue-presence")["passed"])

    def test_explicit_wu_does_not_warn(self):
        gates, _ = run(make_script([make_shot(dialogue="无")]))
        self.assertTrue(gate(gates, "dialogue-presence")["passed"])


class TestGatesLog(unittest.TestCase):
    def _write(self, directory, name, payload):
        path = directory / name
        path.write_text(payload, encoding="utf-8")
        return path

    def test_pass_run_appends_single_json_line_next_to_file(self):
        with tempfile.TemporaryDirectory() as d:
            path = self._write(Path(d), "shots.json", json.dumps(make_script(), ensure_ascii=False))
            code = vvs.main([str(path)])
            self.assertEqual(code, 0)
            log = Path(d) / ".gates.jsonl"
            self.assertTrue(log.is_file())
            lines = log.read_text(encoding="utf-8").splitlines()
            self.assertEqual(len(lines), 1)
            record = json.loads(lines[0])
            self.assertEqual(record["verdict"], "pass")
            self.assertEqual(record["file"], str(path))
            self.assertEqual(record["shot_count"], 1)
            self.assertIn("timestamp", record)
            self.assertTrue(all(g["passed"] for g in record["gates"] if g["level"] == "fail"))

    def test_fail_run_returns_1_and_logs_verdict(self):
        with tempfile.TemporaryDirectory() as d:
            script = make_script([make_shot(seconds=30)])
            path = self._write(Path(d), "shots.json", json.dumps(script, ensure_ascii=False))
            code = vvs.main([str(path)])
            self.assertEqual(code, 1)
            record = json.loads((Path(d) / ".gates.jsonl").read_text(encoding="utf-8").splitlines()[0])
            self.assertEqual(record["verdict"], "fail")
            self.assertGreaterEqual(record["fail_count"], 1)

    def test_repeated_runs_accumulate(self):
        with tempfile.TemporaryDirectory() as d:
            path = self._write(Path(d), "shots.json", json.dumps(make_script(), ensure_ascii=False))
            vvs.main([str(path)])
            vvs.main([str(path)])
            self.assertEqual(len((Path(d) / ".gates.jsonl").read_text(encoding="utf-8").splitlines()), 2)

    def test_gates_path_override(self):
        with tempfile.TemporaryDirectory() as d:
            path = self._write(Path(d), "shots.json", json.dumps(make_script(), ensure_ascii=False))
            custom = Path(d) / "nested" / "gates.jsonl"
            code = vvs.main([str(path), "--gates", str(custom)])
            self.assertEqual(code, 0)
            self.assertTrue(custom.is_file())
            self.assertFalse((Path(d) / ".gates.jsonl").exists())


class TestCli(unittest.TestCase):
    def test_missing_file_returns_1(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(vvs.main([str(Path(d) / "nope.json")]), 1)

    def test_invalid_json_returns_1(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "shots.json"
            path.write_text("{not json", encoding="utf-8")
            self.assertEqual(vvs.main([str(path)]), 1)

    def test_warn_only_returns_0(self):
        with tempfile.TemporaryDirectory() as d:
            script = make_script([make_shot(dialogue="")])
            path = Path(d) / "shots.json"
            path.write_text(json.dumps(script, ensure_ascii=False), encoding="utf-8")
            self.assertEqual(vvs.main([str(path)]), 0)


class TestMotionWordsSyncWithReferences(unittest.TestCase):
    """词表 tripwire：脚本枚举与两个 references 文件必须同步，防止单边漂移。"""

    def test_guidelines_camera_row_covered_by_enum(self):
        content = GUIDELINES.read_text(encoding="utf-8")
        match = re.search(r"\*\*镜头语言\*\*\s*\|([^|]+)\|", content)
        self.assertIsNotNone(match, "guidelines 五节应保留“镜头语言”行")
        for term in match.group(1).split(","):
            term = term.strip().lower()
            if not term:
                continue
            if "(" in term:
                base = term.split("(")[0].strip()
                alias = term[term.index("(") + 1 : term.index(")")].strip()
                self.assertIn(base, vvs.CAMERA_MOTIONS, term)
                self.assertIn(alias, vvs.CAMERA_MOTIONS, term)
            else:
                self.assertIn(term, vvs.CAMERA_MOTIONS, term)

    def test_enum_canonical_words_all_listed_in_guidelines(self):
        content = GUIDELINES.read_text(encoding="utf-8")
        match = re.search(r"\*\*镜头语言\*\*\s*\|([^|]+)\|", content)
        row = match.group(1).lower()
        for word in vvs.CAMERA_MOTIONS - {"over-the-shoulder"}:
            self.assertIn(word, row, word)

    def test_camera_movements_table_matches_enum_and_families(self):
        content = CAMERA_MOVEMENTS.read_text(encoding="utf-8")
        rows = [line for line in content.splitlines() if line.startswith("|")]
        self.assertTrue(rows, "camera-movements.md 应有对照表")
        mapped = set()
        for line in rows:
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            term = cells[0].lower() if cells else ""
            if not term or term == "术语" or set(term) <= {"-", ":"}:
                continue  # 表头与分隔行
            self.assertIn(term, vvs.CAMERA_MOTIONS, f"表格术语 {term!r} 不在脚本枚举里")
            self.assertEqual(
                vvs.CAMERA_FAMILIES[term],
                cells[1],
                f"{term} 的类型列与脚本 CAMERA_FAMILIES 不一致",
            )
            mapped.add(term)
        # over-the-shoulder 是 ots 的别名写法，不单独占表行，由 guidelines 同步测试覆盖
        self.assertEqual(mapped, vvs.CAMERA_MOTIONS - {"over-the-shoulder"}, "对照表应覆盖全部运镜词")


if __name__ == "__main__":
    unittest.main()
