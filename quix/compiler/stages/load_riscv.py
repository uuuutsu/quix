from io import BytesIO

from quix.riscv.loader.loader import ELFLoader
from quix.riscv.loader.state import State

from .base import Stage


class LoadRISCV(Stage[BytesIO, State]):
    __slots__ = ()

    def _execute(self, __data: BytesIO) -> State:
        return ELFLoader().load(__data)
