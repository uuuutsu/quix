import math
from collections.abc import Callable

from quix.memoptix.scheduler.constraints import BaseConstraint
from quix.memoptix.scheduler.layout import Layout

from .base import Slider
from .simple import SimpleSlider

type Domain = set[type[BaseConstraint]]
type Matcher = Callable[[Domain, list[Domain]], int | None]


def _inclusion_matcher(to_match: Domain, registry: list[Domain]) -> int | None:
    curr_match: int | None = None
    curr_length: float = math.inf

    for idx, domain in enumerate(registry):
        if domain.difference(to_match):
            continue
        if len(domain) < curr_length:
            curr_length = len(domain)
            curr_match = idx

    if curr_match:
        return curr_match

    return None


class SliderRegistry:
    __slots__ = (
        "_matcher",
        "_sliders",
    )

    def __init__(self, matcher: Matcher = _inclusion_matcher) -> None:
        self._matcher = matcher
        self._sliders: list[Slider] = []

    def __call__(self, left: Layout, right: Layout) -> Layout:
        domains = [slider.__domain__ for slider in self._sliders]
        match = self._matcher(left.blueprint.domain | right.blueprint.domain, domains)

        if match is None:
            raise RuntimeError(f"No slider found to handle: {left} + {right}")

        return self._sliders[match](left, right)

    def register(self, slider: Slider) -> None:
        self._sliders.append(slider)


def create_slider_registry() -> SliderRegistry:
    registry = SliderRegistry()
    registry.register(SimpleSlider())
    return registry
