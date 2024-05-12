from spellbound.utils.richer.core.richer import Richer
from spellbound.utils.richer.renderers.common import (
    ExceptionRenderer,
    MarkdownRenderer,
    MarkupRenderer,
    RenderableListRenderer,
    SyntaxRenderer,
)
from spellbound.utils.richer.renderers.spell_result import SpellResultRenderer


def common_preset(richer):
    richer.register(ExceptionRenderer)
    richer.register(MarkdownRenderer)
    richer.register(MarkupRenderer)
    richer.register(RenderableListRenderer)
    richer.register(SyntaxRenderer)
    richer.register(SpellResultRenderer)


# singleton
common_richer = Richer()
common_richer.apply(common_preset)
