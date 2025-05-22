import inspect
from collections.abc import Callable
from functools import wraps
from typing import ClassVar, cast

from quix.bootstrap.program import ToConvert, to_program
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


def from_program(*program: ToConvert) -> MacroCode:
    def _my_code() -> ToConvert:
        return to_program(program)

    _my_code.__name__ = build_name()
    return macrocode(_my_code)()


def build_name() -> str:
    if not (curr_frame := inspect.currentframe()):
        raise ValueError("Cannot identify calling frame to construct branch name")
    elif not (prev_frame := curr_frame.f_back):
        raise ValueError("Cannot identify calling frame to construct branch name")
    elif not (caller_frame := prev_frame.f_back):
        raise ValueError("Cannot identify calling frame to construct branch name")

    module = inspect.getmodule(caller_frame)
    line_no = caller_frame.f_lineno
    func_name = caller_frame.f_code.co_name

    return f"{module}:{func_name}:{line_no}"
