import sqlite3
import time
from utils.pyUtils import timeOut

def viewEvents(timeForecast):

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
