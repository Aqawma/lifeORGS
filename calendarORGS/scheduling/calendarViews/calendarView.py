"""
Calendar View Module

This module provides functionality for displaying and formatting calendar events
in a human-readable format. It handles the presentation layer for calendar data,
organizing events by date and time for user-friendly display.

The module works with the event scheduler to retrieve event data and formats it
for console output or other display purposes.
"""

from calendarORGS.scheduling.eventScheduler import Scheduler
from utils.timeUtils import toShortHumanTime, toHumanHour


class CalendarView:
    """
    Static utility class for formatting and displaying calendar events.

    This class provides methods for converting event data into human-readable
    formats suitable for display in the console or other output interfaces.
    It handles date grouping, time formatting, and text organization.
    """

    @staticmethod
    def convertListToText(lists):
        """
        Convert a list of strings into a single formatted text string.

        Takes a list of strings and joins them with newline characters to create
        a single formatted text block suitable for display or output.

        Args:
            lists (list): List of strings to be joined together

        Returns:
            str: Single string with all list items joined by newlines

        Example:
            >>> convertListToText(["Event 1", "Event 2", "Event 3"])
            "Event 1\nEvent 2\nEvent 3"
        """
        outputString = "\n".join(lists)
        return outputString

    @staticmethod
    def viewEvents(timeForecast):
        """
        Formats events into a human-readable list grouped by day.

        This function retrieves events for the specified time period and organizes them
        chronologically by day, creating a formatted list suitable for display.

        Args:
            timeForecast (str): Time period to look ahead in format "<number> D"
                               (e.g., "7 D" for 7 days)

        Returns:
            list: List of strings containing formatted event information grouped by day
        """
        events = Scheduler.giveEvents(timeForecast)
        dayCheck = []
        output = []

        events.sort(key=lambda x: x[2])

        dateSplit = timeForecast.split(" ")
        output.append(f"Events in the next {dateSplit[0]} days:")

        for event in events:
            daySet = toShortHumanTime(event[2])

            if daySet not in dayCheck:
                dayCheck.append(daySet)
                output.append(f"Events on {daySet}:")
                output.append(f"{event[0]} from {toHumanHour(event[2])} to {toHumanHour(event[3])}")

            else:
                toHumanHour(event[2])
                output.append(f"{event[0]} from {toHumanHour(event[2])} to {toHumanHour(event[3])}")

        return output
