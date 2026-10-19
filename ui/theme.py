"""Colour tokens. Pure Python so it can be unit-tested without Kivy."""
from __future__ import annotations

from dataclasses import dataclass

RGBA = tuple[float, float, float, float]

DARK_ACCENTS = {"cyan": "#22D3EE", "teal": "#2DD4BF", "blue": "#4C8DFF"}
LIGHT_ACCENTS = {"cyan": "#0E7490", "teal": "#0F766E", "blue": "#2563EB"}
TEXT_SIZES = {"small": 14.0, "medium": 16.0, "large": 19.0}  # sp


def hex_rgba(value: str, alpha: float = 1.0) -> RGBA:
    value = value.lstrip("#")
    r, g, b = (int(value[i : i + 2], 16) / 255.0 for i in (0, 2, 4))
    return (r, g, b, alpha)


@dataclass(frozen=True)
class Palette:
    bg: RGBA
    surface: RGBA
    surface_alt: RGBA
    border: RGBA
    text: RGBA
    text_dim: RGBA
    accent: RGBA
    accent_soft: RGBA
    accent_text: RGBA


def build_palette(mode: str, accent_name: str) -> Palette:
    if mode == "light":
        accent = LIGHT_ACCENTS[accent_name]
        return Palette(
            bg=hex_rgba("#EEF3F8"),
            surface=hex_rgba("#FFFFFF"),
            surface_alt=hex_rgba("#DCE6F0"),
            border=hex_rgba("#B8C7D8"),
            text=hex_rgba("#0B1220"),
            text_dim=hex_rgba("#46566B"),
            accent=hex_rgba(accent),
            accent_soft=hex_rgba(accent, 0.16),
            accent_text=hex_rgba("#FFFFFF"),
        )
    accent = DARK_ACCENTS[accent_name]
    return Palette(
        bg=hex_rgba("#050A14"),
        surface=hex_rgba("#0D1828"),
        surface_alt=hex_rgba("#152238"),
        border=hex_rgba("#22344F"),
        text=hex_rgba("#E6F1FA"),
        text_dim=hex_rgba("#8CA3BC"),
        accent=hex_rgba(accent),
        accent_soft=hex_rgba(accent, 0.18),
        accent_text=hex_rgba("#031018"),
    )
