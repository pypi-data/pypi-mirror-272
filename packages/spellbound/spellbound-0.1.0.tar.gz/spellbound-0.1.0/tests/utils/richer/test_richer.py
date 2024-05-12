import unittest

from rich.text import Text

from spellbound.utils.richer.core.renderer import RichRenderer
from spellbound.utils.richer.core.richer import Richer
from spellbound.utils.richer.presets.common import common_richer


class Sample:
    def __init__(self, text):
        self.text = text


class SampleRenderer(RichRenderer):
    @classmethod
    def value_class(cls):
        return Sample

    def __call__(self, value):
        return Text(value.text)


class NotRenderer:
    pass


class NoValueClassRenderer(RichRenderer):
    def __call__(self, value):
        return Text(value)


class TestRicher(unittest.TestCase):
    def test_register(self):
        richer = Richer()
        richer.register(SampleRenderer)
        self.assertIsInstance(richer._renderers[Sample], SampleRenderer)

    def test_register_non_renderer(self):
        richer = Richer()
        with self.assertRaises(TypeError):
            richer.register(NotRenderer)

    def test_register_no_value_class(self):
        richer = Richer()
        with self.assertRaises(ValueError):
            richer.register(NoValueClassRenderer)

    def test_render(self):
        richer = Richer()
        richer.register(SampleRenderer)
        output = richer.render(Sample("test"))
        self.assertIsInstance(output, Text)

    def test_render_no_renderer(self):
        richer = Richer()
        self.assertIsNone(richer.render(Sample("test")))

    def test_richer_fallback_renderer(self):
        richer = Richer()
        richer.register(SampleRenderer)
        output = richer.render(Sample("test"), fallback_renderer=lambda x: Text(str(x)))
        self.assertIsInstance(output, Text)

    def test_render_renderable(self):
        x = Text("test")
        self.assertIs(x, common_richer.render(x))
