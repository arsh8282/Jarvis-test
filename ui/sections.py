"""The 11 navigation sections. Kivy-free. `status` is shown honestly on Home."""
from __future__ import annotations

# key, title, subtitle, status
SECTIONS: list[tuple[str, str, str, str]] = [
    ("text", "Text Assistant", "Chat with JARVIS", "Interface ready"),
    ("voice", "Voice Assistant", "Speak and listen", "Preview only"),
    ("code_lab", "Code Lab", "Smali and code help", "Arrives in Phase 3"),
    ("files", "Project Files", "Workspace and edits", "Arrives in Phase 3"),
    ("device", "Device Control", "Apps, links, sharing", "Arrives in Phase 5"),
    ("search", "Search", "Web, files, history", "Arrives in Phase 3"),
    ("whatsapp", "WhatsApp Tools", "Draft and hand off", "Arrives in Phase 6"),
    ("history", "Conversation History", "Your past chats", "Interface ready"),
    ("settings", "Settings", "Theme, accent, text size", "Interface ready"),
    ("about", "About JARVIS", "Version and limits", "Interface ready"),
]

PLACEHOLDERS: dict[str, str] = {
    "code_lab": "Smali, Java, Kotlin and Python help with explanations in simple Hinglish. Needs the Gemini connection (Phase 2) and the file tools (Phase 3).",
    "files": "Pick a workspace folder, browse and search files, apply patches with diffs and backups. Uses Android's folder picker so no all-files permission is needed.",
    "device": "Open apps and links, share text, open Android settings pages. Each capability will list the permission it needs before you enable it.",
    "search": "Search the web, your workspace files, your conversation history, and code identifiers. Results will be labelled as real results, never generated guesses.",
    "whatsapp": "Draft a message, open WhatsApp with it filled in, and you choose the recipient and press send. JARVIS will never claim a message was delivered.",
}
PHASE_FOR = {"code_lab": 3, "files": 3, "device": 5, "search": 3, "whatsapp": 6}
