from pydantic import ValidationError

from spellbound.core.result import SpellStatus
from spellbound.core.spell import Spell
from tests.helpers.async_case import IsolatedAsyncioTestCase


class DisarmSpellParams(Spell.InputParams):
    param1: str
    param2: str


class DisarmSpell(Spell):
    InputParams = DisarmSpellParams

    async def execute(self):
        return "Expelliarmus"


class LongWeirdNameSpell(Spell):
    pass


class PoorSpell(Spell):
    async def execute(self):
        raise Exception("Something went wrong")


class TestSpell(IsolatedAsyncioTestCase):
    def test_init(self):
        spell = DisarmSpell(param1="value1", param2="value2")
        self.assertEqual(spell.params.param1, "value1")
        self.assertEqual(spell.params.param2, "value2")

    def test_init_with_invalid_params(self):
        with self.assertRaises(ValidationError):
            DisarmSpell(param1=None, param2="value2")

    def test_validate(self):
        spell = DisarmSpell(param1="value1", param2="value2")
        spell.validate()

    def test_spell_name(self):
        self.assertEqual(DisarmSpell.spell_name(), "disarm")
        self.assertEqual(LongWeirdNameSpell.spell_name(), "long-weird-name")

    async def test_execute(self):
        spell = DisarmSpell(param1="value1", param2="value2")
        result = await spell.execute()
        self.assertEqual(result, "Expelliarmus")

    async def test_execute_raises_exception(self):
        spell = PoorSpell()
        with self.assertRaises(Exception):
            await spell.execute()

    async def test_execute_and_continue(self):
        spell = PoorSpell()
        result = await spell.execute_and_continue()
        self.assertEqual(result.status, SpellStatus.ABORTED)
        self.assertIsInstance(result.data, Exception)

    def test_track_progress(self):
        spell = DisarmSpell(param1="value1", param2="value2")
        result = []
        for x in spell.track_progress([1, 2, 3]):
            result.append(x)
        self.assertEqual(result, [1, 2, 3])
