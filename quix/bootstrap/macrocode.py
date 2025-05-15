import inspect
from collections.abc import Callable
from functools import wraps
from typing import ClassVar, cast

from quix.bootstrap.program import ToConvert
from quix.core.interfaces.opcode import OpcodeFactory
from quix.core.opcodes.base import CoreOpcode
from quix.tools.case import snake_case_to_pascal_case


class MacroCode(CoreOpcode):
    __slots__ = ()

    _handler: ClassVar[Callable[..., ToConvert]]

    def __call__(self) -> ToConvert:
        return type(self)._handler(**self.args())


def macrocode[**P](func: Callable[P, ToConvert]) -> OpcodeFactory[P, MacroCode]:
    new_opcode_cls = type(
        snake_case_to_pascal_case(func.__name__),
        (MacroCode,),
        {"__id__": func.__name__, "_handler": func},
    )
    signature = inspect.signature(func)

    @wraps(func)
    def create(*args: P.args, **kwargs: P.kwargs) -> MacroCode:
        binded_signature = signature.bind(*args, **kwargs)
        binded_signature.apply_defaults()
        return cast(MacroCode, new_opcode_cls(binded_signature.arguments))

    return cast(OpcodeFactory[P, MacroCode], create)
