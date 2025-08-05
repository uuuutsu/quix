from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from typing import Any, Self

from rich.repr import Result, rich_repr

from quix.memoptix.scheduler.tree.node import Node
from quix.tools.state import statable


@dataclass(slots=True, frozen=True)
@rich_repr
@statable
class BaseConstraint(ABC):
    @abstractmethod
    def get_nodes(self) -> set[Node]:
        raise NotImplementedError

    def __store__(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def __load__(cls, data: dict[str, Any]) -> Self:
        return cls(**data)

    def __rich_repr__(self) -> Result:
        yield "type", self.__class__.__name__
        yield "nodes", self.get_nodes()
