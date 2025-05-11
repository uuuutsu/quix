from enum import StrEnum

from .base import opcode
from .dtypes import Code, Ref, Value


@opcode
def add(ref: Ref | None, value: Value) -> None: ...
@opcode
def input(ref: Ref | None) -> None: ...
@opcode
def output(ref: Ref | None) -> None: ...
@opcode
def start_loop(ref: Ref | None) -> None: ...
@opcode
def end_loop() -> None: ...
@opcode
def inject(ref: Ref | None, code: Code, exit: Ref | None, sortable: bool = False) -> None: ...


class CoreOpcodes(StrEnum):
    ADD = "add"
    INPUT = "input"
    OUTPUT = "output"
    START_LOOP = "start_loop"
    END_LOOP = "end_loop"
    INJECT = "inject"
