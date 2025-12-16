app/core/profiler.py

import time
import functools

def timed(fn):
    """
    Production-safe performance timing decorator.
    Use ONLY on heavy service or analytics functions.
    """

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = fn(*args, **kwargs)
        duration = time.perf_counter() - start
        print(f"[PERF] {fn.__name__} took {duration:.4f}s")
        return result

    return wrapper