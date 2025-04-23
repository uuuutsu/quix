__all__ = ("UnitProgram",)
from quix.core.interfaces import Program

from .base import UnitOpcode

type UnitProgram = Program[UnitOpcode]
