from scheduling.eventScheduler import Scheduler
from utils.timeUtils import toShortHumanTime, toHumanHour


class CalendarView:

    @staticmethod
    def _convertListToText(lists):
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