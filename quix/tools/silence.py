import ctypes
import os
import sys
from collections.abc import Iterator
from contextlib import contextmanager


@contextmanager
def silence() -> Iterator[None]:
    sys.stdout.flush()
    libc = ctypes.CDLL(None)
    libc.fflush(None)

    with open(os.devnull, "w") as devnull:
        old_fd = sys.stdout.fileno()
        saved_fd = os.dup(old_fd)

        try:
            os.dup2(devnull.fileno(), old_fd)
            yield
        finally:
            libc.fflush(None)
            os.dup2(saved_fd, old_fd)
            os.close(saved_fd)
