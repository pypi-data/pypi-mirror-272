# coding: utf8
""" 
@software: PyCharm
@author: Lionel Johnson
@contact: https://fairy.host
@organization: https://github.com/FairylandFuture
@since: 2024-05-10 12:34:34 UTC+8
"""

from typing import Union, Any
from datetime import datetime, timedelta
import time
from dateutil.relativedelta import relativedelta

from datetime import date as TypeDate
from datetime import time as TypeTime

from fairylandfuture.modules.decorators import SingletonDecorator
from fairylandfuture.constants.enums import DateTimeEnum


@SingletonDecorator
class DateTimeUtils:
    """
    Date time utils.
    """
    
    @classmethod
    def timestamp(cls) -> int:
        """
        Get the current timestamp.
        
        :return: Current timestamp.
        :rtype: int
        """
        return round(time.time())








class DatetimeUtils:
    """
    Date time utils.
    """

    @classmethod
    def normtimestamp(cls) -> int:
        """
        Standard 10-bit timestamps

        :return: 10-bit timestamps: Integer
        :rtype: int
        """
        return time.time().__int__()

    @classmethod
    def timestamp_nbit(cls, n: int) -> int:
        """
        n-bit timestamps

        :param n: n-bit: Integer
        :return: n-bit timestamps: String
        :rtype: str
        """
        if not isinstance(n, int):
            raise TypeError("The n argument must be of type int.")

        timestamp_str = time.time().__str__().replace(".", "")
        if n <= 16:
            result = timestamp_str[:n]
        else:
            result = "".join((timestamp_str, (n - len(timestamp_str)) * "0"))

        return int(result)

    @classmethod
    def timestamp_milliseconds(cls) -> int:
        """
        Get the current time in milliseconds.

        :return: The current time in milliseconds
        :rtype: int
        """
        return round(time.time() * 1000)

    @classmethod
    def normdatetime(cls) -> datetime:
        """
        Get the current date and time.

        :return: Current date and time
        :rtype: datetime
        """
        return datetime.now()

    @classmethod
    def normdatetime_to_string(cls, __format=DateTimeEnum.DATETIME.value) -> str:
        """
        Get the current date and time as a formatted string. %Y-%m-%d %H:%M:%S

        :return: Formatted date and time string
        :rtype: str
        """
        if not isinstance(__format, str):
            raise TypeError("The format argument must be of type str.")

        return datetime.now().strftime(__format)

    @classmethod
    def normnowdate(cls) -> TypeDate:
        """
        Get the current date.

        :return: Current date
        :rtype: datetime
        """
        return datetime.now().date()

    @classmethod
    def normnowdate_to_string(cls, __format=DateTimeEnum.DATE.value) -> str:
        """
        Get the current date as a formatted string.

        :return: Formatted date string
        :rtype: str
        """
        if not isinstance(__format, str):
            raise TypeError("The format argument must be of type str.")

        return datetime.now().date().strftime(__format)

    @classmethod
    def normnowtime(cls) -> TypeTime:
        """
        Get the current time.

        :return: Current time
        :rtype: datetime
        """
        return datetime.now().time()

    @classmethod
    def normnowtime_to_string(cls, __format: str = DateTimeEnum.TIME.value) -> str:
        """
        Get the current time as a formatted string. %H:%M:%S

        :return: Formatted time string
        :rtype: str
        """
        if not isinstance(__format, str):
            raise TypeError("The format argument must be of type str.")

        return datetime.now().time().strftime(__format)

    @classmethod
    def timestamp_to_datetime(cls, timestamp: Union[int, float]) -> datetime:
        """
        Convert timestamp to datetime

        :param timestamp: Timestamp value
        :type timestamp: int or float
        :return: Corresponding datetime
        :rtype: datetime
        """
        if not isinstance(timestamp, (int, float)):
            raise TypeError("The timestamp argument must be of type int or float.")

        if isinstance(timestamp, int):
            timestamp = float(timestamp)

        return datetime.fromtimestamp(timestamp)

    @classmethod
    def datetime_to_timestamp(cls, datetime_object: datetime) -> float:
        """
        Convert datetime to timestamp

        :param datetime_object: Datetime object
        :type datetime_object: datetime
        :return: Corresponding timestamp
        :rtype: float
        """
        return datetime_object.timestamp() if datetime_object else datetime.now().timestamp()

    @classmethod
    def timestamp_to_datetimestring(cls, timestamp: Union[int, float], __format: str = DateTimeEnum.DATETIME.value) -> str:
        """
        Convert timestamp to formatted string

        :param timestamp: Timestamp value
        :type timestamp: Union[int, float]
        :param __format: Format string
        :type __format: str
        :return: Formatted string
        :rtype: str
        """
        if not isinstance(timestamp, (int, float)):
            raise TypeError("The timestamp argument must be of type int or float.")
        if not isinstance(__format, str):
            raise TypeError("The format argument must be of type str.")

        if isinstance(timestamp, int):
            timestamp = float(timestamp)

        return datetime.fromtimestamp(timestamp).strftime(__format)

    @classmethod
    def string_to_timestamp(cls, string: str, __format: str = DateTimeEnum.DATETIME.value) -> float:
        """
        Convert string to timestamp

        :param string: String representation of datetime
        :type string: str
        :param __format: Format string
        :type __format: str
        :return: Corresponding timestamp
        :rtype: float
        """
        if not isinstance(string, str):
            raise TypeError("The string argument must be of type str.")
        if not isinstance(__format, str):
            raise TypeError("The format argument must be of type str.")

        return time.mktime(time.strptime(string, __format))

    @classmethod
    def datetime_to_string(cls, datetime_object: datetime, __format: str = DateTimeEnum.DATETIME.value) -> str:
        """
        Convert datetime to string

        :param datetime_object: Datetime object
        :type datetime_object: datetime
        :param __format: Format string
        :type __format: str
        :return: Formatted string
        :rtype: str
        """
        if not isinstance(__format, str):
            raise TypeError("The format argument must be of type str.")

        return datetime_object.strftime(__format)

    @classmethod
    def string_to_datetime(cls, string: str, format: str = DateTimeEnum.DATETIME.value) -> datetime:
        """
        Convert string to datetime

        :param string: String representation of datetime
        :type string: str
        :param format: Format string
        :type format: str
        :return: Corresponding datetime
        :rtype: datetime
        """
        if not isinstance(string, str):
            raise TypeError("The string argument must be of type str.")

        return datetime.strptime(string, format)

    @classmethod
    def add_datetime(
        cls, years: int = 0, months: int = 0, days: int = 0, hours: int = 0, minutes: int = 0, seconds: int = 0, **kwargs: Any
    ) -> datetime:
        """
        Adds the specified number of years, months, days, hours, minutes, and seconds to the current date and time.

        :param years: The number of years to add.
        :type years: int
        :param months: The number of months to add.
        :type months: int
        :param days: The number of days to add.
        :type days: int
        :param hours: The number of hours to add.
        :type hours: int
        :param minutes: The number of minutes to add.
        :type minutes: int
        :param seconds: The number of seconds to add.
        :type seconds: int
        :param kwargs: Additional optional parameters.
        :type kwargs: Any
        :return: The calculated date and time.
        :rtype: datetime
        """
        if not isinstance(years, int):
            raise TypeError("The years argument must be of type int.")
        if not isinstance(months, int):
            raise TypeError("The months argument must be of type int.")
        if not isinstance(days, int):
            raise TypeError("The days argument must be of type int.")
        if not isinstance(hours, int):
            raise TypeError("The hours argument must be of type int.")
        if not isinstance(minutes, int):
            raise TypeError("The minutes argument must be of type int.")
        if not isinstance(seconds, int):
            raise TypeError("The seconds argument must be of type int.")

        return datetime.now() + relativedelta(years=years, months=months, days=days, hours=hours, minutes=minutes, seconds=seconds, **kwargs)

    @classmethod
    def sub_datetime(
        cls, years: int = 0, months: int = 0, days: int = 0, hours: int = 0, minutes: int = 0, seconds: int = 0, **kwargs: Any
    ) -> datetime:
        """
        Subtracts the specified number of years, months, days, hours, minutes, and seconds from the current date and time.

        :param years: The number of years to subtract.
        :type years: int
        :param months: The number of months to subtract.
        :type months: int
        :param days: The number of days to subtract.
        :type days: int
        :param hours: The number of hours to subtract.
        :type hours: int
        :param minutes: The number of minutes to subtract.
        :type minutes: int
        :param seconds: The number of seconds to subtract.
        :type seconds: int
        :param kwargs: Additional optional parameters.
        :type kwargs: Any
        :return: The calculated date and time.
        :rtype: datetime
        """
        if not isinstance(years, int):
            raise TypeError("The years argument must be of type int.")
        if not isinstance(months, int):
            raise TypeError("The months argument must be of type int.")
        if not isinstance(days, int):
            raise TypeError("The days argument must be of type int.")
        if not isinstance(hours, int):
            raise TypeError("The hours argument must be of type int.")
        if not isinstance(minutes, int):
            raise TypeError("The minutes argument must be of type int.")
        if not isinstance(seconds, int):
            raise TypeError("The seconds argument must be of type int.")

        return datetime.now() - relativedelta(years=years, months=months, days=days, hours=hours, minutes=minutes, seconds=seconds, **kwargs)

    @classmethod
    def yesterday(cls) -> datetime:
        """
        Get the datetime for yesterday.

        :return: Yesterday's datetime.
        :rtype: datetime
        """
        return cls.sub_datetime(days=1)

    @classmethod
    def tomorrow(cls) -> datetime:
        """
        Get the datetime for tomorrow.

        :return: Tomorrow's datetime.
        :rtype: datetime
        """
        return cls.add_datetime(days=1)

    @classmethod
    def week_later(cls) -> datetime:
        """
        Get the datetime for a week later.

        :return: Datetime for a week later.
        :rtype: datetime
        """
        return cls.add_datetime(days=7)

    @classmethod
    def month_later(cls) -> datetime:
        """
        Get the datetime for a month later.

        :return: Datetime for a month later.
        :rtype: datetime
        """
        return cls.add_datetime(months=1)

    @classmethod
    def datetimedelta_days(cls, normdatetime: str) -> int:
        """
        Calculate the difference in days between the given date and the current date.

        :param normdatetime: The normalized date in the format 'YYYY-MM-DD'.
        :type normdatetime: str
        :return: The difference in days.
        :rtype: int
        """
        if not isinstance(normdatetime, str):
            raise TypeError("The normdatetime argument must be of type str.")

        try:
            given_date = datetime.strptime(normdatetime, DateTimeEnum.DATE.value)
        except Exception:
            raise ValueError("Invalid date format. The date should be in the format 'YYYY-MM-DD'.")
        delta = datetime.now() - given_date

        return abs(delta.days)

    @classmethod
    def datetimerelative(cls, days: int) -> str:
        """
        Calculate the date that is 'days' days away from the current date.

        :param days: The number of days, positive or negative.
        :type days: int
        :return: The calculated date.
        :rtype: str
        """
        if not isinstance(days, int):
            raise TypeError("The days argument must be of type int.")

        relative_date = (datetime.now() + timedelta(days=days)).strftime(DateTimeEnum.DATETIME.value)

        return relative_date

    @classmethod
    def current_milliseconds(cls) -> int:
        """
        Get the current time in milliseconds.

        :return: The current time in milliseconds
        :rtype: int
        """
        return round(time.time() * 1000)

    @classmethod
    def today_timestamp(cls) -> int:
        """
        The timestamp of the day at 0:00

        :return: Norm Timestamp
        :rtype: int
        """
        return round(time.mktime(datetime.date.today().timetuple()))
