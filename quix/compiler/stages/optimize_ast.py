from quix.bootstrap.ast.node import Node
from quix.bootstrap.optimizer import optimize

from .base import Stage


class OptimizeAST(Stage[Node, Node]):
    __slots__ = ()

    def _execute(self, __data: Node) -> Node:
        return optimize(__data)
