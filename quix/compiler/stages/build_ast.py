from quix.bootstrap.ast.build import build_ast
from quix.bootstrap.ast.node import Node
from quix.bootstrap.program import ToConvert

from .base import Stage


class BuildAST(Stage[ToConvert, Node]):
    __slots__ = ()

    def _execute(self, __data: ToConvert) -> Node:
        return build_ast(__data)
