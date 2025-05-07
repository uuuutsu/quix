from abc import ABC, abstractmethod

from quix.bootstrap.program import SmartProgram


class Component(ABC):
    @abstractmethod
    def create(self, memory_index: int) -> SmartProgram:
        raise NotImplementedError

    @abstractmethod
    def size(self) -> int:
        raise NotImplementedError
