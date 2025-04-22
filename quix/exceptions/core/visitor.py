from quix.core.interfaces.opcode import Opcode
from quix.core.interfaces.visitor import Visitor

from .base import CoreException


class VisitorException(CoreException): ...


class NoHandlerFoundException(VisitorException):
    __slots__ = ("opcode",)

    def __init__[O: Opcode](self, opcode: O, visitor: Visitor[O]) -> None:
        self.opcode = opcode
        super().__init__(f"No handler found in {visitor} for opcode {opcode}.")
