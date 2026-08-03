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
    return str(td).split(".")[0]


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
