from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel


class SpellStatus(str, Enum):
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    ABORTED = "ABORTED"
    SKIPPED = "SKIPPED"


ERROR_STATUSES = (SpellStatus.FAILURE, SpellStatus.ABORTED)


class SpellResult(BaseModel):
    status: SpellStatus
    title: Optional[str] = None
    data: Optional[Any] = None
    description: Optional[str] = None
    spell_name: Optional[str] = None
    duration: Optional[float] = None

    def is_error(self):
        return self.status in ERROR_STATUSES

    def get_title(self):
        if self.title:
            return self.title

        name = self.spell_name or "Spell"

        if self.status == SpellStatus.SUCCESS:
            return f"`{name}` was completed successfully."
        if self.status == SpellStatus.FAILURE:
            return f"`{name}` has failed."
        if self.status == SpellStatus.ABORTED:
            return f"`{name}` was aborted during execution."

        return f"`{name}` was skipped."
