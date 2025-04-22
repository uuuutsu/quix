import inspect
from collections.abc import Callable
from functools import wraps
from typing import Any, ClassVar, cast, override

from rich.repr import Result, rich_repr

from quix.core.interfaces import Opcode, OpcodeFactory
from quix.tools import pascal_case_to_snake_case, snake_case_to_pascal_case


@rich_repr
class CoreOpcode(Opcode):
    __slots__ = ("_args",)

    __id__: ClassVar[str]

    def __init_subclass__(cls) -> None:
        if not hasattr(cls, "__id__"):
            cls.__id__ = pascal_case_to_snake_case(cls.__name__)

    def __init__(self, args: dict[str, Any]) -> None:
        self._args = args

    @override
    def args(self) -> dict[str, Any]:
        return self._args

    def __rich_repr__(self) -> Result:
        yield from self._args.items()


def opcode[**P](func: Callable[P, None]) -> OpcodeFactory[P, CoreOpcode]:
    new_opcode_cls = type(
        snake_case_to_pascal_case(func.__name__),
        (CoreOpcode,),
        {"__id__": func.__name__},
    )
    signature = inspect.signature(func)

    @wraps(func)
    def create(*args: P.args, **kwargs: P.kwargs) -> Opcode:
        func(*args, **kwargs)
        return cast(Opcode, new_opcode_cls(signature.bind(*args, **kwargs).arguments))

    return cast(OpcodeFactory[P, CoreOpcode], create)
