from collections.abc import Callable, Iterable
from functools import wraps
from typing import Self

from rich.repr import Result, rich_repr

from quix.core.interfaces.opcode import Opcode, Program

type ToConvert = Program[Opcode] | None | Opcode | Iterable[ToConvert] | SmartProgram


@rich_repr
class SmartProgram:
    __slots__ = ("_program",)
    _program: list[Opcode]

    def __init__(self, program: list[Opcode] | None = None) -> None:
        self._program = program or []

    def __or__(self, other: ToConvert) -> Self:
        if isinstance(other, SmartProgram):
            self._program.extend(other._program)
            return self

        return self | _to_program(other)

    def __rich_repr__(self) -> Result:
        yield from self._program


def _to_program(data: ToConvert) -> SmartProgram:
    match data:
        case SmartProgram():
            return data
        case None:
            return SmartProgram()
        case Program():
            return SmartProgram(list(*data))
        case Opcode():
            return SmartProgram([data])
        case Iterable():
            program = []
            for value in data:
                program.extend(*_to_program(value)._program)
            return SmartProgram(program)
        case _:
            raise ValueError(f"Trying to cast an unsupported data to OpCodeReturn. {type(data).__name__}: {data}")


def handler[**P, R: ToConvert](func: Callable[P, R]) -> Callable[P, SmartProgram]:
    @wraps(func)
    def _wrapper(*args: P.args, **kwargs: P.kwargs) -> SmartProgram:
        return _to_program(func(*args, **kwargs))

    return _wrapper
