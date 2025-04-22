from abc import abstractmethod
from typing import override

from core.exceptions import NoHandlerFoundException
from core.interfaces.visitor import Visitor
from core.opcodes import CoreOpcode
from core.opcodes.dtypes import Code, Program, Ptr, Value


class CoreVisitor(Visitor[CoreOpcode]):
    @override
    def visit(self, program: Program[CoreOpcode]) -> None:
        for opcode in program:
            if (method := getattr(self, opcode.__id__, None)) is None:
                raise NoHandlerFoundException(opcode, self)

            method(**opcode.args())

    @abstractmethod
    def add(self, ptr: Ptr, value: Value) -> None:
        raise NotImplementedError

    @abstractmethod
    def input(self, ptr: Ptr) -> None:
        raise NotImplementedError

    @abstractmethod
    def output(self, ptr: Ptr) -> None:
        raise NotImplementedError

    @abstractmethod
    def loop(self, ptr: Ptr, program: Program[CoreOpcode]) -> None:
        raise NotImplementedError

    @abstractmethod
    def inject(self, ptr: Ptr, code: Code, exit: Ptr) -> None:
        raise NotImplementedError
