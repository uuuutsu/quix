from __future__ import annotations

from typing import overload

from quix.core.opcodes.base import CoreOpcode
from quix.core.opcodes.dtypes import CoreProgram, Ref, Value
from quix.core.opcodes.opcodes import add, inject, input, loop, output
from quix.tools import generate_unique_id

type ReducibleToProgram = CoreOpcode | CoreProgram | Var | tuple[Var, ...]


def _to_program(value: ReducibleToProgram, /) -> CoreProgram:
    match value:
        case CoreOpcode():
            return [value]
        case Var():
            return value._program
        case tuple():
            program: list[CoreOpcode] = []
            for var in value:
                program.extend(var._program)
            return program
    return value


class Var:
    __slots__ = "_ref", "_program", "_name"

    def __init__(
        self,
        ref: Ref,
        name: str | None = None,
        program: CoreProgram | None = None,
    ) -> None:
        self._ref = ref
        self._name = name
        self._program: CoreProgram = program or []

    def __add__(self, value: Value) -> Var:
        return self._concat_program(add(self._ref, value))

    def __sub__(self, value: Value) -> Var:
        return self.__add__(-value)

    def __getitem__(self, key: ReducibleToProgram) -> Var:
        return self._concat_program(loop(self._ref, _to_program(key)))

    def output(self) -> Var:
        return self._concat_program(output(self._ref))

    def input(self) -> Var:
        return self._concat_program(input(self._ref))

    def __call__(self, code: str, exit: Ref | None = None) -> Var:
        exit = self._ref if exit is None else exit
        return self._concat_program(inject(self._ref, code, exit))

    def __repr__(self) -> str:
        return f"{type(self).__name__}( {self._name or self._ref} )"

    def build(self) -> CoreProgram:
        return self._program

    def _concat_program(self, other: ReducibleToProgram) -> Var:
        return Var(self._ref, self._name, [*self._program, *_to_program(other)])


@overload
def var(name: str | None) -> Var: ...
@overload
def var(name: str | None, ref: Ref) -> Var: ...
def var(name: str | None = None, ref: Ref | None = None) -> Var:
    if ref is None:
        ref = generate_unique_id()
    return Var(ref=ref, name=name)
