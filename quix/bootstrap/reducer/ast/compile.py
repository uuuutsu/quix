from quix.bootstrap.program import SmartProgram
from quix.core.opcodes.dtypes import CoreProgram

from .node import Node


def compile(ast: Node) -> CoreProgram:
    program = SmartProgram()
    for node in ast.body:
        if isinstance(node, Node):
            program |= compile(node)
        else:
            program |= node
    return program
