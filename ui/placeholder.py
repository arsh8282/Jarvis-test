from __future__ import annotations

from kivy.metrics import dp, sp
from kivy.uix.widget import Widget

from ui.sections import PHASE_FOR, PLACEHOLDERS, SECTIONS
from ui.widgets import BaseScreen, Card, WrappedLabel, fs, palette


class PlaceholderScreen(BaseScreen):
    """Honest 'not built yet' screen for sections that arrive in later phases."""

    def __init__(self, app, key, **kw):
        self.key = key
        self.title = next(t for k, t, _, _ in SECTIONS if k == key)
        super().__init__(app, name=key, **kw)

    def build_body(self):
        p = palette()
        card = Card(p.surface, p.border, orientation="vertical", size_hint_y=None, padding=dp(16), spacing=dp(10))
        card.bind(minimum_height=card.setter("height"))
        card.add_widget(WrappedLabel(text=f"Arrives in Phase {PHASE_FOR[self.key]}", bold=True,
                                     font_size=fs(1.1), color=p.accent))
        card.add_widget(WrappedLabel(text=PLACEHOLDERS[self.key], font_size=fs(), color=p.text))
        card.add_widget(WrappedLabel(text="Nothing here is functional yet, Sir.", font_size=fs(0.85), color=p.text_dim))
        self.body.add_widget(card)
        self.body.add_widget(Widget())
