import json
import unittest
from datetime import datetime

from utils.timeUtilitities.startAndEndBlocks import TimeStarts
from utils.timeUtilitities.timeDataClasses import UnixTimePeriods
from utils.timeUtilitities.timeUtil import TimeConverter, TimeData, TokenizeToDatetime

class tokenizeToDatetimeTests(unittest.TestCase):
    def test_tokenizeToDatetime(self):
        tokenizedDatetime = TokenizeToDatetime("09/07/2025 14:00")
        datetimeObj = datetime(2025, 7, 9, 14, 0)
        self.assertEqual(tokenizedDatetime.datetimeObj, datetimeObj)

class TimeUtilityTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_updateCurrentTime(self):
        print("For updateCurrentTime: Expected: oldTime != currentTime")
        timeUtility = TimeConverter()
        oldTime = timeUtility.currentTime
        timeUtility.updateCurrentTime()
        self.assertNotEqual(oldTime, timeUtility.currentTime)

    def test_convertToUTC(self):
        print("For convertToUTC: Input: 09/07/2025 14:00 [EST-DST] Expected: 1703530800.0")
        timeUtility = TimeConverter(intoUnix="09/07/2025 14:00")
        self.assertEqual(timeUtility.convertToUTC(), 1752084000.0)

    def test_generateTimeDataObj(self):
        print("""For generateTimeDataObj: Input: 175208400\n Expected:\n
        monthName=July
        dayOfWeek=Wednesday
        day=9
        hour=14
        minute=0
        second=0
        dayNumInWeek=3
        year=2025
        unixTimeUTC=1752084000.0""")

        timeDataObj = TimeData(monthNum=7,
                               monthName="July",
                               dayOfWeek="Wednesday",
                               day=9,
                               hour=14,
                               minute=0,
                               second=0,
                               dayNumInWeek=3,
                               year=2025,
                               unixTimeUTC=1752084000.0)
        timeUtility = TimeConverter(unixTimeUTC=1752084000.0)
        timeUtility.generateTimeDataObj()
        self.assertEqual(timeUtility.datetimeObj, timeDataObj)

class UnixTimePeriodsTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timePeriods = UnixTimePeriods()

    def test_minute(self):
        print("Expected: 60")
        self.assertEqual(self.timePeriods.minute, 60)

    def test_hour(self):
        print("Expected: 3600")
        self.assertEqual(self.timePeriods.hour, 3600)

    def test_day(self):
        print("Expected: 86400")
        self.assertEqual(self.timePeriods.day, 86400)

    def test_week(self):
        print("Expected: 604800")
        self.assertEqual(self.timePeriods.week, 604800)

class TimeStartsTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        with open("TimeStartsTuples.json", "r") as file:
            self.timeStartsTuples = json.load(file)

    def test_timeStarts31dMiddle(self):
        print("""For timeStarts31dMiddleLens: Input: Unix timestamp 1752595200.0 (Tuesday, July 15, 2025 12:00:00)
        Expected:
        - daysOfMonth: 31 days tuple (July 1-31, 2025)
        - daysOfThisWeek: 7 days tuple (Monday July 14 - Sunday July 20, 2025) 
        - daysOfFloatingWeek: 7 days tuple (Tuesday July 15 - Monday July 21, 2025)
        - today: Dictionary with start/end for Tuesday July 15, 2025 (00:00-23:59)""")

        starts = TimeStarts(1752595200.0)
        self.assertEqual(starts.daysOfMonth, tuple(self.timeStartsTuples["31dMiddleMonth"]))
        self.assertEqual(starts.daysOfThisWeek, tuple(self.timeStartsTuples["31dMiddleThisWeek"]))
        self.assertEqual(starts.daysOfFloatingWeek, tuple(self.timeStartsTuples["31dMiddleFloatWeek"]))
        self.assertEqual(starts.today, self.timeStartsTuples["31dMiddleToday"])

    def test_timeStarts31dEnd(self):
        print("""For timeStarts31dEnd: Input: Unix timestamp 1753977600.0 (Thursday, July 31, 2025 12:00:00)
        Expected:
        - daysOfMonth: 31 days tuple (July 1-31, 2025) - same as middle test since same month
        - daysOfThisWeek: 7 days tuple (Monday July 28 - Sunday August 3, 2025) - week containing July 31st
        - daysOfFloatingWeek: 7 days tuple (Thursday July 31 - Wednesday August 6, 2025) - starting from July 31st
        - today: Dictionary with start/end for Thursday July 31, 2025 (00:00-23:59)
        
        Note: This tests the last day of July 2025, showing how week calculations work at month boundaries""")

        starts = TimeStarts(1753977600.0)
        self.assertEqual(starts.daysOfMonth, tuple(self.timeStartsTuples["31dEndMonth"]))
        self.assertEqual(starts.daysOfThisWeek, tuple(self.timeStartsTuples["31dEndThisWeek"]))
        self.assertEqual(starts.daysOfFloatingWeek, tuple(self.timeStartsTuples["31dEndFloatWeek"]))

    def test_timeStarts31dStart(self):
        print("""For timeStarts31dStart: Input: Unix timestamp 1751385600.0 (Monday, July 1, 2025 12:00:00)
        Expected:
        - daysOfMonth: 31 days tuple (July 1-31, 2025) - same as middle test since same month
        - daysOfThisWeek: 7 days tuple (Monday July 14 - Sunday July 20, 2025) - week containing July 1st
        - daysOfFloatingWeek: 7 days tuple (Monday July 1 - Sunday July 7, 2025) - starting from July 1st
        - today: Dictionary with start/end for Monday July 1, 2025 (00:00-23:59)
        
        Note: This tests the first day of July 2025, showing how week calculations work at month boundaries""")
        starts = TimeStarts(1751385600.0)
        self.assertEqual(starts.daysOfMonth, tuple(self.timeStartsTuples["31dStartMonth"]))
        self.assertEqual(starts.daysOfThisWeek, tuple(self.timeStartsTuples["31dStartThisWeek"]))
        self.assertEqual(starts.daysOfFloatingWeek, tuple(self.timeStartsTuples["31dStartFloatWeek"]))

    def test_timeStarts28dStart(self):
        print("""For timeStarts28dStart: Input: Unix timestamp 1738429200.0 (Thursday, February 1, 2025 12:00:00)
        Expected:
        - daysOfMonth: 28 days tuple (February 1-28, 2025) - Non-leap year February
        - daysOfThisWeek: 7 days tuple (Monday January 27 - Sunday February 2, 2025) - Week containing Feb 1st
        - daysOfFloatingWeek: 7 days tuple (Thursday February 1 - Wednesday February 7, 2025) - Starting from Feb 1st
        
        Note: This tests the start of a 28-day February in a non-leap year (2025)""")

        starts = TimeStarts(1738429200.0)
        self.assertEqual(starts.daysOfMonth, tuple(self.timeStartsTuples["28dStartMonth"]))
        self.assertEqual(starts.daysOfThisWeek, tuple(self.timeStartsTuples["28dStartThisWeek"]))
        self.assertEqual(starts.daysOfFloatingWeek, tuple(self.timeStartsTuples["28dStartFloatWeek"]))

    def test_timeStarts28dEnd(self):
        print("""For timeStarts28dEnd: Input: Unix timestamp 1740762000.0 (Friday, February 28, 2025 12:00:00)
        Expected:
        - daysOfMonth: 28 days tuple (February 1-28, 2025) - Same month as start test
        - daysOfThisWeek: 7 days tuple (Monday February 24 - Sunday March 2, 2025) - Week containing Feb 28th
        - daysOfFloatingWeek: 7 days tuple (Friday February 28 - Thursday March 6, 2025) - Starting from Feb 28th
        
        Note: This tests the last day of February in a non-leap year, showing month boundary handling""")

        starts = TimeStarts(1740762000.0)
        self.assertEqual(starts.daysOfMonth, tuple(self.timeStartsTuples["28dEndMonth"]))
        self.assertEqual(starts.daysOfThisWeek, tuple(self.timeStartsTuples["28dEndThisWeek"]))
        self.assertEqual(starts.daysOfFloatingWeek, tuple(self.timeStartsTuples["28dEndFloatWeek"]))

    def test_timeStarts29dEnd(self):
        print("""For timeStarts29dEnd: Input: Unix timestamp 1709139600.0 (Thursday, February 29, 2024 12:00:00)
        Expected:
        - daysOfMonth: 29 days tuple (February 1-29, 2024) - Leap year February
        - daysOfThisWeek: 7 days tuple (Monday February 26 - Sunday March 3, 2024) - Week containing Feb 29th
        - daysOfFloatingWeek: 7 days tuple (Thursday February 29 - Wednesday March 6, 2024) - Starting from leap day
        
        Note: This tests leap day (February 29th) in a leap year (2024), validating leap year handling""")

        starts = TimeStarts(1709139600.0)
        self.assertEqual(starts.daysOfMonth, tuple(self.timeStartsTuples["29dEndMonth"]))
        self.assertEqual(starts.daysOfThisWeek, tuple(self.timeStartsTuples["29dEndThisWeek"]))
        self.assertEqual(starts.daysOfFloatingWeek, tuple(self.timeStartsTuples["29dEndFloatWeek"]))

    def test_timeStarts30dEnd(self):
        print("""For timeStarts30dEnd: Input: Unix timestamp 1714492800.0 (Wednesday, April 30, 2025 12:00:00)
        Expected:
        - daysOfMonth: 30 days tuple (April 1-30, 2025) - Month with 30 days
        - daysOfThisWeek: 7 days tuple (Monday April 28 - Sunday May 4, 2025) - Week containing April 30th
        - daysOfFloatingWeek: 7 days tuple (Wednesday April 30 - Tuesday May 6, 2025) - Starting from April 30th
        
        Note: This tests the last day of April (30-day month), showing 30-day month boundary handling""")

        starts = TimeStarts(1714492800.0)
        self.assertEqual(starts.daysOfMonth, tuple(self.timeStartsTuples["30dEndMonth"]))
        self.assertEqual(starts.daysOfThisWeek, tuple(self.timeStartsTuples["30dEndThisWeek"]))
        self.assertEqual(starts.daysOfFloatingWeek, tuple(self.timeStartsTuples["30dEndFloatWeek"]))
