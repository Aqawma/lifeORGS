from datetime import datetime

def toUnixTime(eventTime):
    # Split the date and time parts
    parts = eventTime.split(" ")
    date = parts[0].split("/")
    time = parts[1].split(":")

    # Create datetime object
    dt = datetime(int(date[2]), int(date[1]), int(date[0]), int(time[0]), int(time[1]))
    return dt.timestamp()

def toSeconds(time):
    time = time.split(':')
    combinedTime = int(time[0])*3600 + int(time[1])*60
    if len(time) == 3:
        combinedTime += int(time[2])
    return combinedTime

def timeOut(timeString):

    time = timeString.split(" ")

    if time[1] == "D":
        timeString = int(time[0]) * 86400
        return timeString

    else:
        #TODO Make this logic better
        raise Exception("Invalid time format")

def toShortHumanTime(unixTime):

    realTime = datetime.fromtimestamp(unixTime).strftime('%A, %B %d')

    return realTime

def toHumanHour(unixTime):

    realTime = datetime.fromtimestamp(unixTime).strftime('%I:%M %p')

    return realTime

print(toHumanHour(1749495600))