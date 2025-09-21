from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable, Optional

from pathvalidate import sanitize_filename

from . import settings


_TRUE_VALUES = {"1", "true", "yes", "on"}
_FALSE_VALUES = {"0", "false", "no", "off"}


def config_path(key: str) -> Path:
    """Return the resolved path for a configured directory value."""
    raw_value = settings.get_setting(key) or "."
    path = Path(raw_value).expanduser()
    return path if path.is_absolute() else Path.cwd() / path


def parse_bool(value: str | bool | None) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    normalized = value.strip().lower()
    if not normalized:
        return False
    if normalized in _TRUE_VALUES:
        return True
    if normalized in _FALSE_VALUES:
        return False
    return bool(normalized)


def should_overwrite() -> bool:
    no_overwrite = parse_bool(settings.get_setting("no_overwrite"))
    return not no_overwrite


def default_token_count() -> int:
    value = settings.get_setting("token_count")
    try:
        return int(value)
    except (TypeError, ValueError):
        return 10000


def ensure_directory(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def auto_filename(parts: Iterable[Optional[str]], extension: str) -> str:
    segments: list[str] = []
    for part in parts:
        if not part:
            continue
        sanitized = (
            sanitize_filename(str(part), replacement_text="_")
            .replace(" ", "_")
            .strip("._")
        )
        if sanitized:
            segments.append(sanitized)
    stem = "_".join(segments) if segments else "output"
    return f"{stem}.{extension.lstrip('.')}"


def write_json(path: Path, data: Any) -> None:
    ensure_directory(path.parent)
    path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def render_path(base_dir: Path, filename: str) -> Path:
    return base_dir / filename
