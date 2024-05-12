import functools

import rich.progress
from rich.console import Console

from spellbound.core.caster import PreExecuteEvent, SpellEvent
from spellbound.utils.interceptor import Interceptor


class RichProgressInterceptor(Interceptor):
    def __init__(self, console=None):
        super().__init__()
        self.console = console or Console()

    def _configure(self, when):
        when(SpellEvent.PRE_EXECUTE, self._capture_progress)

    def _capture_progress(self, event: PreExecuteEvent):
        spell = event.spell

        spell.slow = self.console.status
        spell.track_progress = functools.partial(
            rich.progress.track,
            console=self.console,
        )
