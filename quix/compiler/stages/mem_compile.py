from dataclasses import dataclass
from typing import TypedDict

from quix.core.opcodes.dtypes import CoreProgram, Ref
from quix.memoptix.compile import mem_compile

from .base import Stage


class Blueprint(TypedDict):
    program: CoreProgram
    mapping: dict[Ref, int]


@dataclass(slots=True)
class MemCompile(Stage[CoreProgram, Blueprint]):
    gc: bool = False

    def _execute(self, __data: CoreProgram) -> Blueprint:
        program, mapping = mem_compile(__data, garbage_collector=self.gc)
        return Blueprint(program=program, mapping=mapping)
