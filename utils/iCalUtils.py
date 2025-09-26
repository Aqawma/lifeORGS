from datetime import datetime
from icalendar import Calendar, Event
import pytz

from calendarORGS.calendarViews.calendarCreator.calendarView import EventObj

class iCalPackager:
    def __init__(self):
        self.cal = Calendar()
        self.cal.add('prodid', '-//My calendar product//mxm.dk//')
        self.cal.add('version', '2.0')
        self.timezone = pytz.timezone('Asia/Tokyo')

    def packageEvent(self, eventClass: EventObj):
        event = Event()
        event.add('name', eventClass.summary)
        event.add('description', eventClass.description)
        event.add('dtstart', datetime(eventClass.startParsed.year,
                                      eventClass.startParsed.monthNum,
                                      eventClass.startParsed.day,
                                      eventClass.startParsed.hour,
                                      eventClass.startParsed.minute,
                                      0,
                                      tzinfo=self.timezone))
        event.add('dtend', datetime(eventClass.endParsed.year,
                                    eventClass.endParsed.monthNum,
                                    eventClass.endParsed.day,
                                    eventClass.endParsed.hour,
                                    eventClass.endParsed.minute,
                                    0,
                                    tzinfo=self.timezone))
