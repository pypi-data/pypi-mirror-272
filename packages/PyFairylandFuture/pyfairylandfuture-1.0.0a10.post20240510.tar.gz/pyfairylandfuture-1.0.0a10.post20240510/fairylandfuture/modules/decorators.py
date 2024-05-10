# coding: utf8
""" 
@software: PyCharm
@author: Lionel Johnson
@contact: https://fairy.host
@organization: https://github.com/FairylandFuture
@since: 2024-05-10 10:20:53 UTC+8
"""

import time

from types import FunctionType, MethodType
from typing import Union, Any, Callable

from fairylandfuture.modules.journal import journal, logger


class SingletonDecorator:
    """
    Implements the Singleton pattern as a decorator class.

    This class ensures that a class is only instantiated once and
    returns the same instance on subsequent calls.
    """

    def __init__(self, __cls):
        self.__cls = __cls
        self.__instance = dict()

    def __call__(self, *args: Any, **kwargs: Any):
        """
        On call, ensures the decorated class is instantiated only once
        and returns the singleton instance.

        :param args: args
        :type args: tuple
        :param kwargs: kwargs
        :type kwargs: dict
        :return: Singleton instance
        :rtype: Any
        """
        if not self.__instance:
            self.__instance.update(__instance=self.__cls(*args, **kwargs))
            return self.__instance.get("__instance")
        else:
            return self.__instance.get("__instance")


class TimingDecorator:
    """
    Calculate running time
    """

    def __init__(self, __method: Union[FunctionType, MethodType]):
        self.__method = __method

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """
        Execute the wrapped method and calculate its execution time.

        :param args: Positional arguments passed to the method.
        :type args: ...
        :param kwargs: Keyword arguments passed to the method.
        :type kwargs: ...
        :return: The result of the method execution.
        :rtype: ...
        """
        start_time = time.time()
        results = self.__method(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        if elapsed_time.__lt__(60):
            hour, minute, second = 0, 0, elapsed_time
        elif elapsed_time.__ge__(60) and elapsed_time.__lt__(3600):
            hour = 0
            minute = (elapsed_time / 60).__int__()
            second = elapsed_time % 60
        else:
            hour = (elapsed_time / 3600).__int__()
            minute = ((elapsed_time - (hour * 3600)) / 60).__int__()
            second = elapsed_time % 60

        elapsed_time_format_str = f"{hour:02d}:{minute:02d}:{second:06.3f}"
        journal.success(f"This method ran for {elapsed_time_format_str}")

        return results


class ActionDecorator:
    """
    Decorator to log method execution tips (start, success, failure).

    :param name: The name of the method for logging purposes. Defaults to "A Method".
    :type name: str
    """

    def __init__(self, name: str = "A Method"):
        self.__name = name

    def __call__(self, __method: Union[FunctionType, MethodType], *args: Any, **kwargs: Any) -> Callable[..., Any]:
        """
        The decorator's logic to wrap around the given method.

        :param __method: The function or method to be decorated.
        :type __method: FunctionType or MethodType
        :param args: args
        :type args: Any
        :param kwargs: kwargs
        :type kwargs: Any
        :return: The wrapper function around the original method.
        :rtype: Callable
        """

        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """
            Wrapper function that logs the execution status (start, success, failure) of the decorated method.

            :param args: Positional arguments for the decorated method.
            :type args: Any
            :param kwargs: Keyword arguments for the decorated method.
            :type kwargs: Any
            :return: The return value of the decorated method.
            :rtype: ...
            """
            try:
                journal.info(f"Action Running {self.__name}")
                results = __method(*args, **kwargs)
                journal.success(f"Success Running {self.__name}")
            except Exception as error:
                journal.exception(error)
                journal.error(f"Failure Running {self.__name}")
                journal.error(error.args.__getitem__(0))
                raise error

            return results

        return wrapper


class TryCatchDecorator:
    """
    A decorator to catch exceptions thrown by the method it decorates.
    """

    def __init__(self, __method: Union[FunctionType, MethodType]):
        self.__method = __method

    def __call__(self, *args, **kwargs):
        """
        Execute the decorated method and catch any exceptions.

        :param args: Positional arguments for the method.
        :param kwargs: Keyword arguments for the method.
        :return: The result of the method if no exceptions are raised.
        """
        try:
            results = self.__method(*args, **kwargs)
        except Exception as error:
            journal.exception(f"An error occurred: {error}")
            raise error

        return results


class TipsDecorator:
    """
    A decorator to log the start of a method execution.
    """

    def __init__(self, __method: Union[FunctionType, MethodType]):
        self.__method = __method

    def __call__(self, *args, **kwargs):
        """
        Log the method execution and then execute the method.

        :param args: Positional arguments for the method.
        :param kwargs: Keyword arguments for the method.
        :return: The result of the method.
        """
        journal.info(f"Running {self.__method.__name__}")
        results = self.__method(*args, **kwargs)

        return results
