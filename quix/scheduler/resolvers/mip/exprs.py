from collections.abc import Callable

import mip  # type: ignore

from quix.scheduler.constraints import Index, LifeCycle
from quix.scheduler.constraints.base import BaseConstraint
from quix.scheduler.owner import Owner

from .model import Model
from .utils import intervals_intersects


def expr_index(owner2constr: dict[Owner, Index], model: Model) -> None:
    for owner, constr in owner2constr.items():
        model.add_constr(model.get_var_by_owner(owner) == constr.index)


def expr_lifecycle(owner2constr: dict[Owner, LifeCycle], model: Model) -> None:
    cycles = [(owner, (constr.start, constr.end)) for owner, constr in owner2constr.items()]

    for idx, (owner_left, cycle_left) in enumerate(cycles):
        for owner_right, cycle_right in cycles[idx + 1 :]:
            if not intervals_intersects(cycle_left, cycle_right):
                continue

            _do_not_intersect_expression(
                model.get_var_by_owner(owner_left),
                model.get_var_by_owner(owner_right),
                model,
            )


def _do_not_intersect_expression(left: mip.Var, right: mip.Var, model: Model) -> None:
    abs_pos = model.add_var(None)
    abs_neg = model.add_var(None)

    model.add_constr((left - right) == (abs_pos - abs_neg))
    model.add_sos([(abs_pos, 1), (abs_neg, 1)], 1)
    model.add_constr(abs_pos + abs_neg >= 1)


EXPR_REGISTRY: dict[
    type[BaseConstraint],
    Callable[[dict[Owner, BaseConstraint], Model], None],
] = {
    Index: expr_index,  # type: ignore
    LifeCycle: expr_lifecycle,  # type: ignore
}
