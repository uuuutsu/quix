import mip  # type: ignore

from quix.scheduler.constraints import Index

from .model import Model


def handle_index(var: mip.Var, model: Model, constr: Index) -> None:
    model.add_constr(var == constr.index)
