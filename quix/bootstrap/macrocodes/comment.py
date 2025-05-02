from __future__ import annotations

import re

from quix.bootstrap.dtypes.unit import Unit
from quix.bootstrap.program import ToConvert, convert
from quix.core.opcodes.opcodes import inject, loop
from quix.memoptix.opcodes import free


def _check_text_safety(text: str) -> bool:
    return re.match(r".*([,.><\[\]+-]).*", text) is None


@convert
def comment(text: str) -> ToConvert:
    if _check_text_safety(text):
        return inject(None, text, None, sortable=True)

    u1 = Unit("comment_unit")
    yield loop(u1, [inject(None, text, None)])
    return free(u1)
