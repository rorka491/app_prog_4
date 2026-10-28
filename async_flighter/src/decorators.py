from functools import wraps
from time import perf_counter
from typing import Callable, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def measure_time(func: Callable[P, R]) -> Callable[P, R]:
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        start_time = perf_counter()
        result = func(*args, **kwargs)
        processing_time_ms = (perf_counter() - start_time) * 1000

        result.processing_time_ms = processing_time_ms # type: ignore

        return result

    return wrapper