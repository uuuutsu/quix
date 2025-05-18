from dataclasses import dataclass
from io import StringIO

from quix.core.compiler.layout import BFMemoryLayout
from quix.core.compiler.pointer import BFPointer
from quix.core.compiler.visitor import BFVisitor
from quix.core.interfaces.writable import Writable

from .base import Stage
from .mem_compile import Blueprint


@dataclass(slots=True)
class BFGenerator(Stage[Blueprint, BFVisitor]):
    dest: Writable | None = None

    def _execute(self, data: Blueprint) -> BFVisitor:
        dest = self.dest or StringIO()
        ptr = BFPointer(BFMemoryLayout(data["mapping"]))
        return BFVisitor(dest, ptr).visit(data["program"])
