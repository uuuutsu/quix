from collections.abc import Iterable


def find_optimal_usage_scope(scope_estimate: tuple[int, int], loops: Iterable[tuple[int, int]]) -> tuple[int, int]:
    """
    Resizes a rough-usage estimation to ensure its safety for merging with other usage intervals.
    This adjustment is done to ensure that when a memory unit is re-used, older data is not needed.

    :param scope_estimate: The initial rough estimate of the memory usage interval.
    :param loops: A list of loop intervals to consider for adjustment.
    :return: An adjusted interval that avoids unnecessary overlap with loop intervals.
    """

    def overlap(a: tuple[int, int], b: tuple[int, int]) -> bool:
        return a[0] <= b[1] and b[0] <= a[1]

    def within(a: tuple[int, int], b: tuple[int, int]) -> bool:
        return b[0] <= a[0] and a[1] <= b[1]

    def adjust_interval(candidate: tuple[int, int], other: tuple[int, int]) -> tuple[int, int]:
        if within(candidate, other) or within(other, candidate):
            return candidate
        else:
            start = min(candidate[0], other[0])
            end = max(candidate[1], other[1])
            return start, end

    loops = sorted(loops, key=lambda x: x[0])
    for loop in loops:
        if overlap(scope_estimate, loop) and not within(scope_estimate, loop) and not within(loop, scope_estimate):
            scope_estimate = adjust_interval(scope_estimate, loop)

    return scope_estimate
