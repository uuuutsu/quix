from typing import Any

from quix.core.interfaces.opcode import Opcode

from .base import CoreException


class VisitorException(CoreException): ...


class NoHandlerFoundException(VisitorException):
    def __init__[O: Opcode](self, opcode: O, visitor: Any) -> None:
        self.opcode = opcode
        super().__init__(f"No handler found in {visitor} for opcode {opcode}.")
