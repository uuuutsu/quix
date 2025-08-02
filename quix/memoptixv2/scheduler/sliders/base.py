from abc import abstractmethod
from typing import ClassVar, Protocol

from quix.memoptixv2.scheduler.layout import Layout
from quix.memoptixv2.scheduler.tree import BaseConstraint


class Slider(Protocol):
    __slots__ = ()

    __domain__: ClassVar[set[type[BaseConstraint]]]

    @abstractmethod
    def __call__(self, left: Layout, right: Layout) -> Layout:
        raise NotImplementedError
