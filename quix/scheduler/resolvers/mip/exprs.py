import mip  # type: ignore

from quix.scheduler.constraints import Array, Index, LifeCycle
from quix.scheduler.owner import Owner

from .model import Model
from .utils import intervals_intersects


def expr_index(owner2constr: dict[Owner, Index], model: Model) -> None:
    for owner, constr in owner2constr.items():
        model.add_constr(model.get_var_by_owner(owner) == constr.index)


def expr_lifecycle(owner2constr: dict[Owner, LifeCycle], arrays: dict[Owner, Array], model: Model) -> None:
    cycles = [(owner, (constr.start, constr.end)) for owner, constr in owner2constr.items()]

    for idx, (owner_left, cycle_left) in enumerate(cycles):
        for owner_right, cycle_right in cycles[idx + 1 :]:
            if not intervals_intersects(cycle_left, cycle_right):
                continue

            if (arr := arrays.get(owner_left)) is None:
                _do_not_intersect_unit_expression(
                    model.get_var_by_owner(owner_left),
                    model.get_var_by_owner(owner_right),
                    model,
                )
                continue

            _do_not_intersect_array_expression(
                model.get_var_by_owner(owner_left),
                arr.length,
                model.get_var_by_owner(owner_right),
                model,
            )


def _do_not_intersect_array_expression(
    anchor: mip.Var,
    length: int,
    right: mip.Var,
    model: Model,
) -> None:
    fir_cond_abs = model.add_var(None)
    fir_cond_neg = model.add_var(None)
    sec_cond_abs = model.add_var(None)
    sec_cond_neg = model.add_var(None)

    model.add_constr((fir_cond_abs - fir_cond_neg) == (right - anchor - length + 2))
    model.add_constr((sec_cond_abs - sec_cond_neg) == (anchor - right + 1))

    model.add_sos([(fir_cond_abs, 1), (fir_cond_neg, 1)], 1)
    model.add_sos([(sec_cond_abs, 1), (sec_cond_neg, 1)], 1)

    model.add_constr(fir_cond_abs + sec_cond_abs >= 2)


def _do_not_intersect_unit_expression(left: mip.Var, right: mip.Var, model: Model) -> None:
    abs_pos = model.add_var(None)
    abs_neg = model.add_var(None)

    model.add_constr((left - right) == (abs_pos - abs_neg))
    model.add_sos([(abs_pos, 1), (abs_neg, 1)], 1)
    model.add_constr(abs_pos + abs_neg >= 1)
