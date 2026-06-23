from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Iterable, List


def ensure_directory(path: str) -> None:
    """Create directory if missing, raise OSError on failure."""
    try:
        os.makedirs(path, exist_ok=True)
    except OSError as e:
        raise OSError(f"Could not create directory {path}: {e}") from e


def load_json_file(path: str) -> Any:
    """Load and return JSON from a file.

    Raises FileNotFoundError, ValueError (for invalid JSON) or PermissionError.
    """
    p = Path(path)
    if not p.is_file():
        raise FileNotFoundError(f"File not found: {path}")
    try:
        with p.open("r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in {path}: {e}") from e
    except PermissionError as e:
        raise PermissionError(f"Permission denied reading {path}: {e}") from e


def read_jsonl(path: str) -> List[dict]:
    """Read a JSONL file and return a list of parsed objects.

    Malformed lines are skipped with a printed warning.
    Raises FileNotFoundError or PermissionError when appropriate.
    """
    p = Path(path)
    if not p.is_file():
        raise FileNotFoundError(f"File not found: {path}")

    results: List[dict] = []
    try:
        with p.open("r", encoding="utf-8") as f:
            for i, line in enumerate(f, start=1):
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                    results.append(obj)
                except json.JSONDecodeError as e:
                    print(f"Skipping malformed JSONL line {i} in {path}: {e}")
    except PermissionError as e:
        raise PermissionError(f"Permission denied reading {path}: {e}") from e

    return results


def read_text_file(path: str) -> str:
    """Read entire text file and return its contents.

    Raises FileNotFoundError or PermissionError.
    """
    p = Path(path)
    if not p.is_file():
        raise FileNotFoundError(f"File not found: {path}")
    try:
        with p.open("r", encoding="utf-8") as f:
            return f.read()
    except PermissionError as e:
        raise PermissionError(f"Permission denied reading {path}: {e}") from e


def append_jsonl(records: Iterable[dict], path: str) -> None:
    """Append records (dicts) to a JSONL file,
    creating parent dir if needed."""
    p = Path(path)
    ensure_directory(str(p.parent))
    try:
        with p.open("a", encoding="utf-8") as f:
            for r in records:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
    except OSError as e:
        raise OSError(f"Could not append to {path}: {e}") from e


def write_json_file(obj: Any, path: str) -> None:
    """Write an object as pretty JSON to a file,
     creating parent dir if needed."""
    p = Path(path)
    ensure_directory(str(p.parent))
    try:
        with p.open("w", encoding="utf-8") as f:
            json.dump(obj, f, indent=2, ensure_ascii=False)
    except OSError as e:
        raise OSError(f"Could not write JSON to {path}: {e}") from e


def write_text_file(text: str, path: str) -> None:
    """Write text to a file, creating parent dir if needed."""
    p = Path(path)
    ensure_directory(str(p.parent))
    try:
        with p.open("w", encoding="utf-8") as f:
            f.write(text)
    except OSError as e:
        raise OSError(f"Could not write to {path}: {e}") from e
