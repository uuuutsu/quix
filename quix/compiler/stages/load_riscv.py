from io import BytesIO
from pathlib import Path

from quix.riscv.loader.loader import ELFLoader
from quix.riscv.loader.state import State

from .base import Stage


class LoadRISCV(Stage[Path, State]):
    __slots__ = ()

    def _execute(self, __data: Path) -> State:
        with open(__data, "rb") as file:
            return ELFLoader().load(BytesIO(file.read()))
