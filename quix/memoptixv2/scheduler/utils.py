import math
from collections.abc import Callable

from quix.memoptixv2.scheduler.tree import Domain

type Matcher = Callable[[Domain, list[Domain]], int | None]


def inclusion_matcher(to_match: Domain, registry: list[Domain]) -> int | None:
    curr_match: int | None = None
    curr_length: float = math.inf

    for idx, domain in enumerate(registry):
        if to_match - domain:
            continue
        if len(domain) < curr_length:
            curr_length = len(domain)
            curr_match = idx

    if curr_match is not None:
        return curr_match

    return None
