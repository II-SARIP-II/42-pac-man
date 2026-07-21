from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Iterable, List


def ensure_directory(path: str) -> None:
    """Create a directory (and any missing parents) if it doesn't exist.

    Args:
        path (str): Path of the directory to ensure exists.

    Returns:
        None.

    Raises:
        OSError: If the directory could not be created.
    """
    try:
        os.makedirs(path, exist_ok=True)
    except OSError as e:
        raise OSError(f"Could not create directory {path}: {e}") from e


def load_json_file(path: str) -> Any:
    """Load and parse a JSON file, stripping `#`-style comment lines.

    Args:
        path (str): Path of the JSON file.

    Returns:
        Any: The parsed JSON content.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the content is not valid JSON.
        PermissionError: If the file cannot be read.
    """
    p = Path(path)
    if not p.is_file():
        raise FileNotFoundError(f"File not found: {path}")
    try:
        with p.open("r", encoding="utf-8") as f:
            content = re.sub(r"\s*#.*", "", f.read())
            return json.loads(content)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in {path}: {e}") from e
    except PermissionError as e:
        raise PermissionError(f"Permission denied reading {path}: {e}") from e


def read_jsonl(path: str) -> List[dict[Any, Any]]:
    """Read a JSONL file into a list of objects, skipping bad lines.

    Args:
        path (str): Path of the JSONL file.

    Returns:
        List[dict[Any, Any]]: The successfully parsed objects.

    Raises:
        FileNotFoundError: If the file does not exist.
        PermissionError: If the file cannot be read.
    """
    p = Path(path)
    if not p.is_file():
        raise FileNotFoundError(f"File not found: {path}")

    results: List[dict[Any, Any]] = []
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
    """Read the entire contents of a text file.

    Args:
        path (str): Path of the file.

    Returns:
        str: The file's text content.

    Raises:
        FileNotFoundError: If the file does not exist.
        PermissionError: If the file cannot be read.
    """
    p = Path(path)
    if not p.is_file():
        raise FileNotFoundError(f"File not found: {path}")
    try:
        with p.open("r", encoding="utf-8") as f:
            return f.read()
    except PermissionError as e:
        raise PermissionError(f"Permission denied reading {path}: {e}") from e


def append_jsonl(records: Iterable[dict[Any, Any]], path: str) -> None:
    """Append a sequence of records to a JSONL file.

    Args:
        records (Iterable[dict[Any, Any]]): Records to append.
        path (str): Path of the JSONL file.

    Returns:
        None.

    Raises:
        OSError: If the file could not be written to.
    """
    p = Path(path)
    ensure_directory(str(p.parent))
    try:
        with p.open("a", encoding="utf-8") as f:
            for r in records:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
    except OSError as e:
        raise OSError(f"Could not append to {path}: {e}") from e


def write_json_file(obj: Any, path: str) -> None:
    """Write an object to a file as pretty-printed JSON.

    Args:
        obj (Any): JSON-serializable object to write.
        path (str): Path of the file.

    Returns:
        None.

    Raises:
        OSError: If the file could not be written to.
    """
    p = Path(path)
    ensure_directory(str(p.parent))
    try:
        with p.open("w", encoding="utf-8") as f:
            json.dump(obj, f, indent=2, ensure_ascii=False)
    except OSError as e:
        raise OSError(f"Could not write JSON to {path}: {e}") from e


def write_text_file(text: str, path: str) -> None:
    """Write text content to a file.

    Args:
        text (str): Text to write.
        path (str): Path of the file.

    Returns:
        None.

    Raises:
        OSError: If the file could not be written to.
    """
    p = Path(path)
    ensure_directory(str(p.parent))
    try:
        with p.open("w", encoding="utf-8") as f:
            f.write(text)
    except OSError as e:
        raise OSError(f"Could not write to {path}: {e}") from e


def resource_path(relative_path: str) -> str:
    """Resolve a path relative to the app's base directory.

    Args:
        relative_path (str): Path relative to the base directory.

    Returns:
        str: The resolved absolute path.
    """
    if '__compiled__' in globals():
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)
