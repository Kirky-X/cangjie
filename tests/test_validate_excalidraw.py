"""references/excalidraw/validate_excalidraw.py 纯函数与 CLI 离线测试。

脚本不在包内且与渲染工具链同址，按路径 importlib 加载。
"""
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest

sys.dont_write_bytecode = True

_SCRIPT = os.path.join(
    os.path.dirname(__file__), "..", "references", "excalidraw", "validate_excalidraw.py"
)
_spec = importlib.util.spec_from_file_location("validate_excalidraw", _SCRIPT)
mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mod)


def rect(el_id, x=0, y=0, w=100, h=50, **extra):
    el = {"type": "rectangle", "id": el_id, "x": x, "y": y, "width": w, "height": h}
    el.update(extra)
    return el


def text(el_id, x=0, y=0, w=80, h=20, **extra):
    el = {"type": "text", "id": el_id, "x": x, "y": y, "width": w, "height": h,
          "fontSize": 16, "text": el_id, "originalText": el_id}
    el.update(extra)
    return el


def arrow(el_id, x=0, y=0, points=None, **extra):
    el = {"type": "arrow", "id": el_id, "x": x, "y": y,
          "width": 0, "height": 0, "points": points or [[0, 0], [100, 0]]}
    el.update(extra)
    return el


def diagram(elements):
    return {"type": "excalidraw", "version": 2, "elements": list(elements)}


def validate(elements, palette=frozenset({"#3b82f6", "#1e3a5f"})):
    # 默认给白名单集合：None 在脚本语义中是"调色板文件缺失"，由专门用例覆盖
    return mod.validate(diagram(elements), palette)


class ValidateStructure(unittest.TestCase):
    def test_minimal_valid_diagram_clean(self):
        errors, warnings = validate([rect("r1")])
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def test_wrong_top_level_type_fails(self):
        errors, _ = mod.validate({"type": "drawio", "elements": [rect("r1")]}, None)
        self.assertTrue(any("type" in e for e in errors))

    def test_missing_elements_fails(self):
        errors, _ = mod.validate({"type": "excalidraw"}, None)
        self.assertTrue(any("elements" in e for e in errors))

    def test_empty_elements_fails(self):
        errors, _ = mod.validate({"type": "excalidraw", "elements": []}, None)
        self.assertTrue(any("为空" in e for e in errors))

    def test_non_object_element_fails(self):
        errors, _ = mod.validate({"type": "excalidraw", "elements": ["oops"]}, None)
        self.assertTrue(any("不是对象" in e for e in errors))

    def test_element_without_id_fails(self):
        errors, _ = validate([{"type": "rectangle", "x": 0, "y": 0, "width": 1, "height": 1}])
        self.assertTrue(any("id" in e for e in errors))


class ValidateDuplicateIds(unittest.TestCase):
    def test_duplicate_id_fails_once_per_id(self):
        errors, _ = validate([rect("dup"), rect("dup"), rect("dup"), rect("dup")])
        dup_errors = [e for e in errors if "重复" in e]
        self.assertEqual(len(dup_errors), 1)
        self.assertIn('"dup"', dup_errors[0])

    def test_deleted_duplicate_ignored(self):
        errors, _ = validate([rect("r1"), rect("r1", isDeleted=True)])
        self.assertEqual(errors, [])


class ValidateDanglingRefs(unittest.TestCase):
    def test_dangling_boundelements_fails(self):
        errors, _ = validate([rect("r1", boundElements=[{"id": "ghost", "type": "arrow"}])])
        self.assertTrue(any("boundElements" in e and "ghost" in e for e in errors))

    def test_dangling_start_and_end_binding_fail(self):
        el = rect("r1")
        errors, _ = validate([
            arrow("a1", startBinding={"elementId": "no-start", "focus": 0, "gap": 2},
                  endBinding={"elementId": "no-end", "focus": 0, "gap": 2}),
            el,
        ])
        self.assertTrue(any("startBinding" in e and "no-start" in e for e in errors))
        self.assertTrue(any("endBinding" in e and "no-end" in e for e in errors))

    def test_dangling_container_and_frame_id_fail(self):
        errors, _ = validate([text("t1", containerId="no-box"), rect("f1", frameId="no-frame")])
        self.assertTrue(any("containerId" in e and "no-box" in e for e in errors))
        self.assertTrue(any("frameId" in e and "no-frame" in e for e in errors))

    def test_existing_references_pass(self):
        errors, _ = validate([
            rect("r1", boundElements=[{"id": "a1", "type": "arrow"}]),
            arrow("a1", startBinding={"elementId": "r1", "focus": 0, "gap": 2},
                  endBinding={"elementId": "r2", "focus": 0, "gap": 2}),
            rect("r2", boundElements=[{"id": "a1", "type": "arrow"}]),
        ])
        self.assertEqual(errors, [])


class ValidateBindingConsistency(unittest.TestCase):
    def test_text_binding_without_backref_warns(self):
        _, warnings = validate([rect("box"), text("t1", containerId="box")])
        self.assertTrue(any("未回指" in w and "t1" in w for w in warnings))

    def test_container_declares_text_without_containerid_warns(self):
        _, warnings = validate([
            rect("box", boundElements=[{"id": "t1", "type": "text"}]),
            text("t1"),
        ])
        self.assertTrue(any("containerId" in w and "t1" in w for w in warnings))

    def test_arrow_binding_without_backref_warns(self):
        _, warnings = validate([
            rect("r1"),
            rect("r2"),
            arrow("a1", startBinding={"elementId": "r1", "focus": 0, "gap": 2}),
        ])
        self.assertTrue(any("未回指" in w and "a1" in w for w in warnings))

    def test_full_binding_roundtrip_clean(self):
        errors, warnings = validate([
            rect("box", boundElements=[{"id": "t1", "type": "text"}, {"id": "a1", "type": "arrow"}]),
            text("t1", x=10, y=10, w=80, h=20, containerId="box"),
            rect("r2", boundElements=[{"id": "a1", "type": "arrow"}]),
            arrow("a1", x=100, y=25, startBinding={"elementId": "box", "focus": 0, "gap": 2},
                  endBinding={"elementId": "r2", "focus": 0, "gap": 2}),
        ])
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])


class ValidateOverflow(unittest.TestCase):
    def test_text_overflowing_container_fails(self):
        errors, _ = validate([rect("box", w=100, h=50), text("t1", x=90, y=10, w=80, h=20, containerId="box")])
        self.assertTrue(any("溢出" in e and "box" in e for e in errors))

    def test_text_within_container_tolerance_passes(self):
        # 文字右缘 103 = 容器右缘 100 + TOL 3，视为贴边
        errors, _ = validate([rect("box", w=100, h=50), text("t1", x=0, y=0, w=103, h=50, containerId="box")])
        self.assertEqual(errors, [])

    def test_frame_child_overflow_fails(self):
        errors, _ = validate([
            rect("frame", w=100, h=100),
            rect("child", x=200, y=0, w=50, h=50, frameId="frame"),
        ])
        self.assertTrue(any("溢出" in e and "frame" in e for e in errors))

    def test_frame_child_inside_passes(self):
        errors, _ = validate([
            rect("frame", w=100, h=100),
            rect("child", x=10, y=10, w=50, h=50, frameId="frame"),
        ])
        self.assertEqual(errors, [])


class ValidateOverlap(unittest.TestCase):
    def test_substantial_overlap_warns_once_per_pair(self):
        _, warnings = validate([rect("a", x=0, y=0), rect("b", x=50, y=0)])
        overlap = [w for w in warnings if "重叠" in w]
        self.assertEqual(len(overlap), 1)
        self.assertIn('"a"', overlap[0])
        self.assertIn('"b"', overlap[0])

    def test_contained_element_not_flagged(self):
        # 完全包含属有意分层（徽标、绑定文字、代码块底板）
        _, warnings = validate([rect("outer", w=200, h=100), rect("inner", x=10, y=10, w=50, h=40)])
        self.assertEqual([w for w in warnings if "重叠" in w], [])

    def test_slight_touch_not_flagged(self):
        # 交叠 5×50=250 < 20% × 5000，属轻微接触
        _, warnings = validate([rect("a", x=0, y=0), rect("b", x=95, y=0)])
        self.assertEqual([w for w in warnings if "重叠" in w], [])

    def test_crossing_lines_not_checked(self):
        _, warnings = validate([
            {"type": "line", "id": "l1", "x": 0, "y": 0, "width": 100, "height": 100,
             "points": [[0, 0], [100, 100]]},
            {"type": "line", "id": "l2", "x": 0, "y": 100, "width": 100, "height": 100,
             "points": [[0, 100], [100, 0]]},
        ])
        self.assertEqual([w for w in warnings if "重叠" in w], [])

    def test_bound_text_overlapping_other_shape_warns(self):
        _, warnings = validate([
            rect("box", x=0, y=0, w=100, h=50),
            text("t1", x=10, y=15, w=80, h=20, containerId="box"),
            rect("other", x=20, y=20, w=100, h=50),
        ])
        self.assertTrue(any("重叠" in w and "t1" in w for w in warnings))


class ValidatePalette(unittest.TestCase):
    PALETTE = {"#3b82f6", "#1e3a5f", "#1e293b"}

    def test_off_palette_color_warns_with_users(self):
        _, warnings = validate(
            [rect("a", strokeColor="#ff0000"), rect("b", strokeColor="#FF0000")],
            palette=self.PALETTE,
        )
        color_warns = [w for w in warnings if "#ff0000" in w]
        self.assertEqual(len(color_warns), 1)
        self.assertIn("a.strokeColor", color_warns[0])
        self.assertIn("b.strokeColor", color_warns[0])

    def test_palette_color_and_transparent_pass(self):
        _, warnings = validate(
            [rect("a", strokeColor="#3b82f6", backgroundColor="transparent")],
            palette=self.PALETTE,
        )
        self.assertEqual([w for w in warnings if "调色板" in w], [])

    def test_three_digit_hex_expanded(self):
        _, warnings = validate([rect("a", strokeColor="#3b8")], palette={"#33bb88"})
        self.assertEqual([w for w in warnings if "调色板" in w], [])

    def test_missing_palette_file_reported_once(self):
        _, warnings = validate([rect("a", strokeColor="#123456")], palette=None)
        self.assertEqual(len([w for w in warnings if "跳过色值" in w]), 1)

    def test_load_palette_reads_real_file(self):
        palette = mod.load_palette(os.path.join(os.path.dirname(_SCRIPT), "color-palette.md"))
        self.assertIsNotNone(palette)
        self.assertIn("#3b82f6", palette)
        self.assertIn("#ffffff", palette)

    def test_load_palette_missing_file_returns_none(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertIsNone(mod.load_palette(os.path.join(d, "absent.md")))


class ValidateFontSizes(unittest.TestCase):
    def test_within_limit_passes(self):
        elements = [text(f"t{i}", fontSize=s) for i, s in enumerate([16, 20, 28, 12])]
        _, warnings = validate(elements)
        self.assertEqual([w for w in warnings if "字号" in w], [])

    def test_over_limit_warns_with_sizes(self):
        elements = [text(f"t{i}", fontSize=s) for i, s in enumerate([16, 20, 28, 12, 24])]
        _, warnings = validate(elements)
        size_warns = [w for w in warnings if "字号" in w]
        self.assertEqual(len(size_warns), 1)
        self.assertIn("5 种", size_warns[0])

    def test_font_size_only_counts_text_elements(self):
        # fontSize 只对 text 元素计数，形状元素上的同名属性不参与
        _, warnings = validate([rect("r1", fontSize=99), rect("r2", fontSize=98)])
        self.assertEqual([w for w in warnings if "字号" in w], [])


class Cli(unittest.TestCase):
    def run_cli(self, payload):
        fd, path = tempfile.mkstemp(suffix=".excalidraw")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(payload, f)
            return subprocess.run([sys.executable, os.path.abspath(_SCRIPT), path],
                                  capture_output=True, text=True)
        finally:
            os.unlink(path)

    def test_valid_file_exits_zero(self):
        proc = self.run_cli(diagram([rect("r1")]))
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("静态门禁通过", proc.stdout)

    def test_dangling_ref_exits_one(self):
        proc = self.run_cli(diagram([rect("r1", boundElements=[{"id": "ghost", "type": "arrow"}])]))
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        self.assertIn("FAIL", proc.stdout)

    def test_syntax_error_exits_one(self):
        fd, path = tempfile.mkstemp(suffix=".excalidraw")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                f.write("{not json")
            proc = subprocess.run([sys.executable, os.path.abspath(_SCRIPT), path],
                                  capture_output=True, text=True)
        finally:
            os.unlink(path)
        self.assertEqual(proc.returncode, 1)
        self.assertIn("JSON 语法错误", proc.stdout)


if __name__ == "__main__":
    unittest.main()
