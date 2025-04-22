from abc import abstractmethod
from typing import Protocol

from .opcode import Opcode, Program


class Visitor[O: Opcode](Protocol):
    __slots__ = ()

    @abstractmethod
    def visit(self, program: Program[O]) -> None:
        raise NotImplementedError
