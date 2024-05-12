from pydantic import ValidationError

from spellbound.core.book import SpellBook
from spellbound.core.caster import SpellCaster
from spellbound.core.spell import Spell, SpellResult, SpellStatus
from spellbound.utils.exception import NotFoundException
from tests.helpers.async_case import IsolatedAsyncioTestCase


class PatronusSpellParams(Spell.InputParams):
    shape: str


class PatronusSpell(Spell):
    InputParams = PatronusSpellParams

    async def execute(self):
        return SpellResult(status=SpellStatus.SUCCESS, data="Expecto Patronum")


class ForbiddenSpell(Spell):
    InputParams = PatronusSpellParams

    async def execute(self):
        return SpellResult(status=SpellStatus.SUCCESS, data="Avada Kedavra")


class TestSpellCaster(IsolatedAsyncioTestCase):
    def setUp(self):
        self.caster = SpellCaster()
        self.caster.learn("patronus", PatronusSpell)

    def test_learn(self):
        self.caster.learn("patronum", PatronusSpell)
        self.caster.find("patronum")

    def test_learn_with_group(self):
        self.caster.learn("patronum", PatronusSpell, group="test")
        self.assertEqual(self.caster._spell_to_group["patronum"], "test")

    def test_learn_all(self):
        book = SpellBook({"patronus": ForbiddenSpell, "forbidden": ForbiddenSpell})
        self.caster.learn_all(book)
        self.assertEqual(self.caster.find("patronus"), ForbiddenSpell)
        self.assertEqual(self.caster.find("forbidden"), ForbiddenSpell)

    def test_learn_all_with_group(self):
        book = SpellBook({"patronus": ForbiddenSpell, "forbidden": ForbiddenSpell})
        self.caster.learn_all(book, group="test")
        self.assertEqual(self.caster._spell_to_group["patronus"], "test")
        self.assertEqual(self.caster._spell_to_group["forbidden"], "test")

    def test_forget(self):
        self.caster.learn("patronum", PatronusSpell)
        self.caster.forget("patronum")
        with self.assertRaises(NotFoundException):
            self.caster.find("patronum")

    def test_forget_unknown(self):
        self.caster.forget("patronum")

    def test_find(self):
        result = self.caster.find("patronus")
        self.assertEqual(result, PatronusSpell)

    async def test_craft_unknown(self):
        with self.assertRaises(NotFoundException):
            await self.caster.craft("Stupefy")

    async def test_craft_invalid_params(self):
        with self.assertRaises(ValidationError):
            await self.caster.craft("patronus")

    async def test_craft(self):
        spell = await self.caster.craft("patronus", shape="stag")
        self.assertIsInstance(spell, Spell)
        result = await spell.execute()
        self.assertEqual(result.data, "Expecto Patronum")

    async def test_craft_from_class(self):
        spell = await self.caster.craft(PatronusSpell, shape="stag")
        self.assertIsInstance(spell, Spell)
        result = await spell.execute()
        self.assertEqual(result.data, "Expecto Patronum")

    async def test_craft_invalid(self):
        def not_a_spell():
            pass

        with self.assertRaises(ValueError):
            await self.caster.craft(not_a_spell)

    async def test_cast(self):
        result = await self.caster.cast("patronus", shape="stag")
        self.assertEqual(result.data, "Expecto Patronum")

    async def test_cast_with_exception(self):
        result = await self.caster.cast("forbidden", shape="stag")
        self.assertEqual(result.status, SpellStatus.ABORTED)

    def test_describe_input(self):
        self.assertEqual(
            self.caster.describe_input("patronus"),
            {
                "title": "PatronusSpellParams",
                "type": "object",
                "properties": {"shape": {"title": "Shape", "type": "string"}},
                "required": ["shape"],
            },
        )

    def test_list(self):
        self.assertEqual(self.caster.list(), [("patronus", PatronusSpell)])

    def test_list_by_group(self):
        self.assertEqual(
            self.caster.list_by_group(), {None: [("patronus", PatronusSpell)]}
        )
        caster = SpellCaster()
        caster.learn("patronus", PatronusSpell, group="test")
        self.assertEqual(
            caster.list_by_group(), {"test": [("patronus", PatronusSpell)]}
        )
