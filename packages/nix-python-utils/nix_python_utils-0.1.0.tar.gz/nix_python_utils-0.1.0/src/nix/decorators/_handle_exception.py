from functools import wraps
from logging import Logger
from typing import Callable, Any


def handle_exception(handler: Callable[[Exception], Any] = None, exceptions=Exception, default_value=None,
                     raise_exception: bool = False,
                     logger: Logger = None, *handlers_args, **handler_kwargs):
    """
    A decorator to handle exceptions in a function.

    Parameters:
    handler (Callable[[Exception], Any]): A function that handles the exception. It should accept an Exception as its first argument.
    exceptions (Exception): The type of exceptions to catch. Defaults to all exceptions.
    default_value (Any): The value to return if an exception occurs and is not re-raised or handled by the handler function.
    raise_exception (bool): If True, the exception will be re-raised after being logged or handled.
    logger (Logger): A logger to log the exception. If not provided, the exception will not be logged.
    handlers_args (tuple): Additional positional arguments to pass to the handler function.
    handler_kwargs (dict): Additional keyword arguments to pass to the handler function.

    Returns:
    Callable: A decorated function that handles exceptions according to the provided parameters.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exceptions as error:
                if logger is not None:
                    logger.exception(f"Exception occurred in {func.__name__}: {error}")
                if handler is not None:
                    return handler(error, *handlers_args, **handler_kwargs)
                if raise_exception:
                    raise error
                return default_value

        return wrapper

    return decorator
