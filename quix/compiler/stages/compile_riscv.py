from quix.bootstrap.program import ToConvert
from quix.riscv.compiler.compiler import Compiler
from quix.riscv.loader.state import State

from .base import Stage


class CompileRISCV(Stage[State, ToConvert]):
    __slots__ = ()

    def _execute(self, __data: State) -> ToConvert:
        comp = Compiler()
        return comp.run(__data).program
