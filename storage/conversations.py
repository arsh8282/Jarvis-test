"""Local conversation history. Pure Python, no Kivy."""
from __future__ import annotations

import json
import logging
import os
import time
import uuid
from typing import Any

log = logging.getLogger("jarvis.conversations")
DEFAULT_TITLE = "New chat"


class ConversationStore:
    def __init__(self, path: str, max_messages: int = 500) -> None:
        self.path = path
        self.max_messages = max_messages
        self.conversations: list[dict[str, Any]] = []
        self.active_id: str | None = None
        self._load()

    # ---- persistence -------------------------------------------------
    def _load(self) -> None:
        if not os.path.exists(self.path):
            return
        try:
            with open(self.path, "r", encoding="utf-8") as fh:
                raw = json.load(fh)
            self.conversations = [c for c in raw["conversations"] if "id" in c and "messages" in c]
            self.active_id = raw.get("active_id")
        except (OSError, ValueError, KeyError, TypeError) as exc:
            log.warning("History unreadable (%s); keeping a .bad copy and starting fresh", exc)
            try:
                os.replace(self.path, self.path + ".bad")
            except OSError:
                pass
            self.conversations, self.active_id = [], None

    def save(self) -> None:
        os.makedirs(os.path.dirname(self.path) or ".", exist_ok=True)
        tmp = self.path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump({"active_id": self.active_id, "conversations": self.conversations}, fh)
        os.replace(tmp, self.path)

    # ---- queries -----------------------------------------------------
    def get(self, conv_id: str) -> dict[str, Any] | None:
        return next((c for c in self.conversations if c["id"] == conv_id), None)

    @property
    def active(self) -> dict[str, Any]:
        conv = self.get(self.active_id) if self.active_id else None
        return conv or self.new_conversation()

    def summaries(self) -> list[dict[str, Any]]:
        ordered = sorted(self.conversations, key=lambda c: c["updated"], reverse=True)
        return [{"id": c["id"], "title": c["title"], "count": len(c["messages"])} for c in ordered]

    # ---- changes -----------------------------------------------------
    def new_conversation(self, title: str = DEFAULT_TITLE) -> dict[str, Any]:
        conv = {"id": uuid.uuid4().hex[:8], "title": title, "updated": time.time(), "messages": []}
        self.conversations.append(conv)
        self.active_id = conv["id"]
        self.save()
        return conv

    def add_message(self, role: str, text: str) -> None:
        conv = self.active
        conv["messages"].append({"role": role, "text": text, "ts": time.time()})
        del conv["messages"][: -self.max_messages]
        conv["updated"] = time.time()
        if role == "user" and conv["title"] == DEFAULT_TITLE:
            conv["title"] = " ".join(text.split())[:40] or DEFAULT_TITLE
        self.save()

    def set_active(self, conv_id: str) -> None:
        if self.get(conv_id) is None:
            raise KeyError(conv_id)
        self.active_id = conv_id
        self.save()

    def rename(self, conv_id: str, title: str) -> None:
        conv = self.get(conv_id)
        if conv is None:
            raise KeyError(conv_id)
        conv["title"] = title.strip() or DEFAULT_TITLE
        self.save()

    def clear(self, conv_id: str) -> None:
        conv = self.get(conv_id)
        if conv is None:
            raise KeyError(conv_id)
        conv["messages"] = []
        self.save()

    def delete(self, conv_id: str) -> None:
        self.conversations = [c for c in self.conversations if c["id"] != conv_id]
        if self.active_id == conv_id:
            self.active_id = None
        self.save()
