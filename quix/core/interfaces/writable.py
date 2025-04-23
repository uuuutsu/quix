from abc import abstractmethod
from typing import Protocol


class Writable(Protocol):
    __slots__ = ()

    @abstractmethod
    def write(self, __value: str, /) -> int:
        raise NotImplementedError
