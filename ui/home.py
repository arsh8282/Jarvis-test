from __future__ import annotations

from datetime import datetime

from kivy.metrics import dp, sp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView

from ui.sections import SECTIONS
from ui.widgets import BaseScreen, Tile, WrappedLabel, fs, palette


def greeting() -> str:
    hour = datetime.now().hour
    part = "morning" if hour < 12 else "afternoon" if hour < 18 else "evening"
    return f"Good {part}, Sir."


class HomeScreen(BaseScreen):
    title = "JARVIS"
    show_back = False

    def build_body(self):
        p = palette()
        head = BoxLayout(orientation="vertical", size_hint_y=None, height=dp(86), padding=(dp(4), dp(10), 0, 0))
        head.add_widget(WrappedLabel(text=greeting(), font_size=sp(26), bold=True, color=p.text, height=dp(40)))
        head.add_widget(WrappedLabel(text="How may I assist you?", font_size=fs(), color=p.text_dim, height=dp(26)))
        self.body.add_widget(head)

        grid = GridLayout(cols=2, spacing=dp(10), size_hint_y=None, padding=(0, dp(4)))
        grid.bind(minimum_height=grid.setter("height"))
        for key, name, sub, status in SECTIONS:
            live = status in ("Interface ready",)
            tile = Tile(p.surface, p.accent if live else p.border, orientation="vertical",
                        size_hint_y=None, height=dp(104), padding=dp(12), spacing=dp(2),
                        on_release=lambda *_, k=key: self.app.go(k))
            tile.add_widget(WrappedLabel(text=name, bold=True, font_size=fs(), color=p.text))
            tile.add_widget(WrappedLabel(text=sub, font_size=fs(0.8), color=p.text_dim))
            tile.add_widget(WrappedLabel(text=status, font_size=fs(0.75), color=p.accent if live else p.text_dim))
            grid.add_widget(tile)
        scroll = ScrollView(do_scroll_x=False)
        scroll.add_widget(grid)
        self.body.add_widget(scroll)
