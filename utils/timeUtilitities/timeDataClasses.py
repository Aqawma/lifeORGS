from dataclasses import dataclass

from utils.jsonUtils import loadConfig

@dataclass
class TimeData:
    """
    Data container class for structured time information.

    This dataclass holds comprehensive time data including date components,
    time components, and timezone information. It provides a standardized
    way to represent time data throughout the application.

    Attributes:
        monthNum (int): Month number (01-12) with zero padding
        monthName (str): Full month name (e.g., "January", "February")
        dayOfWeek (str): Full day name (e.g., "Monday", "Tuesday")
        day (int): Day of month (01-31) with zero padding
        hour (int): Hour (00-23) with zero padding
        minute (int): Minute (00-59) with zero padding
        second (int): Second (00-59) with zero padding
        dayNumInWeek (int): Day number in week (1-7) with zero padding
        year (int): Four-digit year
        unixTimeUTC (float): Unix timestamp in UTC
        timeZone (str): User's timezone from configuration

    Example:
        # >>> time_data = TimeData(
        # ...     monthNum=12, monthName="December", dayOfWeek="Monday",
        # ...     day=25, hour=14, minute=30, second=00,
        # ...     dayNumInWeek=1, year=2023, unixTimeUTC=1703530800.0
        # ... )
    """
    monthNum: int
    monthName: str
    dayOfWeek: str
    day: int
    hour: int
    minute: int
    second: int
    dayNumInWeek: int
    year: int

    unixTimeUTC: float
    timeZone: str = loadConfig()['USER_TIMEZONE']

@dataclass
class UnixTimePeriods:
    """
    Constants for common time periods in seconds.

    This dataclass provides convenient constants for time calculations,
    storing the number of seconds in common time periods. These constants
    are used throughout the application for time arithmetic and scheduling.

    Attributes:
        minute (int): Seconds in one minute (60)
        hour (int): Seconds in one hour (3,600)
        day (int): Seconds in one day (86,400)
        week (int): Seconds in one week (604,800)

    Example:
        # >>> periods = UnixTimePeriods()
        # >>> tomorrow = current_time + periods.day
        # >>> next_week = current_time + periods.week
    """
    minute: int = 60
    hour: int = 60 * minute
    day: int = 24 * hour
    week: int = 7 * day
