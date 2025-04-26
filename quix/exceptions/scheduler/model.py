from quix.memoptix.scheduler.owner import Owner

from .base import SchedulerException


class IndexIsNotYetResolvedError(SchedulerException):
    def __init__(self, owner: Owner) -> None:
        super().__init__(f"Index of {owner} has not yet been resolved by the model.")


class UnknownOwnerException(SchedulerException):
    def __init__(self, owner: Owner) -> None:
        super().__init__(f"Owner {owner} has not yet been registered in the model.")
