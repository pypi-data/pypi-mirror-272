import logging

from rich.console import Console
from rich.logging import RichHandler

from spellbound.core.caster import PreExecuteEvent, SpellEvent
from spellbound.utils.interceptor import Interceptor


class RichLogInterceptor(Interceptor):
    def __init__(self, console=None):
        super().__init__()
        self.console = console or Console()

    def _configure(self, when):
        when(SpellEvent.PRE_EXECUTE, self._capture_logs)

    def _capture_logs(self, event: PreExecuteEvent):
        caster = event.caster
        spell = event.spell

        is_debug = caster.log_level == logging.DEBUG
        log_handler = RichHandler(
            level=caster.log_level,
            console=self.console,
            rich_tracebacks=is_debug,
            tracebacks_show_locals=is_debug,
        )
        log_handler.setFormatter(logging.Formatter("%(message)s"))
        spell.logger.addHandler(log_handler)
