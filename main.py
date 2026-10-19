"""JARVIS entry point (Phase 1)."""
from __future__ import annotations

import logging
import os
import traceback

os.environ.setdefault("KIVY_NO_ARGS", "1")
from kivy.config import Config  # noqa: E402

Config.set("kivy", "exit_on_escape", "0")

from kivy.app import App  # noqa: E402
from kivy.clock import Clock  # noqa: E402
from kivy.core.window import Window  # noqa: E402
from kivy.uix.boxlayout import BoxLayout  # noqa: E402

from assistant.engine import PlaceholderEngine  # noqa: E402
from storage.conversations import ConversationStore  # noqa: E402
from storage.settings import SettingsStore  # noqa: E402
from ui.manager import build_manager  # noqa: E402
from ui.theme import TEXT_SIZES, build_palette  # noqa: E402

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
log = logging.getLogger("jarvis")


class JarvisApp(App):
    title = "JARVIS"

    def build(self):
        try:
            return self._build()
        except Exception:  # show the error on screen so it can be reported
            log.exception("Startup failed")
            return self._crash_view(traceback.format_exc())

    def _crash_view(self, text: str):
        from kivy.metrics import sp
        from kivy.uix.label import Label
        from kivy.uix.scrollview import ScrollView

        label = Label(text="JARVIS startup error:\n\n" + text, size_hint_y=None, halign="left",
                      valign="top", font_size=sp(12), text_size=(Window.width - 24, None))
        label.bind(texture_size=lambda w, s: setattr(w, "height", s[1]))
        scroll = ScrollView()
        scroll.add_widget(label)
        return scroll

    def _build(self):
        data = self.user_data_dir
        self.settings_store = SettingsStore(os.path.join(data, "settings.json"))
        self.conversations = ConversationStore(os.path.join(data, "conversations.json"))
        self.engine = PlaceholderEngine()
        Window.softinput_mode = "below_target"
        Window.bind(on_keyboard=self._on_keyboard)
        self.container = BoxLayout()
        self.apply_theme()
        self.sm = build_manager(self)
        self.container.add_widget(self.sm)
        return self.container

    def apply_theme(self):
        s = self.settings_store
        self.palette = build_palette(s.get("theme"), s.get("accent"))
        self.font_size = TEXT_SIZES[s.get("text_size")]
        Window.clearcolor = self.palette.bg

    def update_setting(self, key: str, value: str):
        self.settings_store.set(key, value)
        Clock.schedule_once(lambda _dt: self._rebuild("settings"), 0)

    def _rebuild(self, start: str):
        from kivy.animation import Animation

        Animation.cancel_all(self.sm.get_screen("voice").orb)  # stop the old orb's loop
        self.apply_theme()
        self.container.clear_widgets()
        self.sm = build_manager(self, start)
        self.container.add_widget(self.sm)

    def go(self, name: str):
        self.sm.current = name

    def _on_keyboard(self, _window, key, *_args):
        if key == 27:  # Android back button
            if self.sm.current != "home":
                self.go("home")
                return True
            return False  # on Home: let Android close the app
        return False


if __name__ == "__main__":
    JarvisApp().run()
