from dataclasses import dataclass
from typing import TypedDict

from quix.bootstrap.program import ToConvert, to_program
from quix.core.opcodes.dtypes import CoreProgram, Ref
from quix.memoptix.schedule import schedule

from .base import Stage


class Blueprint(TypedDict):
    program: CoreProgram
    mapping: dict[Ref, int]


@dataclass(slots=True)
class Scheduler(Stage[ToConvert, Blueprint]):
    gc: bool = True

    def _execute(self, __data: ToConvert) -> Blueprint:
        program, mapping = schedule(to_program(__data), garbage_collector=self.gc)
        return Blueprint(program=program, mapping=mapping)
