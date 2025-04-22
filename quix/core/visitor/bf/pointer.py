from typing import Final, Self

from quix.core.opcodes.dtypes import Code, Ref

from .commands import BFCommands
from .layout import BFMemoryLayout
from .types import Ptr

_DEFAULT_START: Final[Ptr] = 0


class BFPointer:
    __slots__ = (
        "_curr_pos",
        "_layout",
    )

    def __init__(self, layout: BFMemoryLayout, start_position: Ptr = _DEFAULT_START) -> None:
        self._curr_pos = start_position
        self._layout = layout

    def move_by_ptr(self, ptr: Ptr, /) -> Code:
        sign = BFCommands.MOVE_LEFT if ptr < self._curr_pos else BFCommands.MOVE_RIGHT
        self._curr_pos, _curr_pos = ptr, self._curr_pos
        return sign * abs(ptr - _curr_pos)

    def move_by_ref(self, ref: Ref, /) -> Code:
        return self.move_by_ptr(self._layout[ref])

    @classmethod
    def default(cls) -> Self:
        return cls(BFMemoryLayout.default(), _DEFAULT_START)
