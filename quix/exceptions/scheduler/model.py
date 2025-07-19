from __future__ import annotations

from typing import TYPE_CHECKING

from .base import SchedulerException

if TYPE_CHECKING:
    from quix.memoptix.scheduler.owner import Owner
    from quix.memoptixv2.scheduler.tree.node import Node


class IndexIsNotYetResolvedError(SchedulerException):
    def __init__(self, owner: Owner) -> None:
        super().__init__(f"Index of {owner} has not yet been resolved by the model.")


class UnknownOwnerException(SchedulerException):
    def __init__(self, owner: Owner) -> None:
        super().__init__(f"Owner {owner} has not yet been registered in the model.")


class UnknownNodeException(SchedulerException):
    def __init__(self, node: Node) -> None:
        super().__init__(f"Node {node} has not yet been registered in the model.")


class NodeIndexIsNotYetResolvedError(SchedulerException):
    def __init__(self, node: Node) -> None:
        super().__init__(f"Index of {node} has not yet been resolved by the model.")
