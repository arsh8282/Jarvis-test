from __future__ import annotations

import logging

from kivy.clock import Clock
from kivy.core.clipboard import Clipboard
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

from ui.widgets import BaseScreen, Card, PillButton, WrappedLabel, fs, palette

log = logging.getLogger("jarvis.chat")


class MessageRow(BoxLayout):
    def __init__(self, role: str, text: str, **kw):
        super().__init__(orientation="horizontal", size_hint_y=None, **kw)
        p = palette()
        user = role == "user"
        bubble = Card(p.accent_soft if user else p.surface, p.accent if user else p.border,
                      orientation="vertical", size_hint_x=0.88, size_hint_y=None,
                      padding=dp(12), spacing=dp(6))
        bubble.add_widget(WrappedLabel(text=text, font_size=fs(), color=p.text))
        if not user:
            bubble.add_widget(PillButton(p.surface_alt, p.text_dim, text="Copy", size_hint=(None, None),
                                         size=(dp(64), dp(30)),
                                         on_release=lambda *_: Clipboard.copy(text)))
        bubble.bind(minimum_height=bubble.setter("height"))
        bubble.bind(height=lambda _w, h: setattr(self, "height", h))
        spacer = Widget(size_hint_x=0.12, size_hint_y=None, height=0)
        for w in ((spacer, bubble) if user else (bubble, spacer)):
            self.add_widget(w)


class ChatScreen(BaseScreen):
    title = "Text Assistant"

    def top_actions(self):
        return [("New", self.new_chat), ("Voice", lambda: self.app.go("voice"))]

    def build_body(self):
        p = palette()
        self.scroll = ScrollView(do_scroll_x=False)
        self.list = BoxLayout(orientation="vertical", size_hint_y=None, spacing=dp(10), padding=(0, dp(4)))
        self.list.bind(minimum_height=self.list.setter("height"))
        self.scroll.add_widget(self.list)
        self.body.add_widget(self.scroll)

        self.input = TextInput(multiline=True, hint_text="Message JARVIS", size_hint_y=None, height=dp(48),
                               background_normal="", background_active="", background_color=(0, 0, 0, 0),
                               foreground_color=p.text, hint_text_color=p.text_dim, cursor_color=p.accent,
                               padding=(dp(10), dp(12)), font_size=fs())
        self.input.bind(minimum_height=self._grow)
        self.input_card = Card(p.surface, p.border, size_hint_x=1, padding=dp(2))
        self.input_card.add_widget(self.input)
        row = BoxLayout(orientation="horizontal", size_hint_y=None, height=dp(52), spacing=dp(8))
        self.input_card.size_hint_y = None
        self.input_card.height = dp(52)
        row.add_widget(self.input_card)
        row.add_widget(PillButton(p.accent, p.accent_text, text="Send", bold=True, size_hint=(None, None),
                                  size=(dp(72), dp(48)), on_release=self.send))
        self.row = row
        self.body.add_widget(row)

    def _grow(self, _w, value):
        height = max(dp(48), min(dp(140), value))
        self.input.height = height
        self.input_card.height = height + dp(4)
        self.row.height = height + dp(4)

    def on_pre_enter(self, *_):
        self.refresh()

    def refresh(self):
        p = palette()
        self.list.clear_widgets()
        messages = self.app.conversations.active["messages"]
        if not messages:
            self.list.add_widget(WrappedLabel(
                text="No messages yet, Sir. Type below to begin.\n\nReplies are placeholders until Gemini is connected in Phase 2.",
                font_size=fs(0.9), color=p.text_dim, padding=(dp(4), dp(12))))
        for msg in messages:
            self.list.add_widget(MessageRow(msg["role"], msg["text"]))
        Clock.schedule_once(lambda _dt: setattr(self.scroll, "scroll_y", 0), 0.05)

    def new_chat(self):
        self.app.conversations.new_conversation()
        self.refresh()

    def send(self, *_):
        text = self.input.text.strip()
        if not text:
            return
        self.input.text = ""
        store = self.app.conversations
        store.add_message("user", text)
        try:
            reply = self.app.engine.reply(store.active["messages"], text)
        except Exception as exc:  # engine errors must never crash the UI
            log.exception("Engine failure")
            reply = f"Apologies, Sir. Something went wrong: {exc}"
        store.add_message("assistant", reply)
        self.refresh()
