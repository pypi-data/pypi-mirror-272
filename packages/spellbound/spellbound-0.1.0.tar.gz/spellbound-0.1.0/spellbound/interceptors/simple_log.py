import logging

from spellbound.core.caster import PreExecuteEvent, SpellEvent
from spellbound.utils.interceptor import Interceptor
from spellbound.utils.logging import PipeHandler

logger = logging.getLogger(__name__)


class SimpleLogInterceptor(Interceptor):
    def _configure(self, when):
        when(SpellEvent.PRE_EXECUTE, self._capture_logs)

    def _capture_logs(self, event: PreExecuteEvent):
        caster = event.caster
        spell = event.spell

        log_handler = PipeHandler(logger)
        log_handler.setLevel(caster.log_level)
        spell.logger.addHandler(log_handler)
