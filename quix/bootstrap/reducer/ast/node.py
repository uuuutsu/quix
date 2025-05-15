from __future__ import annotations

from quix.core.opcodes.base import CoreOpcode


class Node:
    __slots__ = "body", "opcode"

    def __init__(self, opcode: CoreOpcode | None, body: list[Node | CoreOpcode]) -> None:
        self.body = body
        self.opcode = opcode
