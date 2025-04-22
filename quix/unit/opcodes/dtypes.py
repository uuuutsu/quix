__all__ = ("Program",)
from quix.core.interfaces import Program as _Program

from .base import UnitOpcode

type Program = _Program[UnitOpcode]
