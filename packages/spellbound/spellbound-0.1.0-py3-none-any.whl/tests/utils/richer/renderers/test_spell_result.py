import unittest

from rich.console import Group
from rich.text import Text

from spellbound.core.result import SpellResult, SpellStatus
from spellbound.utils.richer.core.renderer import RichRenderer
from spellbound.utils.richer.core.richer import Richer
from spellbound.utils.richer.renderers.spell_result import SpellResultRenderer


class Sample:
    def __init__(self, text):
        self.text = text


class SampleRenderer(RichRenderer):
    @classmethod
    def value_class(cls):
        return Sample

    def __call__(self, value):
        return Text(value.text)


class TestMinervaDiffRenderer(unittest.TestCase):
    def setUp(self):
        richer = Richer()
        richer.register(SampleRenderer)

        self.renderer = SpellResultRenderer(richer)
        return super().setUp()

    def test_value_class(self):
        self.assertEqual(SpellResultRenderer.value_class(), SpellResult)

    def test_render_title_only(self):
        output = self.renderer(SpellResult(status=SpellStatus.SUCCESS, title="test"))
        self.assertIsInstance(output, Group)

    def test_render_with_unknown_data(self):
        output = self.renderer(
            SpellResult(
                status=SpellStatus.SUCCESS,
                title="test",
                data={"blah": "blah"},
            )
        )
        self.assertIsInstance(output, Group)

    def test_render_with_data(self):
        output = self.renderer(
            SpellResult(
                status=SpellStatus.SUCCESS,
                title="test",
                data=Sample("test"),
            )
        )
        self.assertIsInstance(output, Group)
