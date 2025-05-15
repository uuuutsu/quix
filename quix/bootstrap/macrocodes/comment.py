from __future__ import annotations

import re

from quix.bootstrap.dtypes.unit import Unit
from quix.bootstrap.macrocode import macrocode
from quix.bootstrap.program import ToConvert
from quix.core.opcodes.opcodes import end_loop, inject, start_loop
from quix.memoptix.opcodes import free


def _check_text_safety(text: str) -> bool:
    return re.match(r".*([,.><\[\]+-]).*", text) is None


@macrocode
def comment(text: str) -> ToConvert:
    if _check_text_safety(text):
        return inject(None, text, None, sortable=True)

    u1 = Unit("comment_unit")
    yield start_loop(u1)
    yield inject(None, text, None)
    yield end_loop()
    return free(u1)
