import time
from collections.abc import Callable
from functools import wraps


def log[**P, R](func: Callable[P, R]) -> Callable[P, R]:
    @wraps(func)
    def _wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        name = func.__name__
        if (name == "__call__") and callable(args[0]):
            name = f"{type(args[0]).__name__}:{name}"
        print(f"Running: {name}")
        start_time = time.time()

        res = func(*args, **kwargs)

        final_time = time.time() - start_time
        print(f"Finished in: {final_time:.2f}s")
        print()
        return res

    return _wrapper
