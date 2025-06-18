import sqlite3
import time
from utils.timeUtils import timeOut, toShortHumanTime, toHumanHour
from scheduling.calEvent import addEvent, modifyTask

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

def giveTasks():

    conn = sqlite3.connect('calendar.db')
    c = conn.cursor()

    selection = """ SELECT * FROM tasks WHERE scheduled = 0"""

    c.execute(selection)
    tasks = c.fetchall()
    conn.close()
    return tasks

def giveBlocks():

    conn = sqlite3.connect('calendar.db')
    c = conn.cursor()

    selection = """ SELECT * FROM blocks"""

    c.execute(selection)
    blocks = c.fetchall()
    conn.close()
    return blocks

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

def getSchedulingData(timeForecast):
    """
    Retrieves and prepares data needed for scheduling tasks.

    Args:
        timeForecast (str): Time period for scheduling in format "<number> D"

    Returns:
        tuple: (tasks, blocks) where:
            - tasks: List of unscheduled tasks sorted by urgency
            - blocks: Combined list of time blocks and events sorted chronologically
    """
    timeForecastSeconds = timeOut(timeForecast)

    tasks = giveTasks()
    blocks = giveBlocks()
    events = giveEvents(timeForecastSeconds)

    # Sort tasks by urgency
    tasks.sort(key=lambda x: x[2])

    # Combine events with blocks
    for event in events:
        event = list(event)
        # Remove name and description fields
        event.remove(event[0])
        event.remove(event[0])

        event = tuple(event)
        blocks.append(event)

    # Sort blocks chronologically
    blocks.sort(key=lambda x: x[0])

    return tasks, blocks

def findAvailableTimeSlots(blocks):
    """
    Identifies available time slots between blocks.

    Args:
        blocks (list): List of time blocks sorted chronologically

    Returns:
        list: List of available time slots as tuples (duration, (start_time, end_time))
    """
    availableTime = []

    for n in range(len(blocks)):
        if (n != (len(blocks)-1)) and (n != 0):
            # Calculate time between current block end and next block start
            delta = blocks[n+1][0] - blocks[n][1]

            # Create time slot with 5-minute buffers on each end
            timeslot = (delta-600, (blocks[n][1]+300, blocks[n+1][0]-300))
            availableTime.append(timeslot)
        else:
            break

    return availableTime

def assignTasksToSlots(tasks, availableTime):
    """
    Assigns tasks to available time slots.

    Args:
        tasks (list): List of tasks sorted by urgency
        availableTime (list): List of available time slots

    Returns:
        list: List of scheduled tasks
    """
    scheduledTasks = []

    for i in range(len(tasks)):
        for j in range(len(availableTime)):
            if availableTime[j][0] > tasks[i][0]:
                # Fix: Use availableTime[j] instead of availableTime[0]
                addEvent(tasks[i][0], f"Level {tasks[i][1]} urgency", 
                         availableTime[j][1][0], availableTime[j][1][1], True)
                modifyTask(tasks[i][0], tasks[i][1], tasks[i][2], tasks[i][4], True)
                scheduledTasks.append(tasks[i])
                # Remove this time slot from available slots to avoid double booking
                availableTime.pop(j)
                break

    return scheduledTasks

def scheduleTasks(timeForecast):
    """
    Schedules tasks within available time blocks while considering existing events.

    Args:
        timeForecast (str): Time period for scheduling in format "<number> D" 
                          (e.g., "7 D" for 7 days)

    The function:
    1. Converts the time forecast to seconds
    2. Retrieves tasks, time blocks, and events from the database
    3. Sorts tasks by priority/urgency
    4. Combines events with time blocks
    5. Identifies available time slots between blocks
    6. Schedules tasks in available time slots

    Available time slots are calculated with 5-minute buffers (300 seconds) 
    before and after each block, and a minimum 10-minute (600 seconds) gap 
    between blocks is required.

    Returns:
        tuple: A tuple containing:
              - List of available time slots: Each slot is a tuple containing:
                  - Duration of available time (in seconds)
                  - Tuple of (start_time, end_time) in unix timestamp format
              - List of scheduled tasks

    Example:
        #>>> availableTime, scheduledTasks = scheduleTasks("7 D")
        #>>> availableTime
        [(3600, (1,632,567,900, 1,632,571,500)), # Example output
         (1800, (1,632,578,700, 1,632,580,500))]

    Note:
        - Events and blocks are combined and sorted chronologically
        - Time slots less than 10 minutes (600 seconds) are ignored
        - Each slot has 5-minute buffers on both ends for transitions
        - Tasks are scheduled in the database as a side effect
    """
    # Step 1: Get tasks and blocks data
    tasks, blocks = getSchedulingData(timeForecast)

    # Step 2: Find available time slots
    availableTime = findAvailableTimeSlots(blocks)

    # Step 3: Assign tasks to available slots
    scheduledTasks = assignTasksToSlots(tasks, availableTime)

    # Return both available time slots and scheduled tasks
    return availableTime, scheduledTasks
