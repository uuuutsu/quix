__all__ = (
    "Ref",
    "Value",
    "CoreProgram",
)
from quix.core.interfaces import Program

from .base import CoreOpcode

type Ref = int
type Value = int
type Code = str
type CoreProgram = Program[CoreOpcode]
