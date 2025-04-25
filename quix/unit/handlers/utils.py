from collections.abc import Callable, Iterable
from functools import wraps
from typing import Self

from rich.repr import Result, rich_repr

from quix.core.interfaces.opcode import Opcode, Program
from quix.core.var import Var
from quix.scheduler.blueprint import Blueprint

type ToConvert = Program[Opcode] | None | Opcode | SmartProgram | Var | Blueprint | Iterable[ToConvert]


@rich_repr
class SmartProgram:
    __slots__ = (
        "program",
        "bps",
    )

    program: list[Opcode]
    bps: list[Blueprint]

    def __init__(
        self,
        program: list[Opcode] | None = None,
        bps: list[Blueprint] | None = None,
    ) -> None:
        self.program = program or []
        self.bps = bps or []

    def __or__(self, other: ToConvert) -> Self:
        if isinstance(other, SmartProgram):
            self.program.extend(other.program)
            self.bps.extend(other.bps)
            return self

        return self | _to_program(other)

    def __rich_repr__(self) -> Result:
        yield from self.program
        yield from self.bps


def _to_program(data: ToConvert) -> SmartProgram:
    match data:
        case SmartProgram():
            return data
        case None:
            return SmartProgram()
        case Var():
            return SmartProgram(list(data.build()))
        case Opcode():
            return SmartProgram([data])
        case Blueprint():
            return SmartProgram([], [data])
        case Iterable():
            program: list[Opcode] = []
            bps: list[Blueprint] = []
            for value in data:
                new = _to_program(value)
                program.extend(new.program)
                bps.extend(new.bps)
            return SmartProgram(program, bps)
        case _:
            raise ValueError(f"Trying to cast an unsupported data to OpCodeReturn. {type(data).__name__}: {data}")


def handler[**P, R: ToConvert](func: Callable[P, R]) -> Callable[P, SmartProgram]:
    @wraps(func)
    def _wrapper(*args: P.args, **kwargs: P.kwargs) -> SmartProgram:
        return _to_program(func(*args, **kwargs))

    return _wrapper
