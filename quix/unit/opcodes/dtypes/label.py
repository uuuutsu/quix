from collections.abc import Iterable

from quix.core.opcodes.base import CoreOpcode
from quix.core.opcodes.dtypes import CoreProgram

from .base import DType, dtype


@dtype
class Label(DType):
    program: CoreProgram

    def __iter__(self) -> Iterable[CoreOpcode]:
        return self.program
