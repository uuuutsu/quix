from __future__ import annotations

from abc import abstractmethod
from collections.abc import Hashable
from typing import TYPE_CHECKING, Any, Protocol, _ProtocolMeta, final


class FlyweightStateType(Protocol):
    @abstractmethod
    def __call__(*__args: Any, **__kwargs: Any) -> Hashable:
        raise NotImplementedError


def _dummy_factory(*args: Any, **kwargs: Any) -> str:
    return f"{args}_{kwargs}"


@final
class FlyweightMeta(_ProtocolMeta):
    __flyweights__: dict[Hashable, FlyweightMeta]
    __state_factory__: FlyweightStateType

    def __init__(
        cls: FlyweightMeta,
        name: str,
        bases: tuple[type[Any], ...],
        classdict: dict[str, Any],
        state_factory: FlyweightStateType = _dummy_factory,
        **kwargs: Any,
    ) -> None:
        super().__init__(name, bases, classdict, **kwargs)
        cls.__flyweights__ = {}
        cls.__state_factory__ = state_factory

    if not TYPE_CHECKING:

        def __call__(cls: FlyweightMeta, *args: Any, **kwargs: Any) -> FlyweightMeta:
            state = cls.__state_factory__(*args, **kwargs)
            if state in cls.__flyweights__:
                return cls.__flyweights__[state]
            return cls.__flyweights__.setdefault(state, super().__call__(*args, **kwargs))
