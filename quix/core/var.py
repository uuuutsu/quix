from __future__ import annotations

from quix.core.opcodes.base import CoreOpcode
from quix.core.opcodes.dtypes import Program, Ref, Value
from quix.core.opcodes.opcodes import add, inject, input, loop, output


def _opcode_to_uniform_program(value: CoreOpcode | Program | Var, /) -> Program:
    match value:
        case CoreOpcode():
            return [value]
        case Var():
            return value.program
        case Program():
            return value


class Var:
    __slots__ = "_ref", "program", "_name"

    def __init__(self, ref: Ref, name: str | None = None, program: Program | None = None) -> None:
        self._ref = ref
        self._name = name
        self.program = program or []

    def __add__(self, value: Value) -> Var:
        return self._concat_program(add(self._ref, value))

    def __getitem__(self, key: CoreOpcode | Var | Program) -> Var:
        return self._concat_program(loop(self._ref, _opcode_to_uniform_program(key)))

    def output(self) -> Var:
        return self._concat_program(output(self._ref))

    def input(self) -> Var:
        return self._concat_program(input(self._ref))

    def __call__(self, code: str, exit: Ref) -> Var:
        return self._concat_program(inject(self._ref, code, exit))

    def __str__(self) -> str:
        return f"{type(self).__name__}( {self._name or self._ref} )"

    def build(self) -> Program:
        return self.program

    def _concat_program(self, other: Program | CoreOpcode | Var) -> Var:
        return Var(self._ref, self._name, [self._ref, *_opcode_to_uniform_program(other)])
