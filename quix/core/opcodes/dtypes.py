__all__ = (
    "Ref",
    "Value",
    "Program",
)
from quix.core.interfaces import Program as _Program
from quix.core.opcodes.base import CoreOpcode

type Ref = int
type Value = int
type Code = str
type Program = _Program[CoreOpcode]
