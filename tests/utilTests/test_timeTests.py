import unittest
from utils.timeUtils import TimeUtility, TimeData, UnixTimePeriods


class TimeUtilityTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_updateCurrentTime(self):
        print("For updateCurrentTime: Expected: oldTime != currentTime")
        timeUtility = TimeUtility()
        oldTime = timeUtility.currentTime
        timeUtility.updateCurrentTime()
        self.assertNotEqual(oldTime, timeUtility.currentTime)

    def test_convertToUTC(self):
        print("For convertToUTC: Input: 09/07/2025 EST-DST Expected: 1703530800.0")
        timeUtility = TimeUtility(intoUnix="09/07/2025 14:00")
        self.assertEqual(timeUtility.convertToUTC(), 1752084000.0)

    def test_generateTimeDataObj(self):
        print("""For generateTimeDataObj: Input: 175208400\n Output:\n
        monthName=July\n
        dayOfWeek=Wednesday\n
        day=9\n
        hour=14\n
        minute=0\n
        second=0\n
        dayNumInWeek=3\n
        year=2025\n
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
        timeUtility = TimeUtility(unixTimeUTC=1752084000.0)
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