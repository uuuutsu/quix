from abc import abstractmethod
from typing import ClassVar, Protocol

from quix.scheduler.constraints import BaseConstraint
from quix.scheduler.layout import Layout


class Slider(Protocol):
    __slots__ = ()

    __domain__: ClassVar[set[type[BaseConstraint]]]

    @abstractmethod
    def __call__(self, left: Layout, right: Layout) -> Layout:
        raise NotImplementedError
