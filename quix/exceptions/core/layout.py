from quix.core.opcodes.dtypes import Ref

from .base import CoreException


class LayoutException(CoreException): ...


class RefNotFound(LayoutException):
    def __init__(self, ref: Ref) -> None:
        super().__init__(f"No entry found for reference: {ref}")
