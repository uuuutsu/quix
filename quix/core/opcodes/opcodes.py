from enum import StrEnum

from .base import opcode
from .dtypes import Code, CoreProgram, Ref, Value


@opcode
def add(ref: Ref | None, value: Value) -> None: ...
@opcode
def input(ref: Ref | None) -> None: ...
@opcode
def output(ref: Ref | None) -> None: ...
@opcode
def loop(ref: Ref | None, program: CoreProgram) -> None: ...
@opcode
def inject(ref: Ref | None, code: Code, exit: Ref | None, sortable: bool = False) -> None: ...


class CoreOpcodes(StrEnum):
    ADD = "add"
    INPUT = "input"
    OUTPUT = "output"
    LOOP = "loop"
    INJECT = "inject"
