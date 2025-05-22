import inspect
from collections.abc import Callable
from functools import wraps
from typing import ClassVar, cast, overload

from quix.bootstrap.program import ToConvert, to_program
from quix.core.interfaces.opcode import OpcodeFactory
from quix.core.opcodes.base import CoreOpcode
from quix.tools.case import snake_case_to_pascal_case
from quix.tools.unique import generate_unique_id


class MacroCode(CoreOpcode):
    __slots__ = ()

    _handler: ClassVar[Callable[..., ToConvert]]

    def __call__(self) -> ToConvert:
        return type(self)._handler(**self.args())


@overload
def macrocode[**P](func: Callable[P, ToConvert]) -> OpcodeFactory[P, MacroCode]: ...
@overload
def macrocode(func: ToConvert, *other: ToConvert) -> MacroCode: ...
@overload
def macrocode(func: ToConvert, *other: ToConvert, name: str) -> MacroCode: ...
def macrocode[**P](
    func: Callable[P, ToConvert] | ToConvert,
    *other: ToConvert,
    name: str | None = None,
) -> OpcodeFactory[P, MacroCode] | MacroCode:
    if (not callable(func)) or isinstance(func, MacroCode):
        name = name or build_name()

        def factory() -> ToConvert:
            return to_program(func, *other)
    else:
        if other:
            raise RuntimeError(f"Trying to cast unsupported set of arguments: {func} and {other} to macrocode.")

        name = func.__name__
        factory = func

    new_opcode_cls = type(
        snake_case_to_pascal_case(name),
        (MacroCode,),
        {"__id__": name, "_handler": factory},
    )

    if (not callable(func)) or isinstance(func, MacroCode):
        return cast(MacroCode, new_opcode_cls({}))

    signature = inspect.signature(factory)

    @wraps(factory)
    def create(*args: P.args, **kwargs: P.kwargs) -> MacroCode:
        binded_signature = signature.bind(*args, **kwargs)
        binded_signature.apply_defaults()
        return cast(MacroCode, new_opcode_cls(binded_signature.arguments))

    return cast(OpcodeFactory[P, MacroCode], create)


def build_name() -> str:
    if not (curr_frame := inspect.currentframe()):
        raise ValueError("Cannot identify calling frame to construct branch name")
    elif not (prev_frame := curr_frame.f_back):
        raise ValueError("Cannot identify calling frame to construct branch name")
    elif not (caller_frame := prev_frame.f_back):
        raise ValueError("Cannot identify calling frame to construct branch name")

    module = inspect.getmodule(caller_frame)
    module_name = module.__name__ if module else "<unknown>"
    line_no = caller_frame.f_lineno
    func_name = caller_frame.f_code.co_name

    # Unlike for a function macrocode we cannot guarantee that a dynamically generated one is pure.
    # Meaning every macrocode generated that way is unique to the context it captured.
    # That's why we create a unique identifier even for the "same" dynamic macrocode.
    unique_id = generate_unique_id()

    return f"{module_name}:{func_name}:{line_no}:{unique_id}"
