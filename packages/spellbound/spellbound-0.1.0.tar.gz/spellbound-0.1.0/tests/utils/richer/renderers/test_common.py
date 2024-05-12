import unittest

from rich.console import Group as RichGroup
from rich.markdown import Markdown as RichMarkdown
from rich.text import Text as RichText

from spellbound.utils.richer.presets.common import common_richer
from spellbound.utils.richer.renderers.common import (
    ExceptionRenderer,
    MarkdownRenderer,
    MarkupRenderer,
    RenderableListRenderer,
)
from spellbound.utils.richer.wrappers import Markdown, Markup, RenderableList


class TestCommonRenderer(unittest.TestCase):
    def setUp(self):
        self.richer = common_richer

    def test_value_class(self):
        self.assertEqual(ExceptionRenderer.value_class(), Exception)
        self.assertEqual(MarkdownRenderer.value_class(), Markdown)
        self.assertEqual(MarkupRenderer.value_class(), Markup)
        self.assertEqual(RenderableListRenderer.value_class(), RenderableList)

    def test_render_exception(self):
        self.assertIsInstance(
            ExceptionRenderer(self.richer)(Exception("blah")),
            RichText,
        )

    def test_render_markdown(self):
        self.assertIsInstance(
            MarkdownRenderer(self.richer)(Markdown("blah")),
            RichMarkdown,
        )

    def test_render_markup(self):
        self.assertIsInstance(
            MarkupRenderer(self.richer)(Markup("blah")),
            RichText,
        )

    def test_render_renderable_list_empty(self):
        output = RenderableListRenderer(self.richer)(RenderableList([]))
        self.assertIsInstance(output, RichGroup)
        self.assertEqual(len(output._renderables), 0)

    def test_render_renderable_list(self):
        output = RenderableListRenderer(self.richer)(
            RenderableList(
                [
                    Markdown("blah"),
                    "foo",
                    Markup("blah"),
                ]
            )
        )
        self.assertIsInstance(output, RichGroup)
        self.assertEqual(len(output._renderables), 3)
        self.assertIsInstance(output._renderables[0], RichMarkdown)
        self.assertIsInstance(output._renderables[1], RichText)
        self.assertIsInstance(output._renderables[2], RichText)

    def test_render_renderable_list_nested(self):
        output = RenderableListRenderer(self.richer)(
            RenderableList(
                [
                    Markdown("blah"),
                    RenderableList(
                        [
                            "foo",
                            Markup("blah"),
                        ]
                    ),
                ]
            )
        )
        self.assertIsInstance(output, RichGroup)
        self.assertEqual(len(output._renderables), 2)
        self.assertIsInstance(output._renderables[0], RichMarkdown)
        self.assertIsInstance(output._renderables[1], RichGroup)
        self.assertEqual(len(output._renderables[1]._renderables), 2)
        self.assertIsInstance(output._renderables[1]._renderables[0], RichText)
        self.assertIsInstance(output._renderables[1]._renderables[1], RichText)
