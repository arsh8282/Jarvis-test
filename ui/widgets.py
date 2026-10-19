"""Reusable Kivy widgets styled from the active palette."""
from __future__ import annotations

from kivy.app import App
from kivy.graphics import Color, Line, RoundedRectangle
from kivy.metrics import dp, sp
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen


def palette():
    return App.get_running_app().palette


def fs(scale: float = 1.0) -> float:
    return sp(App.get_running_app().font_size * scale)


class WrappedLabel(Label):
    """Label that wraps to its width and grows to fit its text."""

    def __init__(self, **kw):
        kw.setdefault("size_hint_y", None)
        kw.setdefault("halign", "left")
        kw.setdefault("valign", "top")
        super().__init__(**kw)
        self.bind(width=self._wrap, texture_size=self._fit)

    def _wrap(self, *_):
        self.text_size = (self.width, None)

    def _fit(self, *_):
        self.height = self.texture_size[1]


class Card(BoxLayout):
    """Rounded panel with a thin border."""

    def __init__(self, fill, border, radius=None, **kw):
        super().__init__(**kw)
        self._radius = radius or dp(16)
        with self.canvas.before:
            Color(*fill)
            self._bg = RoundedRectangle(radius=[self._radius])
            Color(*border)
            self._line = Line(rounded_rectangle=(0, 0, 0, 0, self._radius), width=1)
        self.bind(pos=self._sync, size=self._sync)

    def _sync(self, *_):
        self._bg.pos, self._bg.size = self.pos, self.size
        self._line.rounded_rectangle = (self.x, self.y, self.width, self.height, self._radius)


class Tile(ButtonBehavior, Card):
    """Tappable card. ButtonBehavior only accepts keyword arguments, so forward them by name."""

    def __init__(self, fill, border, **kw):
        super().__init__(fill=fill, border=border, **kw)


class PillButton(Button):
    def __init__(self, fill, text_color, radius=None, **kw):
        kw.setdefault("font_size", sp(14))
        super().__init__(
            background_normal="", background_down="", background_color=(0, 0, 0, 0),
            color=text_color, **kw,
        )
        self._radius = radius or dp(20)
        with self.canvas.before:
            self._color = Color(*fill)
            self._rect = RoundedRectangle(radius=[self._radius])
        self._fill = fill
        self.bind(pos=self._sync, size=self._sync, on_press=self._down, on_release=self._up)

    def _sync(self, *_):
        self._rect.pos, self._rect.size = self.pos, self.size

    def _down(self, *_):
        self._color.rgba = (*self._fill[:3], self._fill[3] * 0.6)

    def _up(self, *_):
        self._color.rgba = self._fill


class TopBar(BoxLayout):
    def __init__(self, title, on_back=None, actions=(), **kw):
        super().__init__(orientation="horizontal", size_hint_y=None, height=dp(56),
                         padding=(dp(8), dp(8)), spacing=dp(6), **kw)
        p = palette()
        if on_back:
            self.add_widget(PillButton(p.surface_alt, p.text, text="Home", size_hint_x=None,
                                       width=dp(68), on_release=lambda *_: on_back()))
        label = Label(text=title, bold=True, font_size=sp(18), color=p.text, halign="left", valign="middle")
        label.bind(size=lambda w, s: setattr(w, "text_size", s))
        self.add_widget(label)
        for text, callback in actions:
            self.add_widget(PillButton(p.surface_alt, p.accent, text=text, size_hint_x=None,
                                       width=dp(62), on_release=lambda *_, cb=callback: cb()))


class BaseScreen(Screen):
    title = "JARVIS"
    show_back = True

    def __init__(self, app, **kw):
        super().__init__(**kw)
        self.app = app
        root = BoxLayout(orientation="vertical")
        back = (lambda: app.go("home")) if self.show_back else None
        root.add_widget(TopBar(self.title, on_back=back, actions=self.top_actions()))
        self.body = BoxLayout(orientation="vertical", padding=(dp(14), dp(6), dp(14), dp(12)), spacing=dp(10))
        root.add_widget(self.body)
        self.add_widget(root)
        self.build_body()

    def top_actions(self):
        return []

    def build_body(self):
        raise NotImplementedError
