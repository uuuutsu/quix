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

            return method(**opcode.args())

    @abstractmethod
    def add(ptr: Ptr, value: Value) -> None:
        raise NotImplementedError

    @abstractmethod
    def input(ptr: Ptr) -> None:
        raise NotImplementedError

    @abstractmethod
    def output(ptr: Ptr) -> None:
        raise NotImplementedError

    @abstractmethod
    def loop(ptr: Ptr, program: Program) -> None:
        raise NotImplementedError

    @abstractmethod
    def inject(ptr: Ptr, code: Code, exit: Ptr) -> None:
        raise NotImplementedError
