import sqlite3
import time
from utils.timeUtils import timeOut, toShortHumanTime, toHumanHour, deltaToStartOfWeek
from utils.dbUtils import getDBPath

def giveEvents(timeForecast):
    """
    Retrieves events from the calendar database within a specified time period.

    Args:
        timeForecast (str): Time period to look ahead in format "<number> D"
                           (e.g., "7 D" for 7 days)

    Returns:
        list: List of events where each event is a tuple containing event details
              (name, description, start_time, end_time)
    """
    currentTime = int(round(time.time(), 0))
    timeForecast = timeOut(timeForecast)

    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()

    selection = """SELECT * FROM events WHERE unixtimeEnd > ? AND unixtimeStart < ?"""

    c.execute(selection, (currentTime, currentTime + timeForecast))
    events = c.fetchall()

    conn.close()

    return events

def giveTasks():
    """
    Retrieves all unscheduled tasks from the calendar database.

    Returns:
        list: List of unscheduled tasks where each task is a tuple containing task details
              (name, description, urgency, due_date, scheduled_status)
    """
    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()

    selection = """ SELECT * FROM tasks WHERE scheduled = 0"""

    c.execute(selection)
    tasks = c.fetchall()
    conn.close()
    return tasks

def giveBlocks():
    """
    Retrieves all time blocks from the calendar database.

    Time blocks represent recurring periods when events can be scheduled
    (e.g., working hours, study time, etc.).

    Returns:
        list: List of time blocks where each block is a tuple containing block details
              (start_time, end_time, day_of_week)
    """
    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()

    selection = """ SELECT * FROM blocks"""

    c.execute(selection)
    blocks = c.fetchall()
    conn.close()
    return blocks

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

    tasks = giveTasks()
    tupleBlocks = giveBlocks()
    events = giveEvents(timeForecast)

    currentTime = int(round(time.time(), 0))
    weekSecDelta = deltaToStartOfWeek(currentTime)
    startOfWeek = currentTime - weekSecDelta


    for block in tupleBlocks:
        if block[1] < weekSecDelta:
            tupleBlocks.remove(block)

    blocks = []

    for tupleBlock in tupleBlocks:
        block = list(tupleBlock)
        block[0] = block[0] + startOfWeek
        block[1] = block[1] + startOfWeek
        blocks.append(block)

    # Sort tasks by urgency
    tasks.sort(key=lambda x: x[2])

    # Combine events with blocks
    for event in events:
        event = list(event)
        # Remove name and description fields
        event.remove(event[0])
        event.remove(event[0])
        event.remove(event[2])
        event.remove(event[2])

        blocks.append(event)

    # Sort blocks chronologically
    blocks.sort(key=lambda x: x[0])

    return tasks, blocks \

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
        if (n != (len(blocks)-1)) and (n != 0):  # TODO this is broken for the first block and last(?)
            # Calculate time between current block end and next block start
            delta = blocks[n+1][0] - blocks[n][1]
            if delta > 600:
                # Create time slot with 5-minute buffers on each end
                timeslot = [delta-600, [blocks[n][1]+300, blocks[n+1][0]-300]]
                availableTime.append(timeslot)
        else:
            continue

    return availableTime

def assignTasksToSlots(tasks, availableTime):
    """
    Assigns tasks to available time slots based on task urgency and time slot availability.

    The function iterates through tasks (sorted by urgency) and available time slots,
    scheduling each task in the first available slot that has enough time for the task.
    When a task is scheduled, the time slot is removed from the available slots to prevent
    double booking.

    Args:
        tasks (list): List of tasks sorted by urgency. Each task is a tuple containing:
                     - [0]: Duration needed for the task (in seconds)
                     - [1]: Priority level
                     - [2]: Urgency value
                     - [4]: Task ID or identifier
        availableTime (list): List of available time slots. Each slot is a tuple containing:
                             - [0]: Duration of the slot (in seconds)
                             - [1]: Tuple of (start_time, end_time) in unix timestamp format

    Side Effects:
        - Adds events to the calendar database for each scheduled task
        - Modifies task status in the database to mark them as scheduled

    Returns:
        list: List of scheduled tasks that were successfully assigned to time slots
    """
    scheduledTasks = []

    conn = sqlite3.connect(getDBPath())

    for i in range(len(tasks)):
        for j in range(len(availableTime)):

            if availableTime[j][0] > tasks[i][1]:

                taskStart = availableTime[j][1][0]
                taskEnd = availableTime[j][1][0] + tasks[i][1]

                conn.execute("INSERT INTO events VALUES (?,?,?,?,?,?)",
                             (tasks[i][0],
                              f"""Due on {toShortHumanTime(tasks[i][4])} at {toHumanHour(tasks[i][4])}. 
                              Level {tasks[i][2]} urgency""",
                              taskStart,
                              taskEnd,
                              1, 0,))
                conn.execute("UPDATE tasks SET scheduled = 1 WHERE task=?", (tasks[i][0],))

                scheduledTasks.append(tasks[i])
                # Remove this time slot from available slots to avoid double booking
                availableTime[j][1][0] = availableTime[j][1][0] + tasks[i][1] + 300
                break

    conn.commit()
    conn.close()

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
