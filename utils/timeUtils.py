"""
Time Utilities Module

This module provides comprehensive time handling utilities for the lifeORGS application.
It includes classes for time data management, datetime tokenization, and various utility
functions for time conversion and formatting.

Dependencies:
- time: For Unix timestamp operations
- datetime: For date and time manipulation
- dataclasses: For structured data containers
- typing: For type hints
- zoneinfo: For timezone handling
- utils.jsonUtils: For loading user timezone configuration

Classes:
- TimeData: Data container for structured time information
- TokenizeToDatetime: Converts time strings to datetime objects
- TimeUtility: Main utility class for time operations

Functions:
- toSeconds: Convert time strings to seconds
- timeOut: Convert time period strings to seconds
- toShortHumanTime: Convert Unix timestamps to readable dates
- toHumanHour: Convert Unix timestamps to readable times
- deltaToStartOfWeek: Calculate seconds since start of week
"""

import time
from datetime import datetime, timezone
from dataclasses import dataclass
from typing import Optional
from zoneinfo import ZoneInfo

from utils.jsonUtils import loadConfig


@dataclass
class TimeData:
    """
    Data container class for structured time information.

    This dataclass holds comprehensive time data including date components,
    time components, and timezone information. It provides a standardized
    way to represent time data throughout the application.

    Attributes:
        monthNum (str): Month number (01-12) with zero padding
        monthName (str): Full month name (e.g., "January", "February")
        dayOfWeek (str): Full day name (e.g., "Monday", "Tuesday")
        day (str): Day of month (01-31) with zero padding
        hour (str): Hour (00-23) with zero padding
        minute (str): Minute (00-59) with zero padding
        second (str): Second (00-59) with zero padding
        dayNumInWeek (str): Day number in week (1-7) with zero padding
        year (str): Four-digit year
        unixTimeUTC (float): Unix timestamp in UTC
        timeZone (str): User's timezone from configuration

    Example:
        >>> time_data = TimeData(
        ...     monthNum="12", monthName="December", dayOfWeek="Monday",
        ...     day="25", hour="14", minute="30", second="00",
        ...     dayNumInWeek="01", year="2023", unixTimeUTC=1703530800.0
        ... )
    """
    monthNum: str
    monthName: str
    dayOfWeek: str
    day: str
    hour: str
    minute: str
    second: str
    dayNumInWeek: str
    year: str

    unixTimeUTC: float
    timeZone: str = loadConfig()['USER_TIMEZONE']

class TokenizeToDatetime:
    """
    Tokenizes time strings and converts them to datetime objects.

    This class handles the parsing of time strings in DD/MM/YYYY HH:MM format
    and converts them into Python datetime objects for further processing.

    Attributes:
        timeDict (dict): Dictionary containing parsed date and time components
        datetimeObj (datetime): Python datetime object created from the parsed time string

    Example:
        >>> tokenizer = TokenizeToDatetime("25/12/2023 14:30")
        >>> print(tokenizer.datetimeObj)
        datetime.datetime(2023, 12, 25, 14, 30)
    """

    @staticmethod
    def _splitTime(timeString):
        """
        Splits a time string into date and time components.

        Parses a time string in DD/MM/YYYY HH:MM format and separates
        the date and time parts into lists for further processing.

        Args:
            timeString (str): Time string in format "DD/MM/YYYY HH:MM"

        Returns:
            dict: Dictionary with 'date' and 'time' keys containing lists
                  of string components

        Example:
            >>> TokenizeToDatetime._splitTime("25/12/2023 14:30")
            {'date': ['25', '12', '2023'], 'time': ['14', '30']}
        """
        # Split the string into date and time parts
        parts = timeString.split(" ")
        date = parts[0].split("/")  # [day, month, year]
        times = parts[1].split(":")  # [hour, minute]

        parsedTimeDict = {
            'date': date,
            'time': times,
        }
        return parsedTimeDict

    def __init__(self, timeString):
        """
        Initialize the TokenizeToDatetime with a time string.

        Parses the provided time string and creates a datetime object
        from the parsed components.

        Args:
            timeString (str): Time string in format "DD/MM/YYYY HH:MM"

        Raises:
            ValueError: If the time string format is invalid
            IndexError: If the time string doesn't have enough components
        """
        # Parse the time string into components
        self.timeDict = self._splitTime(timeString)

        # Create datetime object from parsed components
        # Note: datetime expects (year, month, day, hour, minute)
        self.datetimeObj = datetime(int(self.timeDict['date'][2]),  # year
                                    int(self.timeDict['date'][1]),  # month
                                    int(self.timeDict['date'][0]),  # day
                                    int(self.timeDict['time'][0]),  # hour
                                    int(self.timeDict['time'][1]))  # minute

class TimeUtility:
    """
    Main utility class for time operations and conversions.

    This class provides comprehensive time handling capabilities including
    Unix timestamp conversion, timezone handling, and structured time data generation.
    It serves as the primary interface for time operations in the application.

    Attributes:
        currentTime (float): Current Unix timestamp
        intoUnix (Optional[datetime]): Datetime object for conversion to Unix timestamp
        unixTimeUTC (Optional[float]): Unix timestamp in UTC
        timeZone (str): User's timezone from configuration

    Example:
        >>> # Convert time string to Unix timestamp
        >>> utility = TimeUtility(intoUnix="25/12/2023 14:30")
        >>> unix_time = utility.convertToUTC()

        >>> # Generate structured time data from Unix timestamp
        >>> utility = TimeUtility(unixTimeUTC=1703530800.0)
        >>> time_data = utility.generateTimeDataObj()
    """

    def __init__(self, intoUnix: str = None, unixTimeUTC: float = None):
        """
        Initialize the TimeUtility with optional time parameters.

        Args:
            intoUnix (str, optional): Time string in DD/MM/YYYY HH:MM format
                                     to be converted to Unix timestamp
            unixTimeUTC (float, optional): Unix timestamp in UTC for processing

        Note:
            At least one parameter should be provided for meaningful operations.
            If both are provided, both will be available for different operations.
        """
        # Store current system time
        self.currentTime: float = time.time()

        # Convert time string to datetime object if provided
        self.intoUnix: Optional[datetime] = TokenizeToDatetime(intoUnix).datetimeObj if intoUnix else None

        # Store Unix timestamp if provided
        self.unixTimeUTC: Optional[float] = unixTimeUTC

        # Load user's timezone from configuration
        self.timeZone: str = loadConfig()['USER_TIMEZONE']

    def updateCurrentTime(self) -> float:
        """
        Updates and returns the current system time.

        Refreshes the currentTime attribute with the current Unix timestamp.

        Returns:
            float: Current Unix timestamp
        """
        self.currentTime = time.time()
        return self.currentTime

    def convertToUTC(self) -> float:
        """
        Converts the stored datetime object to UTC Unix timestamp.

        Takes the datetime object stored in intoUnix and converts it to
        a Unix timestamp assuming UTC timezone.

        Returns:
            float: Unix timestamp in UTC

        Raises:
            AttributeError: If intoUnix is None (no datetime object to convert)

        Example:
            >>> utility = TimeUtility(intoUnix="25/12/2023 14:30")
            >>> unix_time = utility.convertToUTC()
            >>> print(unix_time)  # Unix timestamp for the specified time
        """
        # Convert datetime to UTC timestamp and store it
        self.unixTimeUTC = self.intoUnix.replace(tzinfo=timezone.utc).timestamp()
        return self.unixTimeUTC

    def generateTimeDataObj(self) -> TimeData:
        """
        Generates a structured TimeData object from the stored Unix timestamp.

        Converts the Unix timestamp to the user's timezone and creates a comprehensive
        TimeData object with all time components formatted and named appropriately.

        Returns:
            TimeData: Structured time data object with all time components

        Raises:
            Exception: If no Unix timestamp is provided (unixTimeUTC is None)

        Example:
            >>> utility = TimeUtility(unixTimeUTC=1703530800.0)
            >>> time_data = utility.generateTimeDataObj()
            >>> print(f"{time_data.dayOfWeek}, {time_data.monthName} {time_data.day}")
            "Monday, December 25"
        """
        if self.unixTimeUTC is None:
            raise Exception("No Unix timestamp provided")

        # Define month and day names for human-readable formatting
        monthNames = ["January", "February", "March",
                      "April", "May", "June",
                      "July", "August", "September",
                      "October", "November", "December"]
        dayOfWeekNames = ["Monday", "Tuesday", "Wednesday",
                          "Thursday", "Friday", "Saturday", "Sunday"]

        # Load user's timezone from configuration
        userTimeZone = loadConfig()['USER_TIMEZONE']

        # Convert UTC timestamp to user's timezone
        utcDateTime = datetime.fromtimestamp(self.unixTimeUTC, tz=timezone.utc)
        userDateTime = utcDateTime.astimezone(ZoneInfo(userTimeZone))

        # Create and return structured TimeData object
        return TimeData(
            monthNum=str(userDateTime.month).zfill(2),           # Zero-padded month number
            monthName=monthNames[userDateTime.month - 1],        # Full month name
            dayOfWeek=dayOfWeekNames[userDateTime.weekday()],    # Full day name
            day=str(userDateTime.day).zfill(2),                 # Zero-padded day
            hour=str(userDateTime.hour).zfill(2),               # Zero-padded hour (24h)
            minute=str(userDateTime.minute).zfill(2),           # Zero-padded minute
            second=str(userDateTime.second).zfill(2),           # Zero-padded second
            dayNumInWeek=str(userDateTime.isoweekday()).zfill(2), # ISO weekday (1=Monday)
            year=str(userDateTime.year),                        # Four-digit year
            unixTimeUTC=self.unixTimeUTC,                       # Original Unix timestamp
        )

def toSeconds(time):
    """
    Converts a time string in HH:MM or HH:MM:SS format to total seconds.

    Args:
        time (str): Time string in format 'HH:MM' or 'HH:MM:SS'

    Returns:
        int: Total seconds (hours*3600 + minutes*60 + seconds)

    Example:
        # >>> toSeconds("14:30")
        # Returns 52,200 (14 hours and 30 minutes in seconds)
        # >>> toSeconds("14:30:15")
        # Returns 52,215 (14 hours, 30 minutes, and 15 seconds)
    """
    time = time.split(':')
    combinedTime = int(time[0]) * 3600 + int(time[1]) * 60
    if len(time) == 3:
        combinedTime += int(time[2])
    return combinedTime

def timeOut(timeString):
    """
    Converts a time period string to total seconds.

    Currently, supports only day format (e.g., "7 D" for 7 days).

    Args:
        timeString (str): Time period string in format "<number> D" for days

    Returns:
        int: Total seconds in the specified time period

    Raises:
        Exception: If the time format is not supported

    Example:
        # >>> timeOut("7 D")
        # Returns 604,800 (7 days in seconds)

    Note:
        Future enhancement planned to support more time formats.
    """
    time = timeString.split(" ")

    if time[1] == "D":
        timeString = int(time[0]) * 86400
        return timeString

    else:
        #TODO Make this logic better
        raise Exception("Invalid time format")

def toShortHumanTime(unixTime):
    """
    Converts a Unix timestamp to a human-readable date string.

    Args:
        unixTime (float): Unix timestamp (seconds since January 1, 1970)

    Returns:
        str: Formatted date string in the format "Weekday, Month Day"
             (e.g., "Monday, January 1")

    Example:
        # >>> toShortHumanTime(1640430600)
        # Returns "Saturday, December 25" (for December 25, 2021)
    """
    realTime = datetime.fromtimestamp(unixTime).strftime('%A, %B %d')

    return realTime

def toHumanHour(unixTime):
    """
    Converts a Unix timestamp to a human-readable time string.

    Args:
        unixTime (float): Unix timestamp (seconds since January 1, 1970)

    Returns:
        str: Formatted time string in 12-hour format with AM/PM indicator
             (e.g., "02:30 PM")

    Example:
        # >>> toHumanHour(1640430600)
        # Returns "10:30 AM" (assuming this timestamp corresponds to 10:30 AM)
    """
    realTime = datetime.fromtimestamp(unixTime).strftime('%I:%M %p')

    return realTime

def deltaToStartOfWeek(currentTime):
    """
    Calculates the number of seconds elapsed since the start of the current week.

    The week is considered to start on Monday at 00:00:00. This function calculates
    how many seconds have passed from the beginning of the week to the given time.

    Args:
        currentTime (float): Unix timestamp (seconds since January 1, 1970)

    Returns:
        int: Number of seconds elapsed since the start of the current week (Monday 00:00:00)

    Example:
        # >>> deltaToStartOfWeek(1640430600) # Assuming this is a Wednesday at 10:30 AM
        # Returns the number of seconds from Monday 00:00:00 to Wednesday 10:30 AM
        # (2 days * 86,400 seconds/day + 10.5 hours * 3600 seconds/hour)

    Note:
        - Monday is considered day 0 of the week
        - The calculation includes weekday, hour, minute, and second components
        - Result is in seconds and can be used for scheduling calculations
    """
    weekStart = (datetime.fromtimestamp(currentTime).weekday() * 86400
                 + datetime.fromtimestamp(currentTime).hour * 3600
                 + datetime.fromtimestamp(currentTime).minute * 60
                 + datetime.fromtimestamp(currentTime).second)
    return weekStart  # Seconds since start of week (Monday)
