from utils.timeUtilitities.timeUtil import TimeUtility
from utils.timeUtilitities.timeDataClasses import UnixTimePeriods

class TimeStarts:
    """
    Utility class for generating time period boundaries and day collections.

    This class provides convenient methods for calculating time boundaries for
    common periods like today, this week, this month, and generating collections
    of all days in the current month. It's designed to support calendar and
    scheduling operations that need standardized time ranges.

    Attributes:
        currentTime (float): Current Unix timestamp in user's timezone
        today (dict): Dictionary with 'start' and 'end' Unix timestamps for today
        thisWeek (dict): Dictionary with 'start' and 'end' Unix timestamps for this week
        thisMonth (dict): Dictionary with 'start' and 'end' Unix timestamps for this month
        daysOfMonth (tuple): Tuple of dictionaries, each containing 'start' and 'end'
                            timestamps for each day in the current month

    Example:
        # >>> time_starts = TimeStarts()
        # >>> time_starts.setToday()
        # >>> print(time_starts.today)
        {'start': 1703462400.0, 'end': 1703548740.0}
    """

    def __init__(self, generationTime=None):
        """
        Initialize TimeStarts with current time in user's timezone.

        Sets up the current time and initializes empty containers for
        time period boundaries that will be populated by the setter methods.
        """
        # Get current time in user's configured timezone
        self.currentTime: float = TimeUtility().currentTime if generationTime is None else generationTime

        # Initialize empty time period containers
        self.today: dict = {}
        self.thisWeek: dict = {}
        self.floatingWeek: dict = {}
        self.daysOfFloatingWeek: tuple = ()
        self.daysOfThisWeek: tuple = ()
        self.thisMonth: dict = {}
        self.daysOfMonth: tuple = ()

        self.dayPointerWeek = TimeUtility(unixTimeUTC=self.currentTime).generateTimeDataObj().dayNumInWeek - 1
        self.dayPointerMonth = TimeUtility(unixTimeUTC=self.currentTime).generateTimeDataObj().day - 1

        self.setToday()
        self.setThisWeek()
        self.setDaysOfThisWeek()
        self.setFloatingWeek()
        self.setDaysOfFloatingWeek()
        self.setThisMonth()
        self.setDaysOfMonth()

    def setToday(self):
        """
        Sets the time boundaries for the current day (00:00 to 23:59).

        Calculates the start (00:00:00) and end (23:59:00) timestamps for
        the current day and stores them in the today attribute.

        Updates:
            self.today: Dictionary with 'start' and 'end' Unix timestamps
        """
        # Generate time data object from current time
        timeUtil = TimeUtility(unixTimeUTC=self.currentTime)
        timeUtil.generateTimeDataObj()
        dateTimeObj = timeUtil.datetimeObj

        # Calculate start of day (00:00:00)
        startUnix = TimeUtility(f"{dateTimeObj.day}/{dateTimeObj.monthNum}/{dateTimeObj.year} 00:00").convertToUTC()

        # Calculate end of day (23:59:00)
        endUnix = TimeUtility(f"{dateTimeObj.day}/{dateTimeObj.monthNum}/{dateTimeObj.year} 23:59").convertToUTC()

        # Store the day boundaries
        self.today = {"start": startUnix, "end": endUnix}
        return self.today

    def setThisWeek(self):
        """
        Sets the time boundaries for the current week (Monday 00:00 to Sunday 23:59).

        Calculates the start of the week (Monday 00:00:00) and end of the week
        (Sunday 23:59:00) based on the current date and stores them in the
        thisWeek attribute.

        Updates:
            self.thisWeek: Dictionary with 'start' and 'end' Unix timestamps

        Note:
            Week starts on Monday (ISO 8601 standard)
        """
        # Generate time data object from current time
        timeUtil = TimeUtility(unixTimeUTC=self.currentTime)
        timeUtil.generateTimeDataObj()
        dateTimeObj = timeUtil.datetimeObj

        # Calculate start of week by going back to Monday
        weekStartDay = dateTimeObj.unixTimeUTC - (UnixTimePeriods.day * (dateTimeObj.dayNumInWeek - 1))
        weekEndDay = weekStartDay + (UnixTimePeriods.day * 6)

        weekStartObj = TimeUtility(unixTimeUTC=weekStartDay)
        weekStartObj.generateTimeDataObj()
        weekStartUnix = TimeUtility(intoUnix=f"{weekStartObj.datetimeObj.day}/"
                                             f"{weekStartObj.datetimeObj.monthNum}/"
                                             f"{weekStartObj.datetimeObj.year} 00:00").convertToUTC()
        weekEndObj = TimeUtility(unixTimeUTC=weekEndDay)
        weekEndObj.generateTimeDataObj()
        weekEndUnix = TimeUtility(intoUnix=f"{weekEndObj.datetimeObj.day}/"
                                           f"{weekEndObj.datetimeObj.monthNum}/"
                                           f"{weekEndObj.datetimeObj.year} 23:59").convertToUTC()

        # Store the week boundaries
        self.thisWeek = {"start": weekStartUnix, "end": weekEndUnix}
        return self.thisWeek

    def setDaysOfThisWeek(self):
        """
        Generates a collection of all days in the current week with their time boundaries.

        Creates a tuple containing dictionaries for each day of the current week,
        where each dictionary has 'start' (00:00:00) and 'end' (23:59:00) timestamps
        for that specific day. The week runs from Monday to Sunday.

        Updates:
            self.daysOfThisWeek: Tuple of dictionaries, each containing day boundaries

        Returns:
            tuple: Collection of day boundary dictionaries for the current week

        Example:
            # >>> time_starts = TimeStarts()
            # >>> days = time_starts.setDaysOfThisWeek()
            # >>> print(len(days))  # Always 7 days in a week
            7
        """
        self.setThisWeek()

        counter = 0
        startEndList = []
        breaker = True
        while breaker:

            startEndDict = {"start": (self.thisWeek["start"] + (UnixTimePeriods.day * counter)),
                            "end": (self.thisWeek["start"] +
                                    (UnixTimePeriods.day * (counter + 1)) - UnixTimePeriods.minute)}

            if startEndDict["end"] > self.thisWeek["end"]:
                breaker = False
            else:
                startEndList.append(startEndDict)
                counter += 1

        self.daysOfThisWeek = tuple(startEndList)
        return self.daysOfThisWeek

    def setFloatingWeek(self):
        """
        Sets the time boundaries for a floating week starting from today.

        Creates a 7-day period that starts from the beginning of today (00:00:00)
        and extends for 6 additional days, providing a week-long window that
        "floats" with the current date rather than being fixed to calendar weeks.

        Updates:
            self.floatingWeek: Dictionary with 'start' and 'end' Unix timestamps

        Returns:
            dict: Dictionary containing start and end timestamps for the floating week

        Example:
            # >>> time_starts = TimeStarts()
            # >>> floating = time_starts.setFloatingWeek()
            # >>> # floating['start'] is today at 00:00:00
            # >>> # floating['end'] is 6 days from today at 23:59:00
        """
        self.setToday()

        floatingStart = self.today["start"]
        floatingEnd = self.today["end"] + UnixTimePeriods.day * 6

        self.floatingWeek = {"start": floatingStart, "end": floatingEnd}
        return self.floatingWeek

    def setDaysOfFloatingWeek(self):
        """
        Generates a collection of all days in the floating week with their time boundaries.

        Creates a tuple containing dictionaries for each day of the floating week,
        where each dictionary has 'start' (00:00:00) and 'end' (23:59:00) timestamps
        for that specific day. The floating week starts from today and extends for 7 days.

        Updates:
            self.daysOfFloatingWeek: Tuple of dictionaries, each containing day boundaries

        Returns:
            tuple: Collection of day boundary dictionaries for the floating week

        Example:
            # >>> time_starts = TimeStarts()
            # >>> days = time_starts.setDaysOfFloatingWeek()
            # >>> print(len(days))  # Always 7 days
            7
            # >>> # First day starts today at 00:00:00
            # >>> # Last day ends 6 days from today at 23:59:00
        """
        self.setFloatingWeek()

        counter = 0
        startEndList = []
        breaker = True
        while breaker:
            startEndDict = {"start": (self.floatingWeek["start"] + (UnixTimePeriods.day * counter)),
                            "end": (self.floatingWeek["start"] +
                                    (UnixTimePeriods.day * (counter + 1)) - UnixTimePeriods.minute)}
            if startEndDict["end"] > self.floatingWeek["end"]:
                breaker = False
            else:
                startEndList.append(startEndDict)
                counter += 1

        self.daysOfFloatingWeek = tuple(startEndList)
        return self.daysOfFloatingWeek

    def setThisMonth(self):
        """
        Sets the time boundaries for the current month (1st 00:00 to last day 23:59).

        Calculates the start of the month (1st day 00:00:00) and end of the month
        (last day 23:59:00) and stores them in the thisMonth attribute.

        Updates:
            self.thisMonth: Dictionary with 'start' and 'end' Unix timestamps

        Note:
            Handles month transitions and year boundaries correctly
        """
        # Generate time data object from current time
        timeUtil = TimeUtility(unixTimeUTC=self.currentTime)
        timeUtil.generateTimeDataObj()
        dateTimeObj = timeUtil.datetimeObj

        # Set to first day of current month
        dateTimeObj.day = 1
        startUnix = TimeUtility(f"{dateTimeObj.day}/{dateTimeObj.monthNum}/{dateTimeObj.year} 00:00").convertToUTC()

        # Calculate next month, handling year transition
        nextMonth = dateTimeObj.monthNum + 1
        if nextMonth > 12:
            nextMonth = 1  # January of next year

        # Get the last second of current month by going to start of next month and subtracting 60 seconds
        tempEndString = (TimeUtility(f"{dateTimeObj.day}/{nextMonth}/{dateTimeObj.year} 00:00")
                         .convertToUTC() - 60)

        # Convert back to get the actual last day of current month
        tempEndObj = TimeUtility(unixTimeUTC=tempEndString)
        tempEndObj.generateTimeDataObj()
        endObj = tempEndObj.datetimeObj

        # Set end time to 23:59 of the last day of current month
        endUnix = TimeUtility(f"{endObj.day}/{endObj.monthNum}/{endObj.year} 23:59").convertToUTC()

        # Store the month boundaries
        self.thisMonth = {"start": startUnix, "end": endUnix}
        return self.thisMonth

    def setDaysOfMonth(self):
        self.setThisMonth()

        counter = 0
        startEndList = []
        breaker = True
        while breaker:
            startEndDict = {"start": (self.thisMonth["start"] + (UnixTimePeriods.day * counter)),
                            "end": (self.thisMonth["start"] +
                                    (UnixTimePeriods.day * (counter + 1)) - UnixTimePeriods.minute)}
            if startEndDict["end"] > self.thisMonth["end"]:
                breaker = False
            else:
                startEndList.append(startEndDict)
                counter += 1

        self.daysOfMonth = tuple(startEndList)
        return self.daysOfMonth
