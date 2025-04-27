from collections.abc import Hashable
from io import StringIO

from quix.core.opcodes.dtypes import CoreProgram
from quix.core.visitor.bf.layout import BFMemoryLayout
from quix.core.visitor.bf.pointer import BFPointer
from quix.core.visitor.bf.visitor import BFVisitor


def compile_to_bf(program: CoreProgram, mapping: dict[Hashable, int]) -> str:
    layout = BFMemoryLayout(mapping)
    pointer = BFPointer(layout)
    buff = StringIO()
    BFVisitor(buff, pointer).visit(program)
    return buff.getvalue()
