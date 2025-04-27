from abc import abstractmethod
from typing import Protocol


class Readable(Protocol):
    __slots__ = ()

    @abstractmethod
    def read(self, __value: int, /) -> str:
        raise NotImplementedError
