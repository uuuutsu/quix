import inspect
from collections.abc import Callable
from functools import wraps
from typing import Any, ClassVar, cast, override

from rich.repr import Result, rich_repr

from quix.core.interfaces import Opcode, OpcodeFactory
from quix.tools import FlyweightMeta, pascal_case_to_snake_case, snake_case_to_pascal_case


@rich_repr
class UnitOpcode(Opcode, metaclass=FlyweightMeta):
    __slots__ = ("_args",)

    __id__: ClassVar[str]

    def __init_subclass__(cls) -> None:
        if not hasattr(cls, "__id__"):
            cls.__id__ = pascal_case_to_snake_case(cls.__name__)

    def __init__(self, args: dict[str, Any]) -> None:
        self._args = args

    def __eq__(self, value: object) -> bool:
        if isinstance(value, UnitOpcode):
            return (self.__id__ == value.__id__) and (self._args == value._args)
        return super().__eq__(value)

    def __hash__(self) -> int:
        return id(self)

    @override
    def args(self) -> dict[str, Any]:
        return self._args

    def __rich_repr__(self) -> Result:
        yield from self._args.items()


def opcode[**P](func: Callable[P, None]) -> OpcodeFactory[P, UnitOpcode]:
    new_opcode_cls = type(
        snake_case_to_pascal_case(func.__name__),
        (UnitOpcode,),
        {"__id__": func.__name__},
    )
    signature = inspect.signature(func)

    @wraps(func)
    def create(*args: P.args, **kwargs: P.kwargs) -> Opcode:
        func(*args, **kwargs)
        binded_signature = signature.bind(*args, **kwargs)
        binded_signature.apply_defaults()
        return cast(Opcode, new_opcode_cls(binded_signature.arguments))

    return cast(OpcodeFactory[P, UnitOpcode], create)
