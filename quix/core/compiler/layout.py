from typing import Self

from quix.core.opcodes import Ref
from quix.exceptions.core import RefNotFound

from .types import Ptr


class BFMemoryLayout(dict[Ref, Ptr]):
    def __getitem__(self, key: Ref) -> Ptr:
        try:
            return super().__getitem__(key)
        except KeyError as exc:
            raise RefNotFound(key) from exc

    @classmethod
    def default(cls) -> Self:
        return cls()
