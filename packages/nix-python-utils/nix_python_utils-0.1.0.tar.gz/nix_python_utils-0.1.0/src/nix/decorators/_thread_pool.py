from typing import Any, List
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import wraps
from logging import Logger


def thread_pool(num_threads=4, exceptions=Exception, raise_first_exception=False, logger: Logger = None):
    """
    A decorator that runs a function in a thread pool.

    This decorator creates a thread pool with a specified number of threads and runs the decorated function in this pool.
    The results of all tasks are collected and returned as a list. If an exception occurs in a task, it is logged and,
    if specified, re-raised.

    Args:
        num_threads (int, optional): The number of threads in the pool. Defaults to 4.
        exceptions (Exception, optional): The type of exceptions to catch. Defaults to Exception.
        raise_first_exception (bool, optional): Whether to re-raise the first exception that occurs. Defaults to False.
        logger (Logger, optional): The logger to use for logging exceptions. Defaults to None.

    Returns:
         Callable: A decorated function that handles exceptions according to the provided parameters.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            results = []
            with ThreadPoolExecutor(max_workers=num_threads) as executor:
                futures = {executor.submit(func, *args, **kwargs) for _ in range(num_threads)}
                for future in as_completed(futures):
                    try:
                        results.append(future.result())
                    except exceptions as e:
                        if logger is not None:
                            logger.exception(f"An exception occurred in thread: {e}")
                        if raise_first_exception:
                            raise e
            return results

        return wrapper

    return decorator
