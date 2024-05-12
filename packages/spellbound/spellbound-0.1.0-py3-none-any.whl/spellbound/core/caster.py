import inspect
import logging
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Union

from spellbound.core.book import SpellBook
from spellbound.core.result import SpellResult, SpellStatus
from spellbound.core.spell import Spell
from spellbound.utils.emitter import Emitter
from spellbound.utils.exception import NotFoundException
from spellbound.utils.inject import FakeInjector, Injector
from spellbound.utils.apply import ApplyMixin


class SpellEvent(str, Enum):
    POST_CRAFT = "post-craft"
    PRE_EXECUTE = "pre-execute"
    POST_EXECUTE = "post-execute"


class SpellCaster(ApplyMixin, Emitter):
    def __init__(self, injector:Injector=None):
        super().__init__()

        self.injector = injector or FakeInjector()
        self._book = SpellBook()
        self.log_level = logging.WARNING
        self._spell_to_group = {}

    def set_spell_group(self, name, group):
        """
        Set the group for a spell.

        Args:
            name (str): spell name
            group (str): spell group
        """
        self._spell_to_group[name] = group

    def learn(self, name, spell_class, group=None):
        """
        Learn a new spell.

        Args:
            name (str): spell name
            spell_class (class): spell class to learn

        Returns:
            SpellCaster: this spell caster
        """
        self._book.register(name, spell_class)
        self.set_spell_group(name, group)
        return self

    def learn_all(self, book, group=None):
        """
        Learn all spells from another book.

        Args:
            book (SpellBook): another spell book

        Returns:
            SpellCaster: this spell caster
        """
        self._book.update(book)
        for name in book.spells:
            self.set_spell_group(name, group)
        return self

    def forget(self, name):
        """
        Forget a spell.

        Args:
            name (str): spell name

        Returns:
            SpellCaster: this spell caster
        """
        if name in self._book.spells:
            del self._book.spells[name]
        if name in self._spell_to_group:
            del self._spell_to_group[name]
        return self

    def find(self, name):
        """
        Find a spell class by name.

        Args:
            name (str): spell name

        Returns:
            class: spell class
        """
        try:
            return self._book.find(name)
        except NotFoundException as exc:
            raise NotFoundException(
                f"This caster does not know Spell `{name}`."
            ) from exc

    async def craft(self, name, **params):
        """
        Create a new spell instance from the given spell name and parameters.

        Args:
            name (str): spell name or class
            **params (dict): parameters for the spell

        Returns:
            Spell: spell instance
        """
        try:
            if isinstance(name, str):
                spell_class = self.find(name)
                spell_name = name
            elif inspect.isclass(name) and issubclass(name, Spell):
                spell_class = name
                spell_name = spell_class.spell_name()
            else:
                raise ValueError(f"Invalid spell name: {name}")

            spell = self.injector.get(spell_class, **params)
            spell.name = spell_name

            self.trigger(
                SpellEvent.POST_CRAFT,
                PostCraftEvent(
                    caster=self,
                    spell_name=spell_name,
                    params=params,
                    spell=spell,
                ),
            )
            return spell
        except Exception as exc:
            self.trigger(
                SpellEvent.POST_CRAFT,
                PostCraftEvent(
                    caster=self,
                    spell_name=name,
                    params=params,
                    spell=None,
                ),
            )
            raise exc

    async def cast(self, name, **params):
        """
        Craft and execute a new spell instance from the given spell name and parameters.
        Equivalent to calling `craft` and then `execute` on the result.

        Args:
            name (str): spell name

        Returns:
            SpellResult: result of this spell
        """
        try:
            spell = await self.craft(name, **params)
        except Exception as exc:
            spell = None
            result = SpellResult(
                status=SpellStatus.ABORTED,
                data=exc,
            )

        if spell:
            # Set log level for spell
            spell.logger.setLevel(self.log_level)

            self.trigger(
                SpellEvent.PRE_EXECUTE,
                PreExecuteEvent(
                    caster=self,
                    spell_name=name,
                    params=params,
                    spell=spell,
                ),
            )

            result = await spell.execute_and_continue()
            spell.logger.handlers.clear()

        result.spell_name = name

        self.trigger(
            SpellEvent.POST_EXECUTE,
            PostExecuteEvent(
                caster=self,
                spell_name=name,
                params=params,
                spell=spell,
                result=result,
            ),
        )

        return result

    def describe_input(self, name):
        """
        Describe the input parameters for the given spell.

        Args:
            name (str): spell name

        Returns:
            str: description of input parameters
        """
        return self.find(name).InputParams.schema()

    def list(self):
        """
        Return a list of all spells known to this caster.

        Returns:
            List[Tuple(name, spell_class)]: list of spells
        """
        return self._book.to_list()

    def list_by_group(self):
        """
        Return a list of all spells known to this caster grouped by group.

        Returns:
            Dict[group, List[Tuple(name, spell_class)]]: list of spells
        """
        spells = self._book.to_list()
        spell_groups = {}
        for name, spell_class in spells:
            group = self._spell_to_group[name]
            if group not in spell_groups:
                spell_groups[group] = []
            spell_groups[group].append((name, spell_class))
        return spell_groups


@dataclass(frozen=True)
class PostCraftEvent:
    caster: SpellCaster
    spell_name: str
    params: dict
    spell: Optional[Spell] = None


@dataclass(frozen=True)
class PreExecuteEvent:
    caster: SpellCaster
    spell_name: str
    params: dict
    spell: Spell


@dataclass(frozen=True)
class PostExecuteEvent:
    caster: SpellCaster
    spell_name: str
    params: dict
    spell: Union[Spell, None]
    result: SpellResult
