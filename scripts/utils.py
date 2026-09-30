#!/usr/bin/env python3
"""
Shared utilities for cangjie audio processing scripts.
"""

from datetime import timedelta
from pathlib import Path
import sys


def format_timestamp(seconds: float) -> str:
    """Format timestamp as HH:MM:SS"""
    td = timedelta(seconds=seconds)
    text = str(td).split(".")[0]
    # str(timedelta) 对 ≥24h 会写成 "1 day, H:MM:SS"，违反 HH:MM:SS 契约；
    # 折算回总小时数。负数（不应出现）保持原样，不做折算。
    if "day" in text and not text.startswith("-"):
        days, _, rest = text.partition(", ")
        hours = int(days.split(" ", 1)[0]) * 24 + int(rest.partition(":")[0])
        text = f"{hours}:{rest.partition(':')[2]}"
    return text


def validate_audio_file(audio_path: str) -> Path:
    """Validate that an audio file exists and return its resolved Path."""
    p = Path(audio_path).resolve()
    if not p.exists():
        print(f"Error: Audio file not found: {p}", file=sys.stderr)
        sys.exit(1)
    if not p.is_file():
        print(f"Error: Not a file: {p}", file=sys.stderr)
        sys.exit(1)
    return p


def ensure_output_dir(output_path: str) -> Path:
    """Ensure the parent directory of output_path exists."""
    p = Path(output_path).resolve()
    p.parent.mkdir(parents=True, exist_ok=True)
    return p
