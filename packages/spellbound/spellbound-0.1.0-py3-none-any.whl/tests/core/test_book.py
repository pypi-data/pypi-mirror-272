import unittest

from spellbound.core.book import SpellBook
from spellbound.utils.exception import NotFoundException


class TestSpellBook(unittest.TestCase):
    def setUp(self):
        self.spell_book = SpellBook()

    def test_register(self):
        self.spell_book.register("Fireball", "SpellClass")
        self.assertEqual(self.spell_book.find("Fireball"), "SpellClass")

    def test_register_existing_spell(self):
        self.spell_book.register("Fireball", "SpellClass")
        self.spell_book.register("Fireball", "NewSpellClass")
        self.assertEqual(self.spell_book.find("Fireball"), "NewSpellClass")

    def test_find_existing_spell(self):
        self.spell_book.register("Fireball", "SpellClass")
        self.assertEqual(self.spell_book.find("Fireball"), "SpellClass")

    def test_find_non_existing_spell(self):
        with self.assertRaises(NotFoundException):
            self.spell_book.find("NonExistingSpell")

    def test_update(self):
        another_book = SpellBook()
        another_book.register("Fireball", "SpellClass")
        another_book.register("Icebolt", "SpellClass")
        self.spell_book.update(another_book)
        self.assertEqual(self.spell_book.find("Fireball"), "SpellClass")
        self.assertEqual(self.spell_book.find("Icebolt"), "SpellClass")

    def test_to_list(self):
        self.spell_book.register("Fireball", "SpellClass")
        self.spell_book.register("Icebolt", "SpellClass")
        spell_list = self.spell_book.to_list()
        self.assertEqual(len(spell_list), 2)
        self.assertEqual(
            spell_list, [("Fireball", "SpellClass"), ("Icebolt", "SpellClass")]
        )

    def test_copy(self):
        self.spell_book.register("Fireball", "SpellClass")
        copied_book = self.spell_book.copy()
        self.assertIsNot(copied_book, self.spell_book)
        self.assertEqual(copied_book.find("Fireball"), "SpellClass")
