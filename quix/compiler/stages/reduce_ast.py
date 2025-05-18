from quix.bootstrap.ast import reduce
from quix.bootstrap.ast.node import Node
from quix.core.opcodes.dtypes import CoreProgram

from .base import Stage


class ReduceAST(Stage[Node, CoreProgram]):
    __slots__ = ()

    def _execute(self, __data: Node) -> CoreProgram:
        return reduce(__data)
