"""Assistant engines. Phase 1 ships an honest placeholder; Phase 2 adds Gemini."""
from __future__ import annotations

from typing import Any, Protocol


class AssistantEngine(Protocol):
    def reply(self, history: list[dict[str, Any]], text: str) -> str: ...


class PlaceholderEngine:
    """Does not pretend to be an AI. It only confirms the message was received."""

    def reply(self, history: list[dict[str, Any]], text: str) -> str:
        return (
            "Understood, Sir. Your message was received, but the Gemini connection "
            "is not built yet, so I cannot answer it. That arrives in Phase 2."
        )
