from typing import Final

from quix.core.visitor.bf import BFMemoryLayout, BFPointer
from quix.core.visitor.bf.commands import BFCommands


def test_pointer_default() -> None:
    pointer = BFPointer.default()
    assert pointer.position == 0

    code = pointer.move_by_ptr(10)
    assert code == BFCommands.MOVE_RIGHT * 10
    assert pointer.position == 10


def test_pointer_ref() -> None:
    START_POS: Final[int] = 3
    REF_ONE_POS: Final[int] = 1
    REF_TWO_POS: Final[int] = 5

    layout = BFMemoryLayout({1: REF_ONE_POS, 2: REF_TWO_POS})
    pointer = BFPointer(layout, start_position=START_POS)
    assert pointer.position == START_POS

    code = pointer.move_by_ref(2)
    assert code == (BFCommands.MOVE_RIGHT if START_POS < REF_TWO_POS else BFCommands.MOVE_LEFT) * abs(
        START_POS - REF_TWO_POS
    )
    assert pointer.position == REF_TWO_POS
