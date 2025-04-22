from abc import abstractmethod
from typing import Protocol


class Writable(Protocol):
    @abstractmethod
    def write(self, __value: str, /) -> None:
        raise NotImplementedError
