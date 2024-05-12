import logging

from spellbound.core.caster import PostExecuteEvent, SpellEvent
from spellbound.utils.interceptor import Interceptor

logger = logging.getLogger(__name__)


class SimpleOutputInterceptor(Interceptor):
    def _configure(self, when):
        when(SpellEvent.POST_EXECUTE, self._capture_output)

    def _capture_output(self, event: PostExecuteEvent):
        result = event.result
        logger.info(result.get_title())

        if result.data:
            if result.is_error():
                logger.error(result.data)
            else:
                logger.info(result.data)
