from abc import ABC, abstractmethod

from quix.memoptix.scheduler.owner import Owner


class BaseConstraint(ABC):
    __slots__ = ()

    @abstractmethod
    def get_owners(self) -> set[Owner]:
        raise NotImplementedError

    def __repr__(self) -> str:
        return type(self).__name__
