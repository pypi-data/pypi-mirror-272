import abc
import logging
from contextlib import contextmanager
from timeit import default_timer as timer
from uuid import uuid4

from cached_property import cached_property
from pydantic import BaseModel

from spellbound.core.result import SpellResult, SpellStatus
from spellbound.utils.logging import pipe_logs
from spellbound.utils.text import kebab_case


class Spell(abc.ABC):
    description = "Description"
    InputParams = BaseModel

    @classmethod
    def spell_name(cls):
        name = cls.__name__
        if name.endswith("Spell"):
            name = name[:-5]
        return kebab_case(name)

    def __init__(self, **params):
        super().__init__()

        self._params = params
        self.uid = str(uuid4())
        self.logger = logging.Logger(f"{__name__}.{self.uid}", logging.WARNING)

        self.validate()

    @cached_property
    def params(self):
        return self.InputParams(**self._params)

    @contextmanager
    def slow(self, *args, **kwargs):
        """
        Mark a slow operation.

        Args:
            description (str): description of the slow operation

        Yields:
            None
        """
        yield

    def track_progress(self, iterable, **kwargs):
        """
        Track progress of an iterable.

        Args:
            iterable (Iterable): iterable to track
            kwargs (dict): kwargs to pass to track_progress

        Returns:
            Iterable: tracked iterable
        """
        return iterable

    def validate(self):
        """Validate the input against the schema."""
        # Create Pydantic class to trigger validation
        return self.params

    @contextmanager
    def consume_logs_from(self, loggers):
        """
        Consume logs from other logger(s).

        Args:
            logger (str|Logger|List[str|Logger]): logger name (str) or logger (Logger) or list of loggers to consume logs from

        Yields:
            None
        """
        with pipe_logs(loggers, self.logger):
            yield

    @abc.abstractmethod
    async def execute(self):
        """Execute the spell."""
        # Subclass only needs to implement this

    async def execute_and_continue(self):
        """
        Execute the spell and guarantee to return a SpellResult.
        If there is an exception, it will be caught and returned as a SpellResult.
        """
        start = timer()
        try:
            result = await self.execute()
            result.duration = timer() - start
            return result
        except Exception as exc:
            self.logger.exception("Exception during spell execution")
            return SpellResult(
                status=SpellStatus.ABORTED,
                data=exc,
                duration=timer() - start,
            )
