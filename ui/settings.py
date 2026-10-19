from __future__ import annotations

from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView

from storage.settings import ALLOWED
from ui.widgets import BaseScreen, Card, PillButton, WrappedLabel, fs, palette

LABELS = {"theme": "Theme", "accent": "Accent colour", "text_size": "Text size"}


class SettingsScreen(BaseScreen):
    title = "Settings"

    def build_body(self):
        p = palette()
        store = self.app.settings_store
        col = BoxLayout(orientation="vertical", size_hint_y=None, spacing=dp(14), padding=(0, dp(4)))
        col.bind(minimum_height=col.setter("height"))

        for key, options in ALLOWED.items():
            col.add_widget(WrappedLabel(text=LABELS[key], bold=True, font_size=fs(), color=p.text))
            row = BoxLayout(orientation="horizontal", size_hint_y=None, height=dp(44), spacing=dp(8))
            for opt in options:
                selected = store.get(key) == opt
                row.add_widget(PillButton(p.accent if selected else p.surface_alt,
                                          p.accent_text if selected else p.text, text=opt.capitalize(),
                                          on_release=lambda *_, k=key, v=opt: self.app.update_setting(k, v)))
            col.add_widget(row)

        col.add_widget(self._card("Gemini API", "Key entry, model choice and a connection test arrive in Phase 2. No key is stored today."))
        col.add_widget(self._card(
            "Privacy and permissions",
            "Internet: declared, not used yet.\n"
            "Microphone: not requested. Asked only when Voice features ship (Phase 4).\n"
            "Storage: not requested. JARVIS will use Android's folder picker for workspaces.\n"
            "Accessibility: not requested and not planned without a clear explanation first.\n"
            "Stored on this phone: your theme choices and your chat history."))
        scroll = ScrollView(do_scroll_x=False)
        scroll.add_widget(col)
        self.body.add_widget(scroll)

    def _card(self, title: str, text: str) -> Card:
        p = palette()
        card = Card(p.surface, p.border, orientation="vertical", size_hint_y=None, padding=dp(14), spacing=dp(6))
        card.bind(minimum_height=card.setter("height"))
        card.add_widget(WrappedLabel(text=title, bold=True, font_size=fs(), color=p.accent))
        card.add_widget(WrappedLabel(text=text, font_size=fs(0.9), color=p.text))
        return card
