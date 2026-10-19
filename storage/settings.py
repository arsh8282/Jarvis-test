"""Validated JSON settings store. Pure Python, no Kivy, so it is unit-testable."""
from __future__ import annotations

import json
import logging
import os
from typing import Any

log = logging.getLogger("jarvis.settings")

ALLOWED: dict[str, tuple[str, ...]] = {
    "theme": ("dark", "light"),
    "accent": ("cyan", "teal", "blue"),
    "text_size": ("small", "medium", "large"),
}
DEFAULTS: dict[str, str] = {"theme": "dark", "accent": "cyan", "text_size": "medium"}


class SettingsStore:
    def __init__(self, path: str) -> None:
        self.path = path
        self._data: dict[str, str] = dict(DEFAULTS)
        self._load()

    def _load(self) -> None:
        if not os.path.exists(self.path):
            return
        try:
            with open(self.path, "r", encoding="utf-8") as fh:
                raw = json.load(fh)
            if not isinstance(raw, dict):
                raise ValueError("settings file is not a JSON object")
        except (OSError, ValueError) as exc:
            log.warning("Ignoring unreadable settings file: %s", exc)
            return
        for key, value in raw.items():
            if key in ALLOWED and value in ALLOWED[key]:
                self._data[key] = value

    def get(self, key: str) -> str:
        return self._data[key]

    def set(self, key: str, value: Any) -> None:
        if key not in ALLOWED:
            raise KeyError(f"Unknown setting: {key}")
        if value not in ALLOWED[key]:
            raise ValueError(f"Invalid value {value!r} for {key}")
        self._data[key] = value
        self.save()

    def save(self) -> None:
        os.makedirs(os.path.dirname(self.path) or ".", exist_ok=True)
        tmp = self.path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(self._data, fh, indent=2)
        os.replace(tmp, self.path)  # atomic: never leaves a half-written file
