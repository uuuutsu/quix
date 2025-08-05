from __future__ import annotations

from typing import TYPE_CHECKING, Self, overload

from rich.repr import Result, rich_repr

from quix.core.opcodes.dtypes import Ref
from quix.tools.unique import generate_unique_id

if TYPE_CHECKING:
    from quix.memoptix.scheduler.tree.constraints import BaseConstraint


@rich_repr
class Node:
    __slots__ = (
        "name",
        "ref",
        "constraints",
        "lifecycle",
    )

    def __init__(
        self,
        lifecycle: tuple[int, int],
        name: str | None = None,
        *,
        ref: Ref | None = None,
        constraints: list[BaseConstraint] | None = None,
    ) -> None:
        self.name = name
        self.ref = ref or generate_unique_id()
        self.constraints: list[BaseConstraint] = constraints or []
        self.lifecycle = lifecycle

    def add_constraint(self, constraint: BaseConstraint) -> Self:
        for node in constraint.get_nodes():
            if node is self:
                raise RuntimeError(f"Self reference detected: {constraint}")

        self.constraints.append(constraint)
        return self

    def __hash__(self) -> int:
        return hash(self.ref)

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Node):
            return False
        return self.ref == value.ref

    def __repr__(self) -> str:
        return f"Node( {self.name or self.ref} )"

    def __rich_repr__(self) -> Result:
        yield "name", self.name
        yield "ref", self.ref
        yield "lifecycle", self.lifecycle
        yield "constraints", self.constraints


@overload
def create_node(lifecycle: tuple[int, int], name: str | None) -> Node: ...
@overload
def create_node(lifecycle: tuple[int, int], name: str | None, ref: Ref) -> Node: ...
def create_node(lifecycle: tuple[int, int], name: str | None = None, ref: Ref | None = None) -> Node:
    if ref is None:
        ref = generate_unique_id()
    return Node(lifecycle=lifecycle, ref=ref, name=name)
