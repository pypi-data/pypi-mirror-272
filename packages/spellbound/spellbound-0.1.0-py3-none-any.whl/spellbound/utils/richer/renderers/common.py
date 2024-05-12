from rich.console import Group as RichGroup
from rich.markdown import Markdown as RichMarkdown
from rich.syntax import Syntax as RichSyntax
from rich.text import Text as RichText

from spellbound.utils.richer.core.renderer import RichRenderer
from spellbound.utils.richer.wrappers import Markdown, Markup, RenderableList, Syntax


def _to_rich_text(value):
    return RichText(str(value))


class ExceptionRenderer(RichRenderer):
    @classmethod
    def value_class(cls):
        return Exception

    def __call__(self, value):
        text = f"[red]{type(value).__name__}:[/red] {value}"
        return RichText.from_markup(text)


class MarkdownRenderer(RichRenderer):
    @classmethod
    def value_class(cls):
        return Markdown

    def __call__(self, value):
        return RichMarkdown(value)


class MarkupRenderer(RichRenderer):
    @classmethod
    def value_class(cls):
        return Markup

    def __call__(self, value):
        return RichText.from_markup(value)


class RenderableListRenderer(RichRenderer):
    @classmethod
    def value_class(cls):
        return RenderableList

    def __call__(self, value):
        outputs = [
            self.richer.render(item, fallback_renderer=_to_rich_text) for item in value
        ]
        return RichGroup(*outputs)


class SyntaxRenderer(RichRenderer):
    @classmethod
    def value_class(cls):
        return Syntax

    def __call__(self, value):
        return RichSyntax(value.code, value.language)
