from collections.abc import Callable, Iterable
from functools import wraps
from typing import Self

from rich.repr import Result, rich_repr

from quix.core.opcodes import CoreOpcode, CoreProgram
from quix.core.var import Var

type ToConvert = CoreProgram | CoreOpcode | SmartProgram | Var | Iterable[ToConvert] | None


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

    def builder(self) -> CoreProgram:
        return self._program

    def __rich_repr__(self) -> Result:
        yield from self._program


def to_program(data: ToConvert) -> SmartProgram:
    match data:
        case SmartProgram():
            return data
        case None:
            return SmartProgram()
        case Var():
            return SmartProgram(list(data.build()))
        case CoreOpcode():
            return SmartProgram([data])
        case Iterable():
            program: list[CoreOpcode] = []
            for value in data:
                new = to_program(value)
                program.extend(new.builder())
            return SmartProgram(program)
        case _:
            raise ValueError(f"Trying to cast an unsupported data to OpCodeReturn. {type(data).__name__}: {data}")


def macrocode[**P, R: ToConvert](func: Callable[P, R]) -> Callable[P, SmartProgram]:
    @wraps(func)
    def _wrapper(*args: P.args, **kwargs: P.kwargs) -> SmartProgram:
        return to_program(func(*args, **kwargs))

    return _wrapper
