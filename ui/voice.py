from __future__ import annotations

from kivy.animation import Animation
from kivy.graphics import Color, Ellipse, Line
from kivy.metrics import dp, sp
from kivy.properties import NumericProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget

from ui.widgets import BaseScreen, PillButton, WrappedLabel, fs, palette

STATE_TEXT = {
    "idle": "Idle. Tap the microphone to begin.",
    "listening": "Listening...",
    "processing": "Processing...",
    "speaking": "Speaking...",
}
AMPLITUDE = {"idle": 0.04, "listening": 0.16, "processing": 0.06, "speaking": 0.24}
PERIOD = {"idle": 2.4, "listening": 0.9, "processing": 1.2, "speaking": 0.6}


class Orb(Widget):
    """Glowing assistant orb. Animation only; it does not hear or speak yet."""

    pulse = NumericProperty(0.0)
    state = StringProperty("idle")

    def __init__(self, accent, **kw):
        super().__init__(**kw)
        self._accent = accent[:3]
        self.bind(pos=self.redraw, size=self.redraw, pulse=self.redraw, state=self.redraw)
        self.set_state("idle")

    def set_state(self, state: str):
        Animation.cancel_all(self, "pulse")
        self.state = state
        self.pulse = 0.0
        if state == "processing":
            anim = Animation(pulse=1.0, d=PERIOD[state], t="linear") + Animation(pulse=0.0, d=0)
        else:
            half = PERIOD[state] / 2
            anim = Animation(pulse=1.0, d=half, t="in_out_sine") + Animation(pulse=0.0, d=half, t="in_out_sine")
        anim.repeat = True
        anim.start(self)

    def redraw(self, *_):
        self.canvas.clear()
        cx, cy = self.center
        base = min(self.width, self.height) * 0.26
        r = base * (1 + AMPLITUDE[self.state] * self.pulse)
        a = self._accent
        with self.canvas:
            for scale, alpha in ((2.1, 0.05), (1.7, 0.09), (1.35, 0.15)):
                Color(*a, alpha * (0.6 + 0.4 * self.pulse))
                Ellipse(pos=(cx - r * scale, cy - r * scale), size=(2 * r * scale, 2 * r * scale))
            Color(*a, 0.22)
            Ellipse(pos=(cx - r, cy - r), size=(2 * r, 2 * r))
            Color(*a, 0.95)
            if self.state == "processing":
                start = self.pulse * 360
                Line(ellipse=(cx - r, cy - r, 2 * r, 2 * r, start, start + 100), width=dp(3))
            else:
                Line(circle=(cx, cy, r), width=dp(2))


class VoiceScreen(BaseScreen):
    title = "Voice Assistant"

    def top_actions(self):
        return [("Text", lambda: self.app.go("text"))]

    def build_body(self):
        p = palette()
        self.orb = Orb(p.accent)
        self.body.add_widget(self.orb)
        self.status = WrappedLabel(text=STATE_TEXT["idle"], font_size=fs(1.1), color=p.text, halign="center", height=fs(1.1) * 1.6)
        self.body.add_widget(self.status)
        self.note = WrappedLabel(
            text="Preview only, Sir. Speech recognition and spoken replies arrive in Phase 4. "
                 "The buttons below only demonstrate the interface states.",
            font_size=fs(0.8), color=p.text_dim, halign="center")
        self.body.add_widget(self.note)

        self.mic = PillButton(p.accent, p.accent_text, text="Start listening", bold=True, size_hint_y=None,
                              height=dp(56), radius=dp(28), on_release=self.toggle_mic)
        self.body.add_widget(self.mic)

        chips = BoxLayout(orientation="horizontal", size_hint_y=None, height=dp(40), spacing=dp(6))
        for state in ("idle", "listening", "processing", "speaking"):
            chips.add_widget(PillButton(p.surface_alt, p.text, text=state.capitalize(), font_size=sp(12),
                                        on_release=lambda *_, s=state: self.set_state(s)))
        self.body.add_widget(chips)

    def set_state(self, state: str):
        self.orb.set_state(state)
        self.status.text = STATE_TEXT[state]
        self.mic.text = "Stop listening" if state == "listening" else "Start listening"

    def toggle_mic(self, *_):
        self.set_state("idle" if self.orb.state == "listening" else "listening")

    def on_leave(self, *_):
        self.set_state("idle")
