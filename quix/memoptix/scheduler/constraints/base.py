from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from typing import Any, Self

from quix.memoptix.scheduler.owner import Owner
from quix.tools.state import statable


@dataclass(slots=True, frozen=True)
@statable
class BaseConstraint(ABC):
    @abstractmethod
    def get_owners(self) -> set[Owner]:
        raise NotImplementedError

    def __store__(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def __load__(cls, data: dict[str, Any]) -> Self:
        return cls(**data)
