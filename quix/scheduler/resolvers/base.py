from abc import abstractmethod
from typing import Protocol

from quix.scheduler.blueprint import Blueprint
from quix.scheduler.layout import Layout


class Resolver(Protocol):
    __slots__ = ()

    @abstractmethod
    def __call__(self, blueprint: Blueprint) -> Layout:
        raise NotImplementedError
