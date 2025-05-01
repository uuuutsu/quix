from typing import override

from quix.memoptix.scheduler.blueprint import Blueprint
from quix.memoptix.scheduler.constraints import Array, Index, LifeCycle
from quix.memoptix.scheduler.layout import Layout
from quix.memoptix.scheduler.owner import Owner
from quix.tools import intervals_intersects

from .base import Resolver


def _extract_constraint_info(
    blueprint: Blueprint,
) -> tuple[
    dict[Owner, int],
    dict[Owner, tuple[int, int]],
    dict[Owner, int],
]:
    indexes: dict[Owner, int] = {}
    life_cycles: dict[Owner, tuple[int, int]] = {}
    arrays: dict[Owner, int] = {}

    for owner, constr in blueprint.iter_constr():
        match constr:
            case Index():
                indexes[owner] = constr.index
            case LifeCycle():
                life_cycles[owner] = constr.start, constr.end
            case Array():
                arrays[owner] = constr.length
            case _:
                raise RuntimeError(f"Unknown constraint: {constr}")

    return indexes, life_cycles, arrays


def _order_ascend(life_cycles: dict[Owner, tuple[int, int]]) -> list[Owner]:
    return [p[0] for p in sorted(life_cycles.items(), key=lambda p: p[1][0])]


def _get_all_affected_owners(
    owner: Owner,
    mapping: dict[Owner, int],
    anchor: int,
    arrays: dict[Owner, int],
) -> set[Owner]:
    owners: set[Owner] = set()

    for idx in range(
        anchor,
        anchor + arrays.get(owner, 0) + 1,
    ):
        for existing_owner, existing_idx in mapping.items():
            left, right = existing_idx, existing_idx + arrays.get(existing_owner, 1)
            if left <= idx < right:
                owners.add(existing_owner)

    return owners


class PrimitiveResolver(Resolver):
    __slots__ = ()

    __domain__ = {Index, LifeCycle, Array}

    @override
    def __call__(self, blueprint: Blueprint) -> Layout:
        indexes, life_cycles, arrays = _extract_constraint_info(blueprint)
        ordered_owners = _order_ascend(life_cycles)

        mapping: dict[Owner, int] = {}
        for owner, index in indexes.items():
            mapping[owner] = index

        for owner in ordered_owners:
            if owner in mapping:
                continue

            index = 0
            while True:
                curr_owners = _get_all_affected_owners(owner, mapping, index, arrays)
                for curr_owner in curr_owners:
                    if curr_owner not in life_cycles:
                        continue
                    elif not intervals_intersects(life_cycles[curr_owner], life_cycles[owner]):
                        continue
                    break
                else:
                    mapping[owner] = index
                    break
                index += 1

        for owner in blueprint.get_owners().difference(mapping):
            mapping[owner] = 0

        return Layout(blueprint, mapping)
