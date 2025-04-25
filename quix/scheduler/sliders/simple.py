from quix.scheduler.constraints import Array, HardLink, Index, LifeCycle, SoftLink
from quix.scheduler.layout import Layout

from .base import Slider


class SimpleSlider(Slider):
    __slots__ = ()

    __domain__ = {Index, SoftLink, HardLink, Array, LifeCycle}

    def __call__(self, left: Layout, right: Layout) -> Layout:
        return left
