__all__ = ("UnitProgram",)


from quix.core.interfaces import Program

from .base import UnitOpcode
from .unit import Unit

type Value = int
type UnitProgram = Program[UnitOpcode]
type Wide = list[Unit]
type Literal = Unit | Value
type WideLiteral = list[Literal]
type Anchor = Unit
type IOValue = Wide | str
