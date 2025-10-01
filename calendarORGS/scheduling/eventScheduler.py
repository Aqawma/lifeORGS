"""
Calendar Functions Module

This module provides high-level functions for calendar operations including viewing events,
scheduling tasks, and managing time blocks. It serves as the main interface for calendar
functionality, coordinating between the database layer and user interface.

Key Features:
- EventObj retrieval and formatting for display
- Task scheduling algorithm that finds available time slots
- Time block management for recurring availability periods
- Integration between events, tasks, and time blocks

The module implements an intelligent scheduling system that:
1. Retrieves unscheduled tasks and available time blocks
2. Combines existing events with time blocks to find free periods
3. Assigns tasks to available time slots based on urgency and duration
4. Automatically creates calendar events for scheduled tasks

Dependencies:
- sqlite3: For database operations
- time: For current time operations
- utils.timeUtils: Time conversion and formatting utilities
- utils.dbUtils: Database path management
"""
import time

from utils.dbUtils import ConnectDB
from utils.timeUtilitities.timeUtil import timeOut, toShortHumanTime, toHumanHour, deltaToStartOfWeek


class Scheduler:
    """
    Task scheduling and calendar management class.

    This class provides static methods for intelligent task scheduling, event retrieval,
    and calendar operations. It implements a sophisticated priority-based scheduling
    algorithm that considers task urgency, due dates, and duration to optimize task
    placement in available time slots.

    The scheduler integrates with the database to:
    - Retrieve unscheduled tasks and existing events
    - Calculate priority scores for optimal task ordering
    - Find available time slots between existing commitments
    - Automatically create calendar events for scheduled tasks

    All methods are static as the class serves as a utility namespace rather than
    maintaining instance state.
    """

    @staticmethod
    def _calculatePriorityScore(task):
        """
        Calculate a priority score for task scheduling based on urgency, due date, and duration.

        This method implements a sophisticated scoring algorithm that considers multiple factors:
        1. Time until due date (more urgent as deadline approaches)
        2. Task urgency level (1-5 scale, user-defined importance)
        3. Task duration (shorter tasks get slight priority for easier scheduling)

        The algorithm also automatically increases urgency for overdue tasks based on
        how long they've been overdue.

        Args:
            task (dict): Task dictionary containing:
                - 'dueDate' (float): Unix timestamp of task due date
                - 'urgency' (int): User-defined urgency level (1-5)
                - 'taskTime' (int): Estimated task duration in seconds

        Returns:
            float: Calculated priority score (higher scores = higher priority)
                  Range typically 0-100, with overdue urgent tasks scoring highest

        Priority Score Components:
            - Due date urgency: 0-35 points (35 for due within 24 hours, decreasing over time)
            - User urgency level: 0-50 points (10 points per urgency level)
            - Duration bonus: 0-15 points (shorter tasks get slight preference)

        Overdue Task Handling:
            - 1 day overdue: +1 urgency level
            - 2 days overdue: +2 urgency levels
            - 3 days overdue: +3 urgency levels
            - 4+ days overdue: maximum urgency (5)
        """

        timeDueDelta = task['dueDate'] - time.time()
        priorityScore = 0.0

        if timeDueDelta < 0:
            if timeDueDelta >= -86400 and (task['urgency'] + 1 <= 5):
                task['urgency'] += 1
            elif timeDueDelta >= -172800 and (task['urgency'] + 2 <= 5):
                task['urgency'] += 2
            elif timeDueDelta >= -259200 and (task['urgency'] + 3 <= 5):
                task['urgency'] += 3
            elif timeDueDelta >= -345600 and (task['urgency'] + 4 <= 5):
                task['urgency'] += 4
            else:
                task['urgency'] = 5

        match timeDueDelta:
            case x if x <= 86400:
                priorityScore += 35

            case x if x <= 172800:
                priorityScore += (30 - (70 / 8))

            case x if x <= 259200:
                priorityScore += (30 - (105 / 8))

            case x if x <= 345600:
                priorityScore += (30 - (140 / 8))

            case x if x <= 432000:
                priorityScore += (30 - (175 / 8))

            case x if x <= 518400:
                priorityScore += (30 - (210 / 8))

            case x if x <= 604800:
                priorityScore += (30 - (245 / 8))

            case x if x > 604800:
                priorityScore += 0

        match task['urgency']:
            case 1:
                priorityScore += 0

            case 2:
                priorityScore += 12.5

            case 3:
                priorityScore += 25

            case 4:
                priorityScore += 37.5

            case 5:
                priorityScore += 50

        match task['taskTime']:
            case x if x <= 300:
                priorityScore += 15

            case x if x <= 900:
                priorityScore += 12

            case x if x <= 1800:
                priorityScore += 9

            case x if x <= 3600:
                priorityScore += 6

            case x if x <= 7200:
                priorityScore += 3

            case x if x > 7200:
                priorityScore += 0

        return priorityScore

    @staticmethod
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
        connector = ConnectDB()

        # Create events table if it doesn't exist
        table = """ CREATE TABLE IF NOT EXISTS events
                    (
                        event         text,
                        description   text,
                        unixtimeStart integer,
                        unixtimeEnd   integer,
                        task          boolean default 0,
                        completed     boolean default 0
                    ); """

        connector.cursor.execute(table)
        connector.conn.commit()

        currentTime = int(round(time.time(), 0))
        timeForecast = timeOut(timeForecast)

        connector.cursor.execute("SELECT * FROM events WHERE unixtimeEnd > ? AND unixtimeStart < ?", (currentTime,
                                                                                                      (currentTime +
                                                                                                       timeForecast)))
        events = connector.cursor.fetchall()

        return events

    @staticmethod
    def _giveTasks():
        """
        Retrieves all unscheduled tasks from the calendar database.

        Returns:
            list: List of unscheduled tasks where each task is a tuple containing task details
                  (name, description, urgency, due_date, scheduled_status)
        """
        connector = ConnectDB()

        # Create tasks table if it doesn't exist
        table = """ CREATE TABLE IF NOT EXISTS tasks
                    (
                        task      text,
                        unixtime  integer,
                        urgency   integer,
                        scheduled boolean default 0,
                        dueDate   integer,
                        completed boolean default 0
                    ); """

        connector.cursor.execute(table)
        connector.conn.commit()

        connector.cursor.execute("SELECT * FROM tasks WHERE scheduled = 0 AND completed = 0;")
        tasks = connector.cursor.fetchall()

        taskList = []
        for task in tasks:
            taskDict = {'iD': task[0],
                        'dueDate': task[4],
                        'urgency': task[2],
                        'taskTime': task[1],
                        }

            priorityScore = Scheduler._calculatePriorityScore(taskDict)
            taskDict.update({'priorityScore': priorityScore})
            taskList.append(taskDict)

        return taskList

    @staticmethod
    def _giveBlocks():
        currentTime = int(round(time.time(), 0))
        weekSecDelta = deltaToStartOfWeek(currentTime)
        startOfWeek = currentTime - weekSecDelta

        connector = ConnectDB()

        # Create blocks table if it doesn't exist
        table = """ CREATE TABLE IF NOT EXISTS blocks
                    (
                        timeStart integer,
                        timeEnd   integer
                    ); """

        connector.cursor.execute(table)
        connector.conn.commit()

        tupleBlocks = connector.cursor.execute("SELECT * FROM blocks WHERE timeEnd > ?", (weekSecDelta,))

        blocks = []

        for bloc in tupleBlocks:
            bloc = list(bloc)
            bloc[0] = bloc[0] + startOfWeek
            bloc[1] = bloc[1] + startOfWeek
            blocks.append(bloc)

        return blocks

    @staticmethod
    def _getSchedulingData(timeForecast):
        """
        Retrieves and prepares data needed for scheduling tasks.

        Args:
            timeForecast (str): Time period for scheduling in format "<number> D"

        Returns:
            tuple: (tasks, blocks) where:
                - tasks: List of unscheduled tasks sorted by urgency
                - blocks: Combined list of time blocks and events sorted chronologically
        """

        tasks = Scheduler._giveTasks()
        events = Scheduler.giveEvents(timeForecast)
        blocks = Scheduler._giveBlocks()

        # Sort tasks by urgency
        tasks.sort(key=lambda x: x['priorityScore'], reverse=True)

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

        return tasks, blocks

    @staticmethod
    def _findAvailableTimeSlots(blocks):
        """
        Identifies available time slots between blocks.

        Args:
            blocks (list): List of time blocks sorted chronologically

        Returns:
            list: List of available time slots as tuples (duration, (start_time, end_time))
        """
        availableTime = []

        for n in range(len(blocks)):
            if n != (len(blocks)-1):
                # Calculate time between current block end and next block start
                delta = blocks[n+1][0] - blocks[n][1]
                if delta > 600:
                    # Create time slot with 5-minute buffers on each end
                    timeslot = {'blockTime': delta-600, 'blockStart': blocks[n][1]+300, 'blockEnd': blocks[n+1][0]-300}
                    availableTime.append(timeslot)
            else:
                continue

        return availableTime

    @staticmethod
    def _assignTasksToSlots(tasks, availableTime):
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

        connector = ConnectDB()

        for i in range(len(tasks)):
            for j in range(len(availableTime)):

                if availableTime[j]['blockTime'] > tasks[i]['taskTime']:

                    taskStart = availableTime[j]['blockStart']
                    taskEnd = availableTime[j]['blockEnd'] + tasks[i]['taskTime']

                    connector.cursor.execute("INSERT INTO events VALUES (?,?,?,?,?,?)",
                                             (tasks[i]['iD'],
                                              f"""Due on {toShortHumanTime(tasks[i]['dueDate'])} at 
                                              {toHumanHour(tasks[i]['dueDate'])}. 
                                              Level {tasks[i]['urgency']} urgency""",
                                              taskStart,
                                              taskEnd,
                                              1, 0,))
                    connector.cursor.execute("UPDATE tasks SET scheduled = 1 WHERE task=?", (tasks[i]['iD'],))

                    scheduledTasks.append(tasks[i])
                    # Remove this time slot from available slots to avoid double booking
                    availableTime[j]['blockStart'] = availableTime[j]['blockStart'] + tasks[i]['taskTime'] + 300
                    break

        connector.conn.commit()

        return scheduledTasks

    @staticmethod
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
        tasks, blocks = Scheduler._getSchedulingData(timeForecast)

        # Step 2: Find available time slots
        availableTime = Scheduler._findAvailableTimeSlots(blocks)

        # Step 3: Assign tasks to available slots
        Scheduler._assignTasksToSlots(tasks, availableTime)
