from __future__ import annotations

from typing import TYPE_CHECKING

from .base import SchedulerException

if TYPE_CHECKING:
    from quix.memoptix.scheduler.tree.node import Node


class UnknownNodeException(SchedulerException):
    def __init__(self, node: Node) -> None:
        super().__init__(f"Node {node} has not yet been registered in the model.")


class NodeIndexIsNotYetResolvedError(SchedulerException):
    def __init__(self, node: Node) -> None:
        super().__init__(f"Index of {node} has not yet been resolved by the model.")
