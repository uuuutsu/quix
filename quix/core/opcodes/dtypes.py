__all__ = (
    "Ref",
    "Value",
    "CoreProgram",
)
from collections.abc import Hashable

from quix.core.interfaces import Program

from .base import CoreOpcode

type Ref = Hashable
type Value = int
type Code = str
type CoreProgram = Program[CoreOpcode]
