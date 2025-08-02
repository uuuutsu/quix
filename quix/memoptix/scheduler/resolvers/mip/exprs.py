import mip  # type: ignore

from quix.memoptix.scheduler.constraints import Array, HardLink, Index, LifeCycle, SoftLink
from quix.memoptix.scheduler.owner import Owner
from quix.tools import intervals_intersects

from .model import Model


def expr_index(owner2constr: dict[Owner, list[Index]], model: Model) -> None:
    for owner, (constr, *_) in owner2constr.items():
        if len(_) > 0:
            raise ValueError(f"At most one `{Index}` constraint is allowed for each owner.")
        model.add_constr(model.get_var_by_owner(owner) == constr.index)


def expr_lifecycle(
    lifecycles: dict[Owner, list[LifeCycle]],
    arrays: dict[Owner, list[Array]],
    model: Model,
) -> None:
    cycles: list[tuple[Owner, tuple[int, int]]] = []
    for owner, (constr, *_) in lifecycles.items():
        if len(_) > 0:
            raise ValueError(f"At most one `{LifeCycle}` constraint is allowed for each owner.")
        cycles.append((owner, (constr.start, constr.end)))

    for idx, (owner_left, cycle_left) in enumerate(cycles):
        for owner_right, cycle_right in cycles[idx + 1 :]:
            if not intervals_intersects(cycle_left, cycle_right):
                continue

            left_arr = arrays.get(owner_left)
            right_arr = arrays.get(owner_right)

            if left_arr is right_arr is None:
                _do_not_intersect_unit_expression(
                    model.get_var_by_owner(owner_left),
                    model.get_var_by_owner(owner_right),
                    model,
                )
                continue

            if (len(left_arr or []) > 1) or (len(right_arr or []) > 1):
                raise ValueError(f"At most one `{Array}` constraint is allowed for each owner.")

            if left_arr:
                _do_not_intersect_array_expression(
                    model.get_var_by_owner(owner_left),
                    left_arr[0].length,
                    model.get_var_by_owner(owner_right),
                    model,
                )
                continue
            _do_not_intersect_array_expression(
                model.get_var_by_owner(owner_right),
                right_arr[0].length,  # type: ignore
                model.get_var_by_owner(owner_left),
                model,
            )


def expr_links(
    hard_links: dict[Owner, list[HardLink]],
    soft_links: dict[Owner, list[SoftLink]],
    model: Model,
) -> None:
    if set(hard_links).intersection(soft_links):
        raise ValueError("Each owner can have either `SoftLink` constraint or `HardLink` one.")

    _hard_links(hard_links, model)
    _soft_links(soft_links, model)


def _hard_links(hard_links: dict[Owner, list[HardLink]], model: Model) -> None:
    for owner, constrs in hard_links.items():
        for constr in constrs:
            model.add_constr(
                (model.get_var_by_owner(owner) - model.get_var_by_owner(constr.to_)) == constr.distance,
            )


def _soft_links(soft_links: dict[Owner, list[SoftLink]], model: Model) -> None:
    for owner, constrs in soft_links.items():
        for constr in constrs:
            factor_var = model.add_var(
                None,
                lb=1.0,  # type: ignore
            )

            for to_, scale in constr.to_.items():
                model.add_constr(
                    (model.get_var_by_owner(owner) - model.get_var_by_owner(to_)) == (factor_var * scale),  # type: ignore
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

    model.add_constr((fir_cond_abs - fir_cond_neg) == (right - anchor - length + 2))  # type: ignore
    model.add_constr((sec_cond_abs - sec_cond_neg) == (anchor - right + 1))  # type: ignore

    model.add_sos([(fir_cond_abs, 1), (fir_cond_neg, 1)], 1)  # type: ignore
    model.add_sos([(sec_cond_abs, 1), (sec_cond_neg, 1)], 1)  # type: ignore

    model.add_constr(fir_cond_abs + sec_cond_abs >= 2)  # type: ignore


def _do_not_intersect_unit_expression(left: mip.Var, right: mip.Var, model: Model) -> None:
    abs_pos = model.add_var(None)
    abs_neg = model.add_var(None)

    model.add_constr((left - right) == (abs_pos - abs_neg))
    model.add_sos([(abs_pos, 1), (abs_neg, 1)], 1)  # type: ignore
    model.add_constr(abs_pos + abs_neg >= 1)  # type: ignore
