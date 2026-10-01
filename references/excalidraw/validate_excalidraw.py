#!/usr/bin/env python3
"""Excalidraw 静态校验器：渲染前拦截结构性缺陷，附带量化美学告警。

落点例外声明：仓库惯例是新增脚本进 scripts/，本脚本显式留在 references/excalidraw/
与 render_excalidraw.py、pyproject.toml 同址——渲染门禁以本目录为工作目录（uv 环境），
校验器与其所门禁的渲染脚本共用同一运行位置，色值白名单也直接以同目录 color-palette.md
为唯一真相源；拆到 scripts/ 会制造两个运行位置并复制一份色值枚举。

用法（纯标准库，无需 uv 环境，在 jq 语法校验之后、渲染之前运行）：
    python3 validate_excalidraw.py <path-to-file.excalidraw>

退出码：0 = 无 FAIL（WARN 不阻塞，结合设计意图判断）；1 = 存在 FAIL 或文件不可读。

检查分级：
- FAIL（结构缺陷，渲染图上必然可见，必须修复后才渲染）：文件结构非法、重复 id、
  悬空引用（boundElements / startBinding / endBinding / containerId / frameId）、
  绑定文字溢出容器、frame 子元素溢出。
- WARN（美学审计，可能是有意设计，交由渲染视检最终裁决）：元素矩形重叠、
  色值不在调色板白名单、字号种类超过上限、绑定关系单向缺失。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent

TOL = 3.0                 # 几何容差（px）：偏差在 TOL 内视为贴边，而非溢出或重叠
OVERLAP_MIN_RATIO = 0.2   # 交叠面积占较小元素面积低于该比例视为轻微接触，不告警
MAX_FONT_SIZES = 4        # 全图字号种类数上限，层级靠 3-4 档字号表达足够

_PALETTE_HEX_RE = re.compile(r"`#([0-9a-fA-F]{6})`")
_THREE_DIGIT_HEX_RE = re.compile(r"#([0-9a-f]{3})")
_SIX_DIGIT_HEX_RE = re.compile(r"#[0-9a-f]{6}")


def element_bbox(el: dict) -> tuple[float, float, float, float] | None:
    """元素外接矩形 (x0, y0, x1, y1)；arrow/line 以 points 相对坐标展开，缺坐标返回 None。"""
    x = el.get("x")
    y = el.get("y")
    if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
        return None
    if el.get("type") in ("arrow", "line") and isinstance(el.get("points"), list):
        xs: list[float] = []
        ys: list[float] = []
        for pt in el["points"]:
            if (isinstance(pt, (list, tuple)) and len(pt) == 2
                    and all(isinstance(v, (int, float)) for v in pt)):
                xs.append(x + pt[0])
                ys.append(y + pt[1])
        if xs:
            return (min(xs), min(ys), max(xs), max(ys))
    w = el.get("width", 0)
    h = el.get("height", 0)
    if not isinstance(w, (int, float)) or not isinstance(h, (int, float)):
        return None
    return (min(x, x + w), min(y, y + h), max(x, x + w), max(y, y + h))


def contains(outer: tuple[float, float, float, float],
             inner: tuple[float, float, float, float],
             tol: float = TOL) -> bool:
    """inner 是否落在 outer 内（含 TOL 容差）。"""
    return (inner[0] >= outer[0] - tol and inner[1] >= outer[1] - tol
            and inner[2] <= outer[2] + tol and inner[3] <= outer[3] + tol)


def load_palette(path: str | Path) -> set[str] | None:
    """从 color-palette.md 提取白名单色值（统一 #xxxxxx 小写）；文件不可读返回 None。"""
    try:
        text = Path(path).read_text(encoding="utf-8")
    except OSError:
        return None
    return {"#" + m.group(1).lower() for m in _PALETTE_HEX_RE.finditer(text)}


def normalize_color(value) -> str | None:
    """色值规范化为 #xxxxxx 小写（3 位 hex 扩展为 6 位）；无法识别返回 None。"""
    if not isinstance(value, str):
        return None
    v = value.strip().lower()
    if v == "transparent":
        return "transparent"
    m = _THREE_DIGIT_HEX_RE.fullmatch(v)
    if m:
        v = "#" + "".join(ch * 2 for ch in m.group(1))
    return v if _SIX_DIGIT_HEX_RE.fullmatch(v) else None


def validate(data, palette: set[str] | None) -> tuple[list[str], list[str]]:
    """校验 Excalidraw 数据，返回 (errors, warnings)。errors 非空即门禁不通过。"""
    errors: list[str] = []
    warnings: list[str] = []

    if not isinstance(data, dict):
        errors.append("文件顶层必须是 JSON 对象")
        return errors, warnings
    if data.get("type") != "excalidraw":
        errors.append(f"顶层 type 应为 'excalidraw'，实际为 {data.get('type')!r}")
    elements = data.get("elements")
    if not isinstance(elements, list):
        errors.append("缺少 'elements' 数组")
        return errors, warnings
    if not elements:
        errors.append("'elements' 为空——没有可渲染的内容")
        return errors, warnings

    for i, el in enumerate(elements):
        if not isinstance(el, dict):
            errors.append(f"elements[{i}] 不是对象")
            continue
        el_id = el.get("id")
        if not isinstance(el_id, str) or not el_id:
            errors.append(f"elements[{i}] 缺少非空字符串 id")
    live = [el for el in elements if isinstance(el, dict) and not el.get("isDeleted")]

    # 重复 id：渲染器会静默丢弃后出现的同 id 元素
    seen: set[str] = set()
    duplicated: set[str] = set()
    for el in live:
        el_id = el.get("id")
        if isinstance(el_id, str) and el_id:
            if el_id in seen:
                duplicated.add(el_id)
            seen.add(el_id)
    for el_id in sorted(duplicated):
        errors.append(f'重复元素 id "{el_id}"——渲染器会静默丢弃后出现的同 id 元素')

    by_id = {el.get("id"): el for el in live if isinstance(el.get("id"), str)}
    known = set(by_id)
    bound_ids: dict[str, set[str]] = {}
    for el_id, el in by_id.items():
        refs = set()
        for bound in el.get("boundElements") or []:
            if isinstance(bound, dict) and isinstance(bound.get("id"), str):
                refs.add(bound["id"])
        bound_ids[el_id] = refs

    # 悬空引用：任何指向其他元素的 id 都必须存在
    for el_id, el in by_id.items():
        for ref in bound_ids[el_id]:
            if ref not in known:
                errors.append(f'元素 "{el_id}" 的 boundElements 引用了不存在的 id "{ref}"')
        for side in ("startBinding", "endBinding"):
            binding = el.get(side)
            if isinstance(binding, dict):
                ref = binding.get("elementId")
                if isinstance(ref, str) and ref not in known:
                    errors.append(f'箭头 "{el_id}" 的 {side} 引用了不存在的 id "{ref}"')
        for key in ("containerId", "frameId"):
            ref = el.get(key)
            if isinstance(ref, str) and ref not in known:
                errors.append(f'元素 "{el_id}" 的 {key} 引用了不存在的 id "{ref}"')

    # 绑定一致性：单向声明（只改了一侧 boundElements / containerId）不致渲染失败，告警提示补齐
    for el_id, el in by_id.items():
        cid = el.get("containerId")
        if isinstance(cid, str) and cid in by_id and el_id not in bound_ids[cid]:
            warnings.append(f'文字 "{el_id}" 绑定容器 "{cid}"，但容器 boundElements 未回指'
                            "（跨区域绑定时漏改另一侧）")
        for bound in el.get("boundElements") or []:
            if not isinstance(bound, dict):
                continue
            ref = bound.get("id")
            if bound.get("type") == "text" and ref in by_id and by_id[ref].get("containerId") != el_id:
                warnings.append(f'容器 "{el_id}" 的 boundElements 声明文字 "{ref}"，'
                                "但该文字 containerId 未指向它")
        for side in ("startBinding", "endBinding"):
            binding = el.get(side)
            if isinstance(binding, dict) and isinstance(binding.get("elementId"), str):
                ref = binding["elementId"]
                if ref in by_id and el_id not in bound_ids[ref]:
                    warnings.append(f'箭头 "{el_id}" 的 {side} 绑定 "{ref}"，但对方 boundElements 未回指')

    # 溢出：绑定文字不得超出容器，frame 子元素不得超出 frame
    for el_id, el in by_id.items():
        box = element_bbox(el)
        if box is None:
            continue
        cid = el.get("containerId")
        if isinstance(cid, str):
            cbox = element_bbox(by_id[cid]) if cid in by_id else None
            if cbox is not None and not contains(cbox, box):
                errors.append(f'文字 "{el_id}" 溢出其容器 "{cid}"——缩小文字或放大容器')
        fid = el.get("frameId")
        if isinstance(fid, str):
            fbox = element_bbox(by_id[fid]) if fid in by_id else None
            if fbox is not None and not contains(fbox, box):
                errors.append(f'元素 "{el_id}" 溢出 frame "{fid}"——调整位置或放大 frame')

    # 重叠审计：arrow/line 是跨空间连线不参与；容器与 frame 本身不参与；
    # 完全包含属有意分层（徽标、绑定文字、代码块底板）不告警
    container_ids = {el.get("containerId") for el in by_id.values() if isinstance(el.get("containerId"), str)}
    frame_ids = {el.get("frameId") for el in by_id.values() if isinstance(el.get("frameId"), str)}
    shapes: list[tuple[str, tuple[float, float, float, float]]] = []
    for el_id, el in by_id.items():
        if el.get("type") in ("arrow", "line") or el_id in container_ids or el_id in frame_ids:
            continue
        box = element_bbox(el)
        if box is not None:
            shapes.append((el_id, box))

    reported: set[tuple[str, str]] = set()
    for i in range(len(shapes)):
        for j in range(i + 1, len(shapes)):
            id_a, box_a = shapes[i]
            id_b, box_b = shapes[j]
            if contains(box_a, box_b) or contains(box_b, box_a):
                continue
            ix = min(box_a[2], box_b[2]) - max(box_a[0], box_b[0])
            iy = min(box_a[3], box_b[3]) - max(box_a[1], box_b[1])
            if ix <= TOL or iy <= TOL:
                continue
            area_a = (box_a[2] - box_a[0]) * (box_a[3] - box_a[1])
            area_b = (box_b[2] - box_b[0]) * (box_b[3] - box_b[1])
            min_area = min(area_a, area_b)
            if min_area > 0 and ix * iy < min_area * OVERLAP_MIN_RATIO:
                continue
            pair = tuple(sorted((id_a, id_b)))
            if pair not in reported:
                reported.add(pair)
                warnings.append(f'元素 "{id_a}" 与 "{id_b}" 矩形重叠——'
                                "若非有意分层（Cloud 重叠椭圆、徽标压框）则调开")

    # 色值白名单：枚举源为同目录 color-palette.md（颜色唯一真相源）
    if palette is None:
        warnings.append("调色板文件 color-palette.md 不可读，跳过色值白名单检查")
    else:
        off_palette: dict[str, list[str]] = {}
        for el_id, el in by_id.items():
            for key in ("strokeColor", "backgroundColor"):
                color = normalize_color(el.get(key))
                if color in (None, "transparent"):
                    continue
                if color not in palette:
                    off_palette.setdefault(color, []).append(f"{el_id}.{key}")
        for color in sorted(off_palette):
            users = ", ".join(sorted(off_palette[color]))
            warnings.append(f"色值 {color} 不在调色板白名单（{users}）——"
                            "用 color-palette.md 的语义色，除非刻意定制")

    # 字号种类数：层级靠少量字号档位表达，种类泛滥即层次失控
    sizes = set()
    for el in by_id.values():
        if el.get("type") == "text" and isinstance(el.get("fontSize"), (int, float)):
            sizes.add(el["fontSize"])
    if len(sizes) > MAX_FONT_SIZES:
        listed = ", ".join(str(s) for s in sorted(sizes))
        warnings.append(f"字号共 {len(sizes)} 种（{listed}），超过上限 {MAX_FONT_SIZES}——"
                        "层级靠 3-4 档字号表达足够")

    return errors, warnings


def main() -> None:
    parser = argparse.ArgumentParser(description="Excalidraw 静态校验器（渲染前运行，纯标准库）")
    parser.add_argument("input", type=Path, help=".excalidraw JSON 文件路径")
    args = parser.parse_args()

    try:
        data = json.loads(args.input.read_text(encoding="utf-8"))
    except OSError as e:
        print(f"FAIL: 无法读取文件 {args.input}: {e}")
        sys.exit(1)
    except UnicodeDecodeError as e:
        print(f"FAIL: 文件不是合法 UTF-8 文本: {e}（.excalidraw 须以 UTF-8 保存）")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"FAIL: JSON 语法错误: {e}（语法层先过 jq . 这一道）")
        sys.exit(1)

    errors, warnings = validate(data, load_palette(SCRIPT_DIR / "color-palette.md"))
    for msg in errors:
        print(f"FAIL: {msg}")
    for msg in warnings:
        print(f"WARN: {msg}")
    if errors:
        print(f"结果：{len(errors)} FAIL / {len(warnings)} WARN——修复全部 FAIL 后再渲染")
        sys.exit(1)
    print(f"结果：0 FAIL / {len(warnings)} WARN——静态门禁通过，进入渲染视检")


if __name__ == "__main__":
    main()
