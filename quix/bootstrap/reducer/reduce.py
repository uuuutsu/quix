from quix.bootstrap.program import ToConvert
from quix.core.opcodes.dtypes import CoreProgram

from .ast import Node, build_ast, compile


def reduce(code: ToConvert) -> CoreProgram:
    ast = build_ast(code)
    ast = _optimize(ast)
    return compile(ast)


def _optimize(ast: Node) -> Node:
    return ast
