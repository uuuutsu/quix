__all__ = (
    "CoreOpcode",
    "add",
    "input",
    "output",
    "loop",
    "inject",
)

from .base import CoreOpcode
from .opcodes import add, inject, input, loop, output
