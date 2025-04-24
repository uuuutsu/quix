from collections.abc import Hashable
from dataclasses import dataclass

type Owner = Hashable


@dataclass(slots=True, frozen=True)
class BaseConstraint:
    owner: Owner
