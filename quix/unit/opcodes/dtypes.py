__all__ = ("UnitProgram",)

from quix.core.interfaces import Program
from quix.core.opcodes.dtypes import Ref

from .base import UnitOpcode


class Unit:
    __slots__ = ("_ref",)

    def __init__(self, ref: Ref) -> None:
        self._ref = ref


type Value = int
type UnitProgram = Program[UnitOpcode]
type Wide = list[Unit]
type Literal = Unit | Value
type WideLiteral = list[Literal]
type Anchor = Unit
type IOValue = Wide | str
