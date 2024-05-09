import asyncio
import functools
import time
from contextlib import contextmanager

from .measure_service import profiling_service


#
# @author andy
#
def profiler(name=None):
    def decorator(func):
        @contextmanager
        def profiling_context(func_name: str):
            is_error = False
            begin_time = time.time() * 1000_000_000
            profiling_service.start_measure(func_name)
            try:
                yield
            except Exception as error:
                is_error = True
                raise error
            finally:
                profiling_service.stop_measure(
                    func_name,
                    time.time() * 1000_000_000 - begin_time,
                    is_error=is_error
                )

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if name is None:
                try:
                    func_name = func.__func__.__qualname__
                except:
                    func_name = func.__qualname__
            else:
                func_name = name

            if not asyncio.iscoroutinefunction(func):
                with profiling_context(func_name):
                    return func(*args, **kwargs)
            else:
                async def async_profiling():
                    with profiling_context(func_name):
                        return await func(*args, **kwargs)

                return async_profiling()

        return wrapper

    return decorator
