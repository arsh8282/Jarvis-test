from __future__ import annotations

from kivy.uix.screenmanager import FadeTransition, ScreenManager

from ui.about import AboutScreen
from ui.chat import ChatScreen
from ui.history import HistoryScreen
from ui.home import HomeScreen
from ui.placeholder import PlaceholderScreen
from ui.sections import PLACEHOLDERS
from ui.settings import SettingsScreen
from ui.voice import VoiceScreen


def build_manager(app, start: str = "home") -> ScreenManager:
    sm = ScreenManager(transition=FadeTransition(duration=0.12))
    screens = [
        HomeScreen(app, name="home"),
        ChatScreen(app, name="text"),
        VoiceScreen(app, name="voice"),
        HistoryScreen(app, name="history"),
        SettingsScreen(app, name="settings"),
        AboutScreen(app, name="about"),
    ]
    screens += [PlaceholderScreen(app, key) for key in PLACEHOLDERS]
    for screen in screens:
        sm.add_widget(screen)
    sm.current = start
    return sm
