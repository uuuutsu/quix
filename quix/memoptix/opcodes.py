from enum import StrEnum

from quix.core.opcodes.base import opcode
from quix.core.opcodes.dtypes import Ref


@opcode
def array(ref: Ref, length: int) -> None: ...


@opcode
def hard_link(ref: Ref, to_: Ref, distance: int) -> None: ...


@opcode
def index(ref: Ref, index: int) -> None: ...


@opcode
def soft_link(ref: Ref, to_: dict[Ref, int]) -> None: ...


@opcode
def free(ref: Ref) -> None: ...


class MemoptixOpcodes(StrEnum):
    ARRAY = "array"
    HARD_LINK = "hard_link"
    INDEX = "index"
    SOFT_LINK = "soft_link"
    FREE = "free"
