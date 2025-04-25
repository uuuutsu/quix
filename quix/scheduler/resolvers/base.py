from abc import abstractmethod
from typing import ClassVar, Protocol

from quix.scheduler.blueprint import Blueprint
from quix.scheduler.constraints import BaseConstraint
from quix.scheduler.layout import Layout


class Resolver(Protocol):
    __slots__ = ()

    __domain__: ClassVar[set[type[BaseConstraint]]]

    @abstractmethod
    def __call__(self, blueprint: Blueprint) -> Layout:
        raise NotImplementedError
