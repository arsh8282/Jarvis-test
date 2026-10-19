import json
import os
import tempfile
import unittest

from storage.conversations import DEFAULT_TITLE, ConversationStore
from storage.settings import DEFAULTS, SettingsStore


class SettingsTests(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.dir.name, "s.json")

    def tearDown(self):
        self.dir.cleanup()

    def test_defaults(self):
        s = SettingsStore(self.path)
        self.assertEqual(s.get("theme"), DEFAULTS["theme"])

    def test_set_persists(self):
        SettingsStore(self.path).set("accent", "teal")
        self.assertEqual(SettingsStore(self.path).get("accent"), "teal")

    def test_rejects_invalid(self):
        s = SettingsStore(self.path)
        with self.assertRaises(ValueError):
            s.set("theme", "neon")
        with self.assertRaises(KeyError):
            s.set("nope", "x")

    def test_corrupt_file_falls_back(self):
        with open(self.path, "w") as fh:
            fh.write("{not json")
        self.assertEqual(SettingsStore(self.path).get("theme"), "dark")

    def test_ignores_invalid_values_on_disk(self):
        with open(self.path, "w") as fh:
            json.dump({"theme": "light", "accent": "pink"}, fh)
        s = SettingsStore(self.path)
        self.assertEqual((s.get("theme"), s.get("accent")), ("light", "cyan"))


class ConversationTests(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.dir.name, "c.json")

    def tearDown(self):
        self.dir.cleanup()

    def test_active_created_on_demand(self):
        store = ConversationStore(self.path)
        self.assertEqual(store.active["title"], DEFAULT_TITLE)

    def test_title_from_first_user_message_and_persistence(self):
        store = ConversationStore(self.path)
        store.add_message("user", "Explain   this smali   code please")
        store.add_message("assistant", "ok")
        again = ConversationStore(self.path)
        self.assertEqual(again.active["title"], "Explain this smali code please")
        self.assertEqual(len(again.active["messages"]), 2)

    def test_rename_clear_delete(self):
        store = ConversationStore(self.path)
        cid = store.active["id"]
        store.add_message("user", "hi")
        store.rename(cid, "Renamed")
        self.assertEqual(store.get(cid)["title"], "Renamed")
        store.clear(cid)
        self.assertEqual(store.get(cid)["messages"], [])
        store.delete(cid)
        self.assertIsNone(store.get(cid))

    def test_message_cap(self):
        store = ConversationStore(self.path, max_messages=3)
        for i in range(6):
            store.add_message("user", str(i))
        self.assertEqual([m["text"] for m in store.active["messages"]], ["3", "4", "5"])

    def test_corrupt_history_is_preserved_as_bad(self):
        with open(self.path, "w") as fh:
            fh.write("garbage")
        store = ConversationStore(self.path)
        self.assertEqual(store.conversations, [])
        self.assertTrue(os.path.exists(self.path + ".bad"))

    def test_summaries_newest_first(self):
        store = ConversationStore(self.path)
        first = store.active["id"]
        store.add_message("user", "one")
        second = store.new_conversation()["id"]
        store.add_message("user", "two")
        self.assertEqual([s["id"] for s in store.summaries()], [second, first])


if __name__ == "__main__":
    unittest.main()
