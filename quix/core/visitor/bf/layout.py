from typing import Self

from quix.core.opcodes import Ref

from .types import Ptr


class BFMemoryLayout(dict[Ref, Ptr]):
    @classmethod
    def default(cls) -> Self:
        return cls()
