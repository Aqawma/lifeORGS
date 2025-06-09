import datetime
#28/04/2000 15:00 956948400
def toUnixTime(date, time):

    date = date.split('/')
    time = time.split(':')

    dt = datetime.datetime(int(date[2]), int(date[1]), int(date[0]), int(time[0]), int(time[1]))
    res = dt.timestamp()

    return res

def toSeconds(time):

    time = time.split(':')
    combinedTime = int(time[0])*3600 + int(time[1])*60
    if len(time) == 3:
        combinedTime += int(time[2])
    return combinedTime


