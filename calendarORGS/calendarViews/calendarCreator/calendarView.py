"""
Calendar View Module

This module provides functionality for displaying and formatting calendar events
in a human-readable format. It handles the presentation layer for calendar data,
organizing events by date and time for user-friendly display.

The module works with the event scheduler to retrieve event data and formats it
for console output or other display purposes.
"""

from calendarORGS.scheduling.eventScheduler import Scheduler
from utils.dbUtils import ConnectDB
from utils.timeUtilitities.timeDataClasses import UnixTimePeriods
from utils.timeUtilitities.timeUtil import toShortHumanTime, toHumanHour, TimeConverter, TimeData
from utils.timeUtilitities.startAndEndBlocks import TimeStarts

class Event:
    def __init__(self, eventTuple: tuple):
        self.iD: str = eventTuple[0]
        self.description: str = eventTuple[1]
        self.start: int = eventTuple[2]
        self.startParsed: TimeData = TimeConverter(unixTimeUTC=eventTuple[2]).generateTimeDataObj()
        self.end: int = eventTuple[3]
        self.endParsed: TimeData = TimeConverter(unixTimeUTC=eventTuple[3]).generateTimeDataObj()
        self.startFromDay: int = self.start - TimeStarts(generationTime=self.start).today["start"]
        self.endFromDay: int = self.end - TimeStarts(generationTime=self.end).today["start"]
        self.percentOfDay: float = ((self.endFromDay - self.startFromDay) / UnixTimePeriods.day) * 100

class EventSorter:
    def __init__(self):
        self.timeStarts = TimeStarts()

        self.allEvents: tuple = ()
        self.futureEvents: tuple = ()
        self.pastEvents: tuple = ()
        self.assembleEventLists()

        self.todayEvents: dict = {}
        self.thisWeekEvents: tuple = ()
        self.floatingWeekEvents: tuple = ()
        self.thisMonthEvents: tuple = ()
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
        connector = ConnectDB()
        connector.cursor.execute("SELECT event, description, unixtimeStart, unixtimeEnd FROM events")
        allEvents = connector.cursor.fetchall()

        self.allEvents = tuple(Event(item) for item in allEvents)

        timeUtil = TimeConverter()

        past = []
        future = []
        for item in self.allEvents:
            if item.end < timeUtil.currentTime:
                past.append(item)
            elif item.start > timeUtil.currentTime:
                future.append(item)

        self.pastEvents = tuple(past)
        self.futureEvents = tuple(future)

        return self.allEvents, self.futureEvents, self.pastEvents

    def assembleTodayEvents(self):
        dayStart = self.timeStarts.today["start"]
        dayEnd = self.timeStarts.today["end"]

        self.todayEvents = self._assembleEvents(dayStart, dayEnd, (self.timeStarts.today,))[0]
        return self.todayEvents


    def assembleThisWeekEvents(self):
        weekStart = self.timeStarts.thisWeek["start"]
        weekEnd = self.timeStarts.thisWeek["end"]

        self.thisWeekEvents = self._assembleEvents(weekStart, weekEnd, self.timeStarts.daysOfThisWeek)
        return self.thisWeekEvents

    def assembleFloatingWeekEvents(self):

        weekStart = self.timeStarts.floatingWeek["start"]
        weekEnd = self.timeStarts.floatingWeek["end"]

        self.floatingWeekEvents = self._assembleEvents(weekStart, weekEnd, self.timeStarts.daysOfFloatingWeek)
        return self.floatingWeekEvents

    def assembleThisMonthEvents(self):
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
            #>>> convertListToText(["Event 1", "Event 2", "Event 3"])
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

        for item in events:
            daySet = toShortHumanTime(item[2])

            if daySet not in dayCheck:
                dayCheck.append(daySet)
                output.append(f"Events on {daySet}:")
                output.append(f"{item[0]} from {toHumanHour(item[2])} to {toHumanHour(item[3])}")

            else:
                toHumanHour(item[2])
                output.append(f"{item[0]} from {toHumanHour(item[2])} to {toHumanHour(item[3])}")

        return output

