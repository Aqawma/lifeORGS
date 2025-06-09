import sqlite3
import time
from utils.timeUtils import timeOut, toShortHumanTime, toHumanHour


def giveEvents(timeForecast):

    currentTime = time.time()
    timeForecast = timeOut(timeForecast)

    conn = sqlite3.connect('calendar.db')
    c = conn.cursor()

    selection = """ SELECT * FROM events WHERE unixtimeEnd > ? AND unixtimeStart < ?
    """

    c.execute(selection, (currentTime, currentTime + timeForecast))
    events = c.fetchall()

    conn.close()

    return events

def viewEvents(timeForecast):

    events = giveEvents(timeForecast)
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
