from typing import Final, Self

from quix.core.opcodes.dtypes import Code, Ptr

from .commands import BFCommands

_DEFAULT_START: Final[Ptr] = 0


class BFPointer:
    __slots__ = ("_curr_pos",)

    def __init__(self, start_position: Ptr = _DEFAULT_START) -> None:
        self._curr_pos = start_position

    def move(self, new_position: Ptr, /) -> Code:
        sign = BFCommands.MOVE_LEFT if new_position < self._curr_pos else BFCommands.MOVE_RIGHT
        return sign * abs(new_position - self._curr_pos)

    @classmethod
    def default(cls) -> Self:
        return cls(_DEFAULT_START)
