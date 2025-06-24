from datetime import datetime

def toUnixTime(eventTime):
    """
    Converts a date and time string to Unix timestamp.

    Args:
        eventTime (str): Date and time in format 'DD/MM/YYYY HH:MM'

    Returns:
        float: Unix timestamp (seconds since January 1, 1970)

    Example:
        # >>> toUnixTime("25/12/2023 14:30")
        # Returns the Unix timestamp for December 25, 2023, at 2:30 PM
    """
    # Split the date and time parts
    parts = eventTime.split(" ")
    date = parts[0].split("/")
    time = parts[1].split(":")

    # Create datetime object
    dt = datetime(int(date[2]), int(date[1]), int(date[0]), int(time[0]), int(time[1]))
    return dt.timestamp()

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
    combinedTime = int(time[0])*3600 + int(time[1])*60
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
        # >>> deltaToStartOfWeek(1640430600)  # Assuming this is a Wednesday at 10:30 AM
        # Returns the number of seconds from Monday 00:00:00 to Wednesday 10:30 AM
        # (2 days * 86400 seconds/day + 10.5 hours * 3600 seconds/hour)

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
