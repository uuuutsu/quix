from quix.bootstrap.macrocode import MacroCode
from quix.bootstrap.program import ToConvert, to_program
from quix.core.opcodes.base import CoreOpcode

from .node import Node


def build_ast(code: ToConvert) -> Node:
    root = Node(None, [])
    child: Node | CoreOpcode
    for opcode in to_program(code):
        if isinstance(opcode, MacroCode):
            child = Node(opcode, build_ast(opcode()).body)
        else:
            child = opcode
        root.body.append(child)

    return root
