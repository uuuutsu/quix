from quix.scheduler.blueprint import Blueprint
from quix.scheduler.constraints import Index, LifeCycle, Reserve
from quix.scheduler.layout import Layout
from quix.scheduler.owner import Owner

from .base import Resolver


def _extract_constraint_info(
    blueprint: Blueprint,
) -> tuple[
    dict[Owner, int],
    dict[Owner, tuple[int, int]],
    dict[Owner, tuple[int, int]],
]:
    indexes: dict[Owner, int] = {}
    life_cycles: dict[Owner, tuple[int, int]] = {}
    reserved: dict[Owner, tuple[int, int]] = {}

    for owner, constraints in blueprint.owner_to_constraints():
        for constraint in constraints:
            match constraint:
                case Index():
                    indexes[owner] = constraint.index
                case LifeCycle():
                    life_cycles[owner] = constraint.start, constraint.end
                case Reserve():
                    reserved[owner] = constraint.left, constraint.right

    return indexes, life_cycles, reserved


def _order_ascend(life_cycles: dict[Owner, tuple[int, int]]) -> list[Owner]:
    return [p[0] for p in sorted(life_cycles.items(), key=lambda p: p[1][0])]


def _intervals_intersects(int1: tuple[int, int], int2: tuple[int, int]) -> bool:
    """
    Determine if two intervals intersects.

    :param int1: The first interval as a tuple of two integers.
    :param int2: The second interval as a tuple of two integers.
    :return: True if the intervals overlap, False otherwise.
    """
    return max(int1[1], int2[1]) - min(int1[0], int2[0]) < (int1[1] - int1[0]) + (int2[1] - int2[0]) or (
        (int1[0] <= int2[0]) and (int1[1] >= int2[1])
    )


def _get_all_affected_owners(
    owner: Owner,
    layout: Layout,
    anchor: int,
    reserved: dict[Owner, tuple[int, int]],
) -> set[Owner]:
    owners: set[Owner] = set()

    left, right = reserved.get(owner, (0, 0))
    for idx in range(anchor - left, anchor + right + 1):
        for existing_owner, existing_idx in layout.items():
            left_off, right_off = reserved.get(existing_owner, (0, 0))
            left, right = existing_idx - left_off, existing_idx + right_off
            if left <= idx <= right:
                owners.add(existing_owner)

    return owners


class PrimitiveResolver(Resolver):
    __slots__ = ()

    __signature__ = {Index, LifeCycle, Reserve}

    def __call__(self, blueprint: Blueprint) -> Layout:
        indexes, life_cycles, reserved = _extract_constraint_info(blueprint)
        ordered_owners = _order_ascend(life_cycles)

        layout = Layout(len(indexes) > 0)
        for owner, index in indexes.items():
            layout[owner] = index

        for owner in ordered_owners:
            if owner in layout:
                continue

            start_idx = reserved.get(owner, (0, 0))[0]
            while True:
                curr_owners = _get_all_affected_owners(
                    owner,
                    layout,
                    start_idx,
                    reserved,
                )
                for curr_owner in curr_owners:
                    if curr_owner not in life_cycles:
                        continue
                    elif not _intervals_intersects(life_cycles[curr_owner], life_cycles[owner]):
                        continue
                    break
                else:
                    layout[owner] = start_idx
                    break
                start_idx += 1
                continue

        return layout
