"""
Calendar View Module

This module provides functionality for displaying and formatting calendar events
in a human-readable format. It handles the presentation layer for calendar data,
organizing events by date and time for user-friendly display.

The module works with the event scheduler to retrieve event data and formats it
for console output or other display purposes.
"""
from pathlib import Path
import json

from calendarORGS.scheduling.eventScheduler import Scheduler
from utils.dbUtils import ConnectDB
from utils.projRoot import getProjRoot
from utils.timeUtilitities.timeDataClasses import UnixTimePeriods
from utils.timeUtilitities.timeUtil import toShortHumanTime, toHumanHour, TimeConverter, TimeData
from utils.timeUtilitities.startAndEndBlocks import TimeStarts

class EventObj:
    """
    Represents a calendar event with time calculations and formatting.

    This class encapsulates event data and provides calculated properties
    for display and scheduling purposes, including day-relative timing
    and percentage calculations for visual representation.

    Attributes:
        iD (str): EventObj identifier/name
        description (str): EventObj description text
        start (int): EventObj start time as Unix timestamp
        startParsed (TimeData): Parsed start time data object
        end (int): EventObj end time as Unix timestamp
        endParsed (TimeData): Parsed end time data object
        startFromDay (int): Seconds from start of day to event start
        endFromDay (int): Seconds from start of day to event end
        percentOfDay (float): Percentage of day occupied by this event
    """
    def __init__(self, eventTuple: tuple):
        """
        Initialize EventObj object from database tuple.

        Args:
            eventTuple (tuple): Database row containing (id, description, start_time, end_time)
        """
        self.iD: str = eventTuple[0]
        self.description: str = eventTuple[1]
        self.start: int = eventTuple[2]
        # Parse start time into structured TimeData object for easy access to date components
        self.startParsed: TimeData = TimeConverter(unixtime=eventTuple[2]).generateTimeDataObj()
        self.end: int = eventTuple[3]
        # Parse end time into structured TimeData object for easy access to date components
        self.endParsed: TimeData = TimeConverter(unixtime=eventTuple[3]).generateTimeDataObj()
        # Calculate seconds from start of day to event start (for positioning in day view)
        self.startFromDay: int = self.start - TimeStarts(generationTime=self.start).today["start"]
        # Calculate seconds from start of day to event end (for positioning in day view)
        self.endFromDay: int = self.end - TimeStarts(generationTime=self.end).today["start"]
        # Calculate what percentage of the day this event occupies (for visual representation)
        self.percentOfDay: float = ((self.endFromDay - self.startFromDay) / UnixTimePeriods.day) * 100

class EventSorter:
    """
    Organizes and categorizes events by different time periods.

    This class retrieves events from the database and sorts them into various
    time-based categories (today, this week, floating week, this month) for
    easy access and display. It also separates past and future events.

    Attributes:
        timeStarts (TimeStarts): Time period calculation utility
        allEvents (tuple): All events from database as EventObj objects
        futureEvents (tuple): Events that haven't started yet
        pastEvents (tuple): Events that have already ended
        todayEvents (dict): Events occurring today with timing metadata
        thisWeekEvents (tuple): Events in the current calendar week
        floatingWeekEvents (tuple): Events in a 7-day period from today
        thisMonthEvents (tuple): Events in the current calendar month
    """
    def __init__(self):
        """
        Initialize EventSorter and populate all event categories.

        Automatically retrieves events from database and organizes them
        into various time-based categories for easy access.
        """
        # Initialize time calculation utility for period boundaries
        self.timeStarts = TimeStarts()

        # Initialize event storage containers
        self.allEvents: tuple = ()
        self.futureEvents: tuple = ()
        self.pastEvents: tuple = ()
        # Populate basic event lists from database
        self.assembleEventLists()

        # Initialize time-period specific event containers
        self.todayEvents: dict = {}
        self.thisWeekEvents: tuple = ()
        self.floatingWeekEvents: tuple = ()
        self.thisMonthEvents: tuple = ()
        # Populate time-period specific event lists
        self.assembleTodayEvents()
        self.assembleThisWeekEvents()
        self.assembleFloatingWeekEvents()
        self.assembleThisMonthEvents()

    def _assembleEvents(self, weekStart: int, weekEnd: int, timeStart: tuple) -> tuple:
        week: list[list] = [[] for _ in range(len(timeStart))]

        for event in self.allEvents:
            # removes events not in this week
            if not (weekStart < event.start < weekEnd and event.end < weekEnd):
                continue

            for idx, day in enumerate(timeStart):
                if day["start"] < event.start and event.end < day["end"]:
                    week[idx].append(event)
                    break  # stop checking other days once matched

        weekEvents = []
        for daysEvents in week:
            thatDayEvents = []

            for idx, event in enumerate(daysEvents):
                if len(daysEvents) > 1:
                    if idx == 0:
                        eventDict = {"eventData": event,
                                     "toPreviousEvent": event.startFromDay,
                                     "toNextEvent": daysEvents[idx + 1].start - event.end}
                    elif idx == len(daysEvents) - 1:
                        eventDict = {"eventData": event,
                                     "toPreviousEvent": event.start - daysEvents[idx - 1].end,
                                     "toNextEvent": event.endFromDay}
                    else:
                        eventDict = {"eventData": event,
                                     "toPreviousEvent": event.start - daysEvents[idx - 1].end,
                                     "toNextEvent": daysEvents[idx + 1].start - event.end}

                else:
                    eventDict = {"eventData": event,
                                 "toPreviousEvent": event.startFromDay,
                                 "toNextEvent": event.endFromDay}

                thatDayEvents.append(eventDict)
            weekEvents.append(tuple(thatDayEvents))
        return tuple(weekEvents)

    def assembleEventLists(self):
        """
        Retrieve all events from database and categorize by time status.

        Fetches all events from the database, converts them to EventObj objects,
        and separates them into past, future, and all events categories based
        on current time.

        Returns:
            tuple: (allEvents, futureEvents, pastEvents) - All event categories
        """
        # Connect to database and retrieve all event records
        connector = ConnectDB()
        connector.cursor.execute("SELECT event, description, unixtimeStart, unixtimeEnd FROM events")
        allEvents = connector.cursor.fetchall()

        # Convert database tuples to EventObj objects for easier manipulation
        self.allEvents = tuple(EventObj(item) for item in allEvents)

        # Get current time for comparison
        timeUtil = TimeConverter()

        # Separate events into past and future categories
        past = []
        future = []
        for item in self.allEvents:
            if item.end < timeUtil.currentTime:
                # EventObj has already ended
                past.append(item)
            elif item.start > timeUtil.currentTime:
                # EventObj hasn't started yet
                future.append(item)
            # Note: Events currently in progress are not categorized as past or future

        self.pastEvents = tuple(past)
        self.futureEvents = tuple(future)

        return self.allEvents, self.futureEvents, self.pastEvents

    def assembleTodayEvents(self):
        """
        Organize today's events with timing metadata for display.

        Returns:
            dict: Today's events with spacing and timing information
        """
        dayStart = self.timeStarts.today["start"]
        dayEnd = self.timeStarts.today["end"]

        self.todayEvents = self._assembleEvents(dayStart, dayEnd, (self.timeStarts.today,))[0]
        return self.todayEvents

    def assembleThisWeekEvents(self):
        """
        Organize this calendar week's events by day.

        Returns:
            tuple: Events organized by day for the current calendar week
        """
        weekStart = self.timeStarts.thisWeek["start"]
        weekEnd = self.timeStarts.thisWeek["end"]

        self.thisWeekEvents = self._assembleEvents(weekStart, weekEnd, self.timeStarts.daysOfThisWeek)
        return self.thisWeekEvents

    def assembleFloatingWeekEvents(self):
        """
        Organize floating week's events by day (7 days from today).

        Returns:
            tuple: Events organized by day for a 7-day period starting today
        """
        weekStart = self.timeStarts.floatingWeek["start"]
        weekEnd = self.timeStarts.floatingWeek["end"]

        self.floatingWeekEvents = self._assembleEvents(weekStart, weekEnd, self.timeStarts.daysOfFloatingWeek)
        return self.floatingWeekEvents

    def assembleThisMonthEvents(self):
        """
        Organize this calendar month's events by day.

        Returns:
            tuple: Events organized by day for the current calendar month
        """
        monthStart = self.timeStarts.thisMonth["start"]
        monthEnd = self.timeStarts.thisMonth["end"]

        self.thisMonthEvents = self._assembleEvents(monthStart, monthEnd, self.timeStarts.daysOfMonth)
        return self.thisMonthEvents

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
            #>>> convertListToText(["EventObj 1", "EventObj 2", "EventObj 3"])
            "EventObj 1\nEventObj 2\nEventObj 3"
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

        for item in events:
            daySet = toShortHumanTime(item[2])

            if daySet not in dayCheck:
                # First event for this day - add day header
                dayCheck.append(daySet)
                output.append(f"Events on {daySet}:")
                output.append(f"{item[0]} from {toHumanHour(item[2])} to {toHumanHour(item[3])}")

            else:
                # Additional event for same day - just add event info
                output.append(f"{item[0]} from {toHumanHour(item[2])} to {toHumanHour(item[3])}")

        return output

    @staticmethod
    def createEventJson():
        """
        Generate JSON file containing all event data for web calendar display.

        Creates a comprehensive JSON file with all event information including
        parsed time data, day-relative positioning, and percentage calculations.
        This file is used by the web-based calendar interface for rendering events.

        The JSON file is saved to calendarSite/eventData.json and contains:
        - EventObj ID and description
        - Raw Unix timestamps and parsed time data
        - Day-relative timing for positioning
        - Percentage of day calculations for visual sizing
        """
        # Get all events from database via EventSorter
        allEvents = EventSorter().allEvents

        # Build comprehensive event dictionary for JSON export
        eventDict = {}
        for event in allEvents:
            eventDict.update({event.iD: {
                "iD": event.iD,
                "description": event.description,
                "start": event.start,
                "startParsed": vars(event.startParsed),  # Convert TimeData object to dict
                "end": event.end,
                "endParsed": vars(event.endParsed),      # Convert TimeData object to dict
                "startFromDay": event.startFromDay,      # Seconds from day start
                "endFromDay": event.endFromDay,          # Seconds from day start
                "percentOfDay": event.percentOfDay       # Percentage for visual sizing
            }})

        # Write JSON file to calendar site directory for web interface
        with open(Path(getProjRoot()) / "calendarORGS" / "calendarViews" / "calendarSite" / "eventData.json", "w") as f:
            json.dump(eventDict, f, indent=4)
