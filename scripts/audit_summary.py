#!/usr/bin/env python3
"""
总结产物机械审计：覆盖率地板 + 退化重复 tripwire + deep-dive 有效字符下限。

三项检查当前全部 WARN 级（先观察真实误报率，再决定是否定档 FAIL）：
- coverage：总结有效字符 ÷ 输入有效字符，地板 0.10。该地板是冷启动借用值
  （借自上游真实语料的兜底位，仅触底约 2% 正常输出），尚未用 cangjie 真实
  输出校准；累计跑 ≥20 篇真实输出后按覆盖率分布的 P2 分位重定，不要长期沿用。
- repetition：同一内容行出现 ≥4 次，或字符级 8-gram 多样性 <0.70（沿用上游
  实测口径），专防"灌水重复骗过覆盖率地板"。
- deep-dive：--density deep-dive 时总结有效字符 <3000 告警，为保守冷启动值。

有效字符口径：剥离 frontmatter / 围栏代码块 / 图嵌（图片语法与 img 标签）/
时间戳 / URL / HTML 注释后，去除全部空白字符计数；中英文同口径按字符计。

豁免清单：剧本、诗歌等行数天然稀疏或高比例复用原文的输入形态，覆盖率地板
不适用；脚本不做自动判定，由调用方以 --exempt coverage 显式声明并留痕。

用法：
    python3 audit_summary.py <summary.md> <input.md> [--density deep-dive] \
        [--exempt coverage] [--json]

退出码：0 = 无 FAIL；1 = 文件不可读；2 = 出现 FAIL 级（当前规则无 FAIL，保留给定档后）。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

COVERAGE_FLOOR = 0.10
REPEAT_LINE_THRESHOLD = 4
GRAM_DIVERSITY_FLOOR = 0.70
GRAM_SIZE = 8
DEEP_DIVE_MIN_CHARS = 3000
# 文本去空白后短于该值时 8-gram 窗口过少（<64 个），多样性无统计意义，跳过
MIN_GRAM_TEXT_CHARS = GRAM_SIZE * 8

EXEMPT_CHOICES = ("coverage", "repetition", "deep-dive")
DENSITY_CHOICES = ("brief", "standard-detailed", "deep-dive")

_FRONTMATTER_SEP = re.compile(r"^---\s*$")
_IMAGE = re.compile(r"!\[[^\]]*\]\([^)]*\)")
_IMG_TAG = re.compile(r"<img\b[^>]*>", re.IGNORECASE)
_URL = re.compile(r"https?://\S+")
_TS_BRACKET = re.compile(r"\[\d{1,2}:\d{2}(?::\d{2})?(?:[.,]\d+)?\]")
_TS_FULL = re.compile(r"\b\d{1,2}:\d{2}:\d{2}\b")
_TS_LEADING = re.compile(r"^\d{1,2}:\d{2}(?::\d{2})?\s+")
# 表格分隔行 / 水平线：只含 |、-、:、空格，属合法 Markdown 结构，不算重复内容行
_TABLE_DIVIDER = re.compile(r"^[\s|:-]+$")


def _strip_html_comments(line: str, in_comment: bool) -> tuple[str, bool]:
    """剥离一行内的 HTML 注释，返回 (剩余文本, 是否仍处于未闭合注释中)。

    注释可跨行：in_comment 在行间衔接，未闭合的注释剥到行尾并延续到后续行。
    """
    kept: list[str] = []
    while True:
        if in_comment:
            end = line.find("-->")
            if end < 0:
                return "".join(kept), True
            line = line[end + 3:]
            in_comment = False
            continue
        start = line.find("<!--")
        if start < 0:
            kept.append(line)
            return "".join(kept), in_comment
        kept.append(line[:start])
        line = line[start + 4:]
        in_comment = True


def strip_noise(text: str) -> str:
    """剥离 frontmatter、围栏代码块、图嵌、时间戳、URL 与 HTML 注释（含跨行注释）。"""
    lines = text.splitlines()
    start = 0
    if lines and _FRONTMATTER_SEP.match(lines[0]):
        start = 1
        while start < len(lines) and not _FRONTMATTER_SEP.match(lines[start]):
            start += 1
        start += 1  # 闭合分隔行也跳过；未闭合则 start 越界，等价于全文剥离

    out = []
    in_fence = False
    in_comment = False
    for line in lines[start:]:
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        line, in_comment = _strip_html_comments(line, in_comment)
        line = _IMAGE.sub("", line)
        line = _IMG_TAG.sub("", line)
        line = _URL.sub("", line)
        line = _TS_BRACKET.sub("", line)
        line = _TS_FULL.sub("", line)
        line = _TS_LEADING.sub("", line)
        out.append(line)
    return "\n".join(out)


def effective_chars(text: str) -> int:
    """有效字符数：剥离噪音后去除全部空白字符，中英文同口径按字符计。"""
    return len(re.sub(r"\s+", "", strip_noise(text)))


def repeated_lines(text: str, threshold: int = REPEAT_LINE_THRESHOLD) -> list[tuple[str, int]]:
    """返回出现次数 ≥ threshold 的内容行（按次数降序），表格分隔行与水平线不算。"""
    counts: dict[str, int] = {}
    for raw in strip_noise(text).splitlines():
        line = raw.strip()
        if not line or _TABLE_DIVIDER.match(line):
            continue
        counts[line] = counts.get(line, 0) + 1
    hits = [(line, n) for line, n in counts.items() if n >= threshold]
    hits.sort(key=lambda item: item[1], reverse=True)
    return hits


def gram_diversity(text: str) -> tuple[float, int]:
    """字符级 8-gram 多样性（去空白后）：unique 窗口数 / 总窗口数。

    返回 (多样性, 总窗口数)；文本过短时返回 (1.0, 0) 表示检查不适用。
    """
    compact = re.sub(r"\s+", "", strip_noise(text))
    if len(compact) < MIN_GRAM_TEXT_CHARS:
        return 1.0, 0
    total = len(compact) - GRAM_SIZE + 1
    grams = {compact[i:i + GRAM_SIZE] for i in range(total)}
    return len(grams) / total, total


def audit(
    summary_text: str,
    input_text: str,
    density: str | None = None,
    exempt: "list[str] | tuple[str, ...]" = (),
) -> list[dict]:
    """对总结产物跑全部检查，返回 [{name, status, detail}]，status ∈ PASS/WARN/SKIP。"""
    results = []
    s_chars = effective_chars(summary_text)
    i_chars = effective_chars(input_text)

    if "coverage" in exempt:
        results.append({
            "name": "coverage",
            "status": "SKIP",
            "detail": "输入形态属豁免清单（剧本/诗歌等），覆盖率地板不适用",
        })
    elif i_chars == 0:
        results.append({
            "name": "coverage",
            "status": "SKIP",
            "detail": "输入有效字符为 0，无法计算覆盖率",
        })
    else:
        ratio = s_chars / i_chars
        if ratio < COVERAGE_FLOOR:
            results.append({
                "name": "coverage",
                "status": "WARN",
                "detail": (
                    f"覆盖率 {ratio:.2f} 低于地板 {COVERAGE_FLOOR}"
                    f"（总结 {s_chars} / 输入 {i_chars} 有效字符）；"
                    "先人工判断是漏了还是输入形态天然稀疏，勿自动凑字数"
                ),
            })
        else:
            results.append({
                "name": "coverage",
                "status": "PASS",
                "detail": f"覆盖率 {ratio:.2f} ≥ {COVERAGE_FLOOR}（总结 {s_chars} / 输入 {i_chars} 有效字符）",
            })

    if "repetition" in exempt:
        results.append({
            "name": "repetition",
            "status": "SKIP",
            "detail": "调用方声明豁免（如剧本对白结构天然重复）",
        })
    else:
        problems = []
        reps = repeated_lines(summary_text)
        if reps:
            top = "；".join(f"「{line[:30]}」×{n}" for line, n in reps[:3])
            problems.append(f"同一内容行 ≥{REPEAT_LINE_THRESHOLD} 次：{top}")
        diversity, gram_total = gram_diversity(summary_text)
        if gram_total and diversity < GRAM_DIVERSITY_FLOOR:
            problems.append(f"字符 {GRAM_SIZE}-gram 多样性 {diversity:.2f} < {GRAM_DIVERSITY_FLOOR}")
        if problems:
            results.append({
                "name": "repetition",
                "status": "WARN",
                "detail": "疑似退化重复/灌水：" + "；".join(problems) + "；优先删重复段落，勿靠新增凑字数",
            })
        else:
            results.append({
                "name": "repetition",
                "status": "PASS",
                "detail": f"无 ≥{REPEAT_LINE_THRESHOLD} 次重复行；8-gram 多样性达标",
            })

    if density == "deep-dive":
        if "deep-dive" in exempt:
            results.append({
                "name": "deep-dive",
                "status": "SKIP",
                "detail": "图表/公式密集型论文等豁免场景，下限不适用",
            })
        elif s_chars < DEEP_DIVE_MIN_CHARS:
            results.append({
                "name": "deep-dive",
                "status": "WARN",
                "detail": (
                    f"deep-dive 有效字符 {s_chars} < {DEEP_DIVE_MIN_CHARS}；"
                    "补证据密度（方法/结果/局限细节）而非拉长空话"
                ),
            })
        else:
            results.append({
                "name": "deep-dive",
                "status": "PASS",
                "detail": f"deep-dive 有效字符 {s_chars} ≥ {DEEP_DIVE_MIN_CHARS}",
            })

    return results


def _read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        print(f"Error: cannot read {path}: {exc}", file=sys.stderr)
        return None


def main(argv: "list[str] | None" = None) -> int:
    parser = argparse.ArgumentParser(description="总结产物机械审计（覆盖率/退化重复/deep-dive 下限）")
    parser.add_argument("summary", help="总结产物 .md 路径")
    parser.add_argument("input", help="原始输入（转录稿/原文）路径")
    parser.add_argument("--density", choices=DENSITY_CHOICES, help="输出密度档；deep-dive 时追加字数下限检查")
    parser.add_argument("--exempt", action="append", default=[], choices=EXEMPT_CHOICES,
                        help="声明豁免的检查项，可多次使用（如剧本/诗歌输入 --exempt coverage）")
    parser.add_argument("--json", action="store_true", help="输出 JSON 结果")
    args = parser.parse_args(argv)

    summary_path = Path(args.summary)
    input_path = Path(args.input)
    summary_text = _read_text(summary_path)
    input_text = _read_text(input_path)
    if summary_text is None or input_text is None:
        return 1

    results = audit(summary_text, input_text, density=args.density, exempt=args.exempt)
    warn_count = sum(1 for r in results if r["status"] == "WARN")
    fail_count = sum(1 for r in results if r["status"] == "FAIL")

    if args.json:
        print(json.dumps({
            "summary_effective_chars": effective_chars(summary_text),
            "input_effective_chars": effective_chars(input_text),
            "checks": results,
            "warn_count": warn_count,
            "fail_count": fail_count,
        }, ensure_ascii=False, indent=2))
    else:
        for r in results:
            print(f"[{r['status']}] {r['name']}: {r['detail']}")
        print(f"结论：{warn_count} WARN / {fail_count} FAIL；WARN 项人工判断是否补充，勿自动凑字数")

    return 2 if fail_count else 0


if __name__ == "__main__":
    sys.exit(main())
