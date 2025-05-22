from quix.bootstrap.macrocode import macrocode


@macrocode
def _nop() -> None:
    return None


NOP = _nop()
