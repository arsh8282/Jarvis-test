import os
import re
import unittest

from storage.settings import ALLOWED
from ui.sections import PHASE_FOR, PLACEHOLDERS, SECTIONS
from ui.theme import TEXT_SIZES, build_palette, hex_rgba
from version import __version__

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def luminance(rgba):
    def lin(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (lin(c) for c in rgba[:3])
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


class ThemeTests(unittest.TestCase):
    def test_hex(self):
        self.assertEqual(hex_rgba("#FF0000"), (1.0, 0.0, 0.0, 1.0))

    def test_every_combination_builds_with_readable_text(self):
        for mode in ALLOWED["theme"]:
            for accent in ALLOWED["accent"]:
                p = build_palette(mode, accent)
                self.assertGreaterEqual(contrast(p.text, p.bg), 7.0, (mode, accent))
                self.assertGreaterEqual(contrast(p.text_dim, p.surface), 4.5, (mode, accent))
                self.assertGreaterEqual(contrast(p.accent_text, p.accent), 4.5, (mode, accent))

    def test_text_sizes_match_settings(self):
        self.assertEqual(set(TEXT_SIZES), set(ALLOWED["text_size"]))


class MetaTests(unittest.TestCase):
    def test_version_matches_buildozer_spec(self):
        spec = open(os.path.join(ROOT, "buildozer.spec")).read()
        self.assertEqual(re.search(r"^version = (.+)$", spec, re.M).group(1).strip(), __version__)

    def test_placeholder_sections_are_complete(self):
        for key in PLACEHOLDERS:
            self.assertIn(key, PHASE_FOR)
            self.assertIn(key, [s[0] for s in SECTIONS])

    def test_every_section_has_a_screen_key(self):
        keys = {s[0] for s in SECTIONS}
        self.assertEqual(keys, {"text", "voice", "code_lab", "files", "device", "search",
                                "whatsapp", "history", "settings", "about"})


if __name__ == "__main__":
    unittest.main()
