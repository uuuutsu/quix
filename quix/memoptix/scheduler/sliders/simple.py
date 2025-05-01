from quix.memoptix.scheduler.constraints import Array, HardLink, Index, LifeCycle, SoftLink
from quix.memoptix.scheduler.layout import Layout
from quix.memoptix.scheduler.owner import Owner
from quix.memoptix.scheduler.utils import get_constraint_mappers
from quix.tools import intervals_intersects

from .base import Slider


def _get_intersected_owners_between_sets(
    left_lifecycles: dict[Owner, list[LifeCycle]],
    right_lifecycles: dict[Owner, list[LifeCycle]],
) -> list[tuple[Owner, Owner]]:
    left_cycles: dict[Owner, tuple[int, int]] = {}
    right_cycles: dict[Owner, tuple[int, int]] = {}

    for owner, (constr, *_) in left_lifecycles.items():
        if len(_) > 0:
            raise ValueError(f"At most one `{LifeCycle}` constraint is allowed for each owner.")
        left_cycles[owner] = (constr.start, constr.end)

    for owner, (constr, *_) in right_lifecycles.items():
        if len(_) > 0:
            raise ValueError(f"At most one `{LifeCycle}` constraint is allowed for each owner.")
        right_cycles[owner] = (constr.start, constr.end)

    inter_pairs = []
    for owner_left, cycle_left in left_cycles.items():
        for owner_right, cycle_right in right_cycles.items():
            if not intervals_intersects(cycle_left, cycle_right):
                continue

            inter_pairs.append((owner_left, owner_right))
    return inter_pairs


def _simplify_array_constrs(arrays: dict[Owner, list[Array]]) -> dict[Owner, int]:
    new_arrays: dict[Owner, int] = {}
    for owner, (constr, *_) in arrays.items():
        if len(_) > 0:
            raise ValueError(f"At most one `{Array}` constraint is allowed for each owner.")
        new_arrays[owner] = constr.length
    return new_arrays


def _mappings_intersect(
    left: dict[Owner, int],
    right: dict[Owner, int],
    inter_pairs: list[tuple[Owner, Owner]],
    left_arrays: dict[Owner, int],
    right_arrays: dict[Owner, int],
) -> int:
    for left_owner, right_owner in inter_pairs:
        left_index = left[left_owner]
        right_index = right[right_owner]

        if intervals_intersects(
            (left_index, left_index + left_arrays.get(left_owner, 1)),
            (right_index, right_index + right_arrays.get(right_owner, 1)),
        ):
            return left_index + left_arrays.get(left_owner, 1) - right_index

    return 0


def _slide_mapping(mapping: dict[Owner, int], offset: int) -> dict[Owner, int]:
    return {owner: index + offset for owner, index in mapping.items()}


class SimpleSlider(Slider):
    __slots__ = ()

    __domain__ = {Index, SoftLink, HardLink, Array, LifeCycle}

    def __call__(self, left: Layout, right: Layout) -> Layout:
        if left.blueprint.get_owners().intersection(right.blueprint.get_owners()):
            raise RuntimeError("Blueprints can't reference same owner.")

        left_constrs = get_constraint_mappers(left.blueprint)
        right_constrs = get_constraint_mappers(right.blueprint)
        if not left_constrs.get(Index, {}):
            left_constrs, right_constrs = right_constrs, left_constrs
            left, right = right, left

        left_arrays = _simplify_array_constrs(left_constrs.get(Array, {}))  # type: ignore
        right_arrays = _simplify_array_constrs(right_constrs.get(Array, {}))  # type: ignore
        pos_inters = _get_intersected_owners_between_sets(
            left_constrs.get(LifeCycle, {}),  # type: ignore
            right_constrs.get(LifeCycle, {}),  # type: ignore
        )

        root_mapping = left.mapping()
        sliding_mapping = right.mapping()

        if right_constrs.get(Index, {}) and left_constrs.get(Index, {}):
            if _mappings_intersect(root_mapping, sliding_mapping, pos_inters, left_arrays, right_arrays) != 0:
                raise RuntimeError(
                    f"Layouts {left} and {right} cannot be combined due to coliding lifecycles on enforced indexes."
                )
            return Layout(left.blueprint.combine(right.blueprint), root_mapping | sliding_mapping)

        offset: int = 0
        while True:
            sliding_mapping = _slide_mapping(sliding_mapping, offset)
            new_offset = _mappings_intersect(root_mapping, sliding_mapping, pos_inters, left_arrays, right_arrays)
            if new_offset != 0:
                offset += new_offset
                continue
            return Layout(left.blueprint.combine(right.blueprint), root_mapping | sliding_mapping)
