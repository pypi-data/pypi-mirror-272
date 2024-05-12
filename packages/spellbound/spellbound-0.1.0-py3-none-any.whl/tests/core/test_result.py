import unittest

from spellbound.core.result import SpellResult, SpellStatus


class TestSpellResult(unittest.TestCase):
    def test_title(self):
        result = SpellResult(status=SpellStatus.SUCCESS)
        self.assertEqual(result.get_title(), "`Spell` was completed successfully.")

    def test_title_fail(self):
        result = SpellResult(status=SpellStatus.FAILURE)
        self.assertEqual(result.get_title(), "`Spell` has failed.")

    def test_title_abort(self):
        result = SpellResult(status=SpellStatus.ABORTED)
        self.assertEqual(result.get_title(), "`Spell` was aborted during execution.")

    def test_title_skip(self):
        result = SpellResult(status=SpellStatus.SKIPPED)
        self.assertEqual(result.get_title(), "`Spell` was skipped.")

    def test_title_custom(self):
        result = SpellResult(status=SpellStatus.SUCCESS, title="Custom title")
        self.assertEqual(result.get_title(), "Custom title")

    def test_is_error(self):
        result = SpellResult(status=SpellStatus.SUCCESS)
        self.assertFalse(result.is_error())

        result = SpellResult(status=SpellStatus.FAILURE)
        self.assertTrue(result.is_error())

        result = SpellResult(status=SpellStatus.ABORTED)
        self.assertTrue(result.is_error())

        result = SpellResult(status=SpellStatus.SKIPPED)
        self.assertFalse(result.is_error())
