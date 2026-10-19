from __future__ import annotations

from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView

from ui.widgets import BaseScreen, Tile, WrappedLabel, fs, palette


class HistoryScreen(BaseScreen):
    title = "Conversation History"

    def build_body(self):
        self.list = BoxLayout(orientation="vertical", size_hint_y=None, spacing=dp(8))
        self.list.bind(minimum_height=self.list.setter("height"))
        scroll = ScrollView(do_scroll_x=False)
        scroll.add_widget(self.list)
        self.body.add_widget(scroll)

    def on_pre_enter(self, *_):
        p = palette()
        self.list.clear_widgets()
        items = [s for s in self.app.conversations.summaries() if s["count"] > 0]
        if not items:
            self.list.add_widget(WrappedLabel(text="No saved conversations yet, Sir.", font_size=fs(), color=p.text_dim))
        for item in items:
            tile = Tile(p.surface, p.border, orientation="vertical", size_hint_y=None, height=dp(70),
                        padding=dp(12), on_release=lambda *_, cid=item["id"]: self.open(cid))
            tile.add_widget(WrappedLabel(text=item["title"], bold=True, font_size=fs(), color=p.text, shorten=True))
            tile.add_widget(WrappedLabel(text=f"{item['count']} messages", font_size=fs(0.8), color=p.text_dim))
            self.list.add_widget(tile)

    def open(self, conv_id: str):
        self.app.conversations.set_active(conv_id)
        self.app.go("text")
