from collections.abc import Iterable

import numpy as np


class Memory:
    __slots__ = "_memory"

    def __init__(self) -> None:
        self._memory: dict[int, int] = {}

    def __setitem__(self, key: int, value: Iterable[int]) -> None:
        for i, byte in enumerate(value):
            self._memory[i + np.uint32(key)] = byte  # type: ignore

    def __getitem__(self, item: int) -> int:
        return self._memory.get(np.uint32(item), 0)  # type: ignore
