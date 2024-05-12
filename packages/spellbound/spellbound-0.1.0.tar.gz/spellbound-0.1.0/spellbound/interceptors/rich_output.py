from rich.console import Console

from spellbound.core.caster import PostExecuteEvent, SpellEvent
from spellbound.utils.interceptor import Interceptor
from spellbound.utils.richer.presets.common import common_richer


class RichOutputInterceptor(Interceptor):
    def __init__(self, console=None, richer=None):
        super().__init__()
        self.console = console or Console()
        self.richer = richer or common_richer

    def _configure(self, when):
        when(SpellEvent.POST_EXECUTE, self._capture_output)

    def _capture_output(self, event: PostExecuteEvent):
        # Create rich Renderable
        renderable = self.richer.render(event.result)

        # Use rich for printing
        self.console.print()
        self.console.print(renderable)
