# coding: utf8
""" 
@software: PyCharm
@author: Lionel Johnson
@contact: https://fairy.host
@organization: https://github.com/FairylandFuture
@since: 2024-05-10 12:34:34 UTC+8
"""

import time
from datetime import datetime
from typing import Union, Optional

from fairylandfuture.constants.enums import DateTimeEnum
from fairylandfuture.core.abstracts.metaclass import SingletonMeta
from fairylandfuture.util.verifies.validate import ParamTypeValidator


class DateTimeModule(SingletonMeta):
    """
    Date time utils.
    """

    @classmethod
    def date(cls, _format: str = DateTimeEnum.DATE.value) -> str:
        """
        Get the current date.

        :param _format: Date format.
        :type _format: str
        :return: Current date
        :rtype: str
        """
        return datetime.now().date().strftime(_format)

    @classmethod
    def time(cls, _fromat: str = DateTimeEnum.TIME.value) -> str:
        """
        Get the current time.

        :param _fromat: Time format.
        :type _fromat: str
        :return: Current time
        :rtype: str
        """
        return datetime.now().time().strftime(_fromat)

    @classmethod
    def datetime(cls, _format: str = DateTimeEnum.DATETIME.value) -> str:
        """
        Get the current datetime_str.

        :param _format: Datetime format.
        :type _format: str
        :return: Current datetime_str
        :rtype: str
        """
        return datetime.now().strftime(_format)

    @classmethod
    def timestamp(cls, millisecond: bool = False, n: Optional[int] = None) -> int:
        """
        Get the current timestamp.

        :return: Current timestamp.
        :rtype: int
        """
        validator = ParamTypeValidator({"millisecond": bool, "n": (int, type(None))})
        validator.validate({"millisecond": millisecond, "n": n})

        if millisecond:
            return int(round(time.time()) * 1000)
        if n:
            return int(round(time.time()) * (10 ** (n - 10)))

        return int(round(time.time()))

    @classmethod
    def timestamp_to_datetime(cls, timestamp: Union[int, float], _format: str = DateTimeEnum.DATETIME.value):
        """
        Convert timestamp to datetime_str.

        :param timestamp: Timestamp.
        :type timestamp: int or float
        :param _format: Datetime format.
        :type _format: str
        :return: Formatted datetime_str string.
        :rtype: str
        """
        validator = ParamTypeValidator({"timestamp": (int, float)})
        validator.validate({"timestamp": timestamp})

        if len(str(int(timestamp))) == 13:
            timestamp /= 1000
        return datetime.fromtimestamp(timestamp).strftime(_format)

    @classmethod
    def datetime_to_timestamp(
        cls,
        datetime_string: str,
        millisecond: bool = False,
        n: Optional[int] = None,
        _format: str = DateTimeEnum.DATETIME.value,
    ) -> int:
        """
        Convert datetime to timestamp.

        :param datetime_string: Datetime string.
        :type datetime_string: str
        :param millisecond: Whether to include milliseconds.
        :type millisecond: bool
        :param n: Number of decimal places for the timestamp.
        :type n: int or None
        :param _format: Datetime format.
        :type _format: str
        :return: Timestamp.
        :rtype: int
        """
        validator_expected_types = {"datetime_string": str, "millisecond": bool, "n": (int, type(None)), "_format": str}
        validator = ParamTypeValidator(validator_expected_types)
        validator.validate({"datetime_string": datetime_string, "millisecond": millisecond, "n": n, "_format": _format})

        dt = datetime.strptime(datetime_string, _format)
        timestamp = dt.timestamp()

        if millisecond:
            return int(timestamp * 1000)
        if n:
            return int(timestamp * (10 ** (n - 10)))

        return int(timestamp)
