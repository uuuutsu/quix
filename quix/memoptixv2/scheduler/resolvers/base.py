from abc import abstractmethod
from typing import ClassVar, Protocol

from quix.memoptixv2.scheduler.layout import Layout
from quix.memoptixv2.scheduler.tree import Node

from .types import Domain


class Resolver(Protocol):
    __slots__ = ()

    __domain__: ClassVar[Domain]

    @abstractmethod
    def __call__(self, node: Node) -> Layout:
        raise NotImplementedError
