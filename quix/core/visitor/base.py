from abc import abstractmethod
from typing import override

from quix.core.interfaces.visitor import Visitor
from quix.core.opcodes import CoreOpcode
from quix.core.opcodes.dtypes import Code, CoreProgram, Ref, Value
from quix.exceptions.core import NoHandlerFoundException


class CoreVisitor(Visitor[CoreOpcode]):
    __slots__ = ()

    @override
    def visit(self, program: CoreProgram) -> None:
        for opcode in program:
            if (method := getattr(self, opcode.__id__, None)) is None:
                raise NoHandlerFoundException(opcode, self)

            method(**opcode.args())

    @abstractmethod
    def add(self, ref: Ref, value: Value) -> None:
        raise NotImplementedError

    @abstractmethod
    def input(self, ref: Ref) -> None:
        raise NotImplementedError

    @abstractmethod
    def output(self, ref: Ref) -> None:
        raise NotImplementedError

    @abstractmethod
    def loop(self, ref: Ref, program: CoreProgram) -> None:
        raise NotImplementedError

    @abstractmethod
    def inject(self, ref: Ref, code: Code, exit: Ref) -> None:
        raise NotImplementedError
