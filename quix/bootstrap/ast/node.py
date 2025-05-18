from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from rich.repr import rich_repr

from quix.core.opcodes.base import CoreOpcode


@rich_repr
class Node:
    __slots__ = "body", "opcode"

    def __init__(self, opcode: CoreOpcode | None, body: list[Node | CoreOpcode]) -> None:
        self.body = body
        self.opcode = opcode

    def __rich_repr__(self) -> Iterable[Any]:
        yield "opcode", self.opcode
        yield "body", self.body
