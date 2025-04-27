from typing import Final

import pytest

from quix.core.compiler import BFMemoryLayout
from quix.exceptions.core import RefNotFound


def test_layout_no_ref() -> None:
    REF_ONE_POS: Final[int] = 1
    REF_TWO_POS: Final[int] = 5

    layout = BFMemoryLayout({1: REF_ONE_POS, 2: REF_TWO_POS})
    with pytest.raises(RefNotFound):
        layout[3]
