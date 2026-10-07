#!/usr/bin/env python3
"""视频脚本 shots.json 交付前确定性校验门（Mode 2）。

两段式工作流的第一段产物 shots.json 必须跑过本脚本且 0 FAIL，才允许渲染成
交付 Markdown；创作协作过程中的来回调整不跑门。每次校验的门结果累积追加到
.gates.jsonl（默认与被校验文件同目录，--gates 可覆盖），为回推提示词规范措辞攒数据。

FAIL 级是确定性数值规则：时长分档、运镜枚举与相邻变化、台词语速折算；
WARN 级是建议性规则：逐镜头旁白配置。运镜词枚举源为
references/guides/video-prompt-guidelines.md 五节"镜头语言"行，
类型划分与 references/guides/camera-movements.md 对照表的"类型"列一致。

纯标准库实现，跨平台。用法：
    python3 validate_video_script.py <shots.json 路径> [--gates <累积文件路径>]
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

# 枚举源是 guidelines 五节词表；ots 与 over-the-shoulder 为同一术语的两种写法。
# 改动词表须与两个 references 文件同步（tests 有同步 tripwire）。
CAMERA_MOTIONS = {
    "follows",
    "tracks",
    "pans",
    "circles around",
    "tilts",
    "pushes in",
    "pulls back",
    "overhead",
    "handheld",
    "ots",
    "over-the-shoulder",
    "static",
}

# 相邻运镜变化矩阵：词 → 运动类型。"禁连续 3 个同类型"按类型判定而非逐词判定
# （pans/tilts/pans 同属摇转，同样算连续），划分依据与 camera-movements.md 一致。
CAMERA_FAMILIES = {
    "follows": "跟随",
    "tracks": "跟随",
    "pans": "摇转",
    "tilts": "摇转",
    "pushes in": "推拉",
    "pulls back": "推拉",
    "circles around": "环绕",
    "overhead": "视角",
    "ots": "视角",
    "over-the-shoulder": "视角",
    "handheld": "手持",
    "static": "固定",
}

# 时长口径官方查证（2026-10-08，Lightricks 官方模型卡 LTX-2 与 LTX-2.3）：
# 官方未写死最大生成时长，参考配置 num_frames=121 @ frame_rate=24 ≈ 5.04s/次生成，
# 帧数须满足 8k+1；15s≈361 帧、12s≈289 帧均为该约束下可实现时长，
# 故本门值是分镜拆分策略上限，不是模型硬限。
DURATION_CAP_DEFAULT = 15
DURATION_CAP_SHORT = 12
SHORT_FILM_SECONDS = 60
SPEECH_UNITS_PER_SECOND = 5  # 中文自然语速约 3-5 字/秒，取上限口径，只在明显说不完时 FAIL
FOREIGN_TOKEN_UNITS = 2  # 一个英文单词/数字串的发音时长约折算 2 个中文单字

SHOT_FIELDS = ("id", "summary", "seconds", "shot_size", "camera_motion", "dialogue", "prompt")
ALLOWED_MOTION_TEXT = " / ".join(sorted(CAMERA_MOTIONS))

_CJK_RE = re.compile(r"[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uac00-\ud7a3]")
# 全角拉丁字母（Ａ-Ｚａ-ｚ）与半角同权，避免全角台词漏计而全角数字反被计入
_WORD_RE = re.compile(r"[A-Za-z\uFF21-\uFF3A\uFF41-\uFF5A]+")
_DIGIT_RE = re.compile(r"\d+")
_QUOTED_RES = (re.compile(r"“([^”]*)”"), re.compile(r"\"([^\"]*)\""))


def _nonempty_str(value) -> bool:
    return isinstance(value, str) and bool(value.strip())


def normalize_motion(value):
    """运镜词归一化：小写去空白后须命中词表，否则返回 None。"""
    if not isinstance(value, str):
        return None
    key = value.strip().lower()
    return key if key in CAMERA_MOTIONS else None


def shot_label(shot, index: int) -> str:
    shot_id = shot.get("id") if isinstance(shot, dict) else None
    if isinstance(shot_id, str) and shot_id.strip():
        return shot_id
    return f"第{index + 1}个镜头"


def spoken_text(dialogue: str) -> str:
    """只取引号内的台词参与语速折算；无引号则整个字段按台词算。"""
    matches = []
    for pattern in _QUOTED_RES:
        matches.extend(pattern.findall(dialogue))
    return "".join(matches) if matches else dialogue


def speech_units(text: str) -> int:
    """发音单位数：中日韩字符（含日文假名与韩文谚文）计 1，英文单词与数字串各计 2。"""
    return (
        len(_CJK_RE.findall(text))
        + len(_WORD_RE.findall(text)) * FOREIGN_TOKEN_UNITS
        + len(_DIGIT_RE.findall(text)) * FOREIGN_TOKEN_UNITS
    )


def duration_cap_for(total_seconds: float) -> int:
    if 0 < total_seconds <= SHORT_FILM_SECONDS:
        return DURATION_CAP_SHORT
    return DURATION_CAP_DEFAULT


def _valid_seconds(seconds) -> bool:
    return not isinstance(seconds, bool) and isinstance(seconds, (int, float)) and seconds > 0


def prepare(script):
    """结构校验并展平镜头。schema_errors 非空表示结构门未过，后续门按已有数据运行。"""
    ctx = {
        "shots": [],
        "schema_errors": [],
        "total_seconds": 0.0,
        "duration_cap": DURATION_CAP_DEFAULT,
    }
    if not isinstance(script, dict):
        ctx["schema_errors"].append("顶层必须是 JSON 对象")
        return ctx
    for field in ("title", "logline", "style"):
        if not _nonempty_str(script.get(field)):
            ctx["schema_errors"].append(
                f"顶层缺少 {field}（渲染交付 Markdown 时直接取用，必须写在 shots.json 里）"
            )
    shots = script.get("shots")
    if not isinstance(shots, list) or not shots:
        ctx["schema_errors"].append("顶层缺少非空 shots 数组")
        return ctx

    seg_of = {}
    valid_segments = []
    segments = script.get("segments")
    if segments is not None:
        if not isinstance(segments, list):
            ctx["schema_errors"].append("segments 必须是数组")
        else:
            seen_segments = set()
            for i, seg in enumerate(segments):
                if (
                    not isinstance(seg, dict)
                    or not _nonempty_str(seg.get("id"))
                    or not isinstance(seg.get("shot_ids"), list)
                    or not seg["shot_ids"]
                ):
                    ctx["schema_errors"].append(f"segments[{i}] 需要 id 与非空 shot_ids")
                    continue
                if seg["id"] in seen_segments:
                    ctx["schema_errors"].append(f"segment id 重复：{seg['id']}")
                seen_segments.add(seg["id"])
                valid_segments.append((seg["id"], seg["shot_ids"]))
                for shot_id in seg["shot_ids"]:
                    if not isinstance(shot_id, str) or not shot_id.strip():
                        ctx["schema_errors"].append(f"segment {seg['id']} 的 shot_ids 含空项")
                    else:
                        seg_of.setdefault(shot_id, seg["id"])

    seen_ids = set()
    for index, shot in enumerate(shots):
        if not isinstance(shot, dict):
            ctx["schema_errors"].append(f"shots[{index}] 必须是对象")
            continue
        label = shot_label(shot, index)
        for field in SHOT_FIELDS:
            if field not in shot:
                ctx["schema_errors"].append(f"{label}：缺少字段 {field}")
        # 字段存在才做类型校验，避免与上面的"缺少字段"对同一缺失双报
        shot_id = shot.get("id")
        if _nonempty_str(shot_id):
            if shot_id in seen_ids:
                ctx["schema_errors"].append(f"{label}：id 重复（{shot_id}）")
            else:
                seen_ids.add(shot_id)
        elif "id" in shot:
            ctx["schema_errors"].append(f"{label}：id 必须是非空字符串")
        seconds = shot.get("seconds")
        if _valid_seconds(seconds):
            ctx["total_seconds"] += seconds
        elif "seconds" in shot:
            ctx["schema_errors"].append(f"{label}：seconds 必须是大于 0 的数字，当前 {seconds!r}")
        for field in ("summary", "shot_size", "prompt"):
            if field in shot and not _nonempty_str(shot[field]):
                ctx["schema_errors"].append(f"{label}：{field} 必须是非空字符串")
        if "camera_motion" in shot and not _nonempty_str(shot["camera_motion"]):
            ctx["schema_errors"].append(f"{label}：camera_motion 必须是非空字符串")
        if "dialogue" in shot and not isinstance(shot["dialogue"], str):
            ctx["schema_errors"].append(f"{label}：dialogue 必须是字符串（无台词显式写“无”）")
        ctx["shots"].append(
            {
                "label": label,
                "shot": shot,
                "segment": seg_of.get(shot["id"]) if _nonempty_str(shot.get("id")) else None,
            }
        )
    for seg_id, shot_ids in valid_segments:
        for shot_id in shot_ids:
            if isinstance(shot_id, str) and shot_id.strip() and shot_id not in seen_ids:
                ctx["schema_errors"].append(f"segment {seg_id} 引用了不存在的镜头：{shot_id}")
    ctx["duration_cap"] = duration_cap_for(ctx["total_seconds"])
    return ctx


def _result(gate: str, level: str, passed: bool, messages: list) -> dict:
    return {"gate": gate, "level": level, "passed": passed, "messages": messages}


def gate_schema(ctx) -> dict:
    return _result("schema", "fail", not ctx["schema_errors"], list(ctx["schema_errors"]))


def gate_duration_cap(ctx) -> dict:
    cap = ctx["duration_cap"]
    tier = f"成片 ≤{SHORT_FILM_SECONDS}s 档" if cap == DURATION_CAP_SHORT else "默认档"
    messages = []
    for entry in ctx["shots"]:
        seconds = entry["shot"].get("seconds")
        if _valid_seconds(seconds) and seconds > cap:
            messages.append(
                f"{entry['label']}：{seconds}s 超过当前档上限 {cap}s（{tier}）——把这一镜头拆成两个"
            )
    return _result("duration-cap", "fail", not messages, messages)


def gate_camera_enum(ctx) -> dict:
    messages = []
    for entry in ctx["shots"]:
        value = entry["shot"].get("camera_motion")
        if not _nonempty_str(value):
            continue  # 结构门已报缺失/类型错误，这里不重复
        if normalize_motion(value) is None:
            messages.append(
                f"{entry['label']}：camera_motion “{value}” 不在运镜词表内，可选：{ALLOWED_MOTION_TEXT}"
            )
    return _result("camera-enum", "fail", not messages, messages)


def gate_camera_variation(ctx) -> dict:
    families = [
        CAMERA_FAMILIES.get(normalize_motion(entry["shot"].get("camera_motion")))
        for entry in ctx["shots"]
    ]
    messages = []
    for i in range(len(families) - 2):
        if families[i] and families[i] == families[i + 1] == families[i + 2]:
            labels = [ctx["shots"][j]["label"] for j in (i, i + 1, i + 2)]
            messages.append(
                f"{labels[0]}、{labels[1]}、{labels[2]}：同类型运镜（{families[i]}）连续 3 个——"
                "相邻镜头运镜要有变化，从词表里换其他类型"
            )
    return _result("camera-variation", "fail", not messages, messages)


def gate_dialogue_rate(ctx) -> dict:
    messages = []
    for entry in ctx["shots"]:
        shot = entry["shot"]
        dialogue = shot.get("dialogue")
        seconds = shot.get("seconds")
        if not isinstance(dialogue, str) or not _valid_seconds(seconds):
            continue  # 结构门已报，这里不重复
        units = speech_units(spoken_text(dialogue))
        if units == 0:
            continue
        budget = seconds * SPEECH_UNITS_PER_SECOND
        if units > budget:
            need = units / SPEECH_UNITS_PER_SECOND
            messages.append(
                f"{entry['label']}：台词约 {units} 个发音单位，按 {SPEECH_UNITS_PER_SECOND} 单位/秒"
                f"需 {need:.1f}s，超过镜头时长 {seconds}s——删减台词或加长镜头"
            )
    return _result("dialogue-rate", "fail", not messages, messages)


def gate_dialogue_presence(ctx) -> dict:
    messages = []
    for entry in ctx["shots"]:
        dialogue = entry["shot"].get("dialogue")
        if isinstance(dialogue, str) and not dialogue.strip():
            messages.append(
                f"{entry['label']}：dialogue 为空——建议补旁白/台词/环境音，确无音频则显式写“无”"
            )
    return _result("dialogue-presence", "warn", not messages, messages)


GATES = (
    gate_schema,
    gate_duration_cap,
    gate_camera_enum,
    gate_camera_variation,
    gate_dialogue_rate,
    gate_dialogue_presence,
)


def validate_script(script):
    """返回 (gates, stats)。gates 为每道门的结果，stats 为镜头数/总时长/当前档上限。"""
    ctx = prepare(script)
    gates = [gate(ctx) for gate in GATES]
    stats = {
        "shot_count": len(ctx["shots"]),
        "total_seconds": round(ctx["total_seconds"], 2),
        "duration_cap": ctx["duration_cap"],
    }
    return gates, stats


def verdict_of(gates) -> str:
    if any(not gate["passed"] and gate["level"] == "fail" for gate in gates):
        return "fail"
    if any(not gate["passed"] for gate in gates):
        return "warn"
    return "pass"


def build_record(source: str, gates: list, stats: dict) -> dict:
    return {
        "timestamp": datetime.now().astimezone().isoformat(timespec="seconds"),
        "file": source,
        "verdict": verdict_of(gates),
        "fail_count": sum(1 for g in gates if g["level"] == "fail" and not g["passed"]),
        "warn_count": sum(1 for g in gates if g["level"] == "warn" and not g["passed"]),
        **stats,
        "gates": gates,
    }


def append_gates_log(gates_path: Path, record: dict) -> None:
    gates_path.parent.mkdir(parents=True, exist_ok=True)
    with gates_path.open("a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def format_report(source: str, gates: list, stats: dict, gates_path: Path) -> str:
    tier = (
        f"（成片 ≤{SHORT_FILM_SECONDS}s 档）"
        if stats["duration_cap"] == DURATION_CAP_SHORT
        else "（默认档）"
    )
    lines = [
        f"校验：{source}",
        f"镜头数：{stats['shot_count']}｜总时长：{stats['total_seconds']}s｜"
        f"单镜头上限：{stats['duration_cap']}s{tier}",
    ]
    for gate in gates:
        if gate["passed"]:
            continue
        marker = "WARN" if gate["level"] == "warn" else "FAIL"
        for message in gate["messages"]:
            lines.append(f"{marker} [{gate['gate']}] {message}")
    verdict = verdict_of(gates)
    fail_n = sum(1 for g in gates if g["level"] == "fail" and not g["passed"])
    warn_n = sum(1 for g in gates if g["level"] == "warn" and not g["passed"])
    verdict_text = {"fail": "未通过", "warn": "通过（含建议项）", "pass": "通过"}[verdict]
    passed_text = "、".join(g["gate"] for g in gates if g["passed"]) or "无"
    lines.append(f"结果：{verdict_text}（FAIL {fail_n} 项，WARN {warn_n} 项）｜通过的门：{passed_text}")
    lines.append(f"门结果已追加：{gates_path}")
    return "\n".join(lines)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="校验视频脚本 shots.json：交付前确定性硬门（FAIL 阻断渲染，WARN 只提示）"
    )
    parser.add_argument("shots", help="shots.json 文件路径")
    parser.add_argument(
        "--gates",
        default=None,
        help="门结果累积文件路径，默认为被校验文件同目录的 .gates.jsonl",
    )
    args = parser.parse_args(argv)

    path = Path(args.shots)
    if not path.is_file():
        print(f"Error: shots.json 不存在或不是文件：{path}", file=sys.stderr)
        return 1
    try:
        script = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        print(f"Error: shots.json 读取或解析失败：{exc}", file=sys.stderr)
        return 1

    gates, stats = validate_script(script)
    gates_path = Path(args.gates) if args.gates else path.parent / ".gates.jsonl"
    append_gates_log(gates_path, build_record(str(path), gates, stats))
    print(format_report(str(path), gates, stats, gates_path))
    return 1 if verdict_of(gates) == "fail" else 0


if __name__ == "__main__":
    sys.exit(main())
