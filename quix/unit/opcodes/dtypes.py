__all__ = ("UnitProgram",)

from collections.abc import Hashable

from quix.core.interfaces import Program

from .base import UnitOpcode

type Unit = Hashable
type Value = int
type UnitProgram = Program[UnitOpcode]
type Wide = list[Unit]
type Literal = Unit | Value
type WideLiteral = list[Literal]
type Anchor = Unit
type IOValue = Wide | str
