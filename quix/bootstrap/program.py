from __future__ import annotations

from collections.abc import Callable, Iterable
from functools import wraps
from typing import Self

from rich.repr import Result, rich_repr

from quix.core.opcodes import CoreOpcode, CoreProgram

type ToConvert = CoreProgram | CoreOpcode | SmartProgram | Iterable[ToConvert] | None


@rich_repr
class SmartProgram:
    __slots__ = ("_program",)

    _program: list[CoreOpcode]

    def __init__(
        self,
        program: list[CoreOpcode] | None = None,
    ) -> None:
        self._program = program or []

    def __or__(self, other: ToConvert) -> Self:
        if isinstance(other, SmartProgram):
            self._program.extend(other._program)
            return self

        return self | to_program(other)

    def __ror__(self, other: ToConvert) -> SmartProgram:
        return to_program(other) | self

    def build(self) -> CoreProgram:
        return self._program

    def __rich_repr__(self) -> Result:
        yield from self._program


def to_program(data: ToConvert, *include: ToConvert) -> SmartProgram:
    if include:
        data = (data, include)

    match data:
        case SmartProgram():
            return data
        case None:
            return SmartProgram()
        case CoreOpcode():
            return SmartProgram([data])
        case Iterable():
            program: list[CoreOpcode] = []
            for value in data:
                new = to_program(value)
                program.extend(new.build())
            return SmartProgram(program)
        case _:
            raise ValueError(f"Trying to cast an unsupported data to OpCodeReturn. {type(data).__name__}: {data}")


def convert[**P, R: ToConvert](func: Callable[P, R]) -> Callable[P, SmartProgram]:
    @wraps(func)
    def _wrapper(*args: P.args, **kwargs: P.kwargs) -> SmartProgram:
        return to_program(func(*args, **kwargs))

    return _wrapper
