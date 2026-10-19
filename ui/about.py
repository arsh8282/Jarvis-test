from __future__ import annotations

from kivy.metrics import dp, sp
from kivy.uix.widget import Widget

from ui.widgets import BaseScreen, Card, WrappedLabel, fs, palette
from version import PHASE, __version__


class AboutScreen(BaseScreen):
    title = "About JARVIS"

    def build_body(self):
        p = palette()
        card = Card(p.surface, p.border, orientation="vertical", size_hint_y=None, padding=dp(16), spacing=dp(8))
        card.bind(minimum_height=card.setter("height"))
        card.add_widget(WrappedLabel(text="JARVIS", bold=True, font_size=sp(28), color=p.accent))
        card.add_widget(WrappedLabel(text=f"Version {__version__} | {PHASE}", font_size=fs(0.9), color=p.text_dim))
        card.add_widget(WrappedLabel(
            text="Working now: navigation, themes, text-chat interface with saved history, voice screen preview.\n\n"
                 "Not built yet: Gemini replies, speech, file editing, device control, WhatsApp tools.",
            font_size=fs(), color=p.text))
        self.body.add_widget(card)
        self.body.add_widget(Widget())
