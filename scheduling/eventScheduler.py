"""
Calendar Functions Module

This module provides high-level functions for calendar operations including viewing events,
scheduling tasks, and managing time blocks. It serves as the main interface for calendar
functionality, coordinating between the database layer and user interface.

Key Features:
- Event retrieval and formatting for display
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
import sqlite3
import time

from utils.dbUtils import ConnectDB
from utils.timeUtils import timeOut, toShortHumanTime, toHumanHour, deltaToStartOfWeek


class Scheduler:
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

        selection = """ SELECT * FROM tasks WHERE scheduled = 0"""

        connector.cursor.execute(selection)
        tasks = connector.cursor.fetchall()

        return tasks

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

        # Sort tasks by urgency
        tasks.sort(key=lambda x: x[2])
        blocks.sort(key=lambda x: x[0])

        print(blocks)

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
                    timeslot = [delta-600, [blocks[n][1]+300, blocks[n+1][0]-300]]
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

                if availableTime[j][0] > tasks[i][1]:

                    taskStart = availableTime[j][1][0]
                    taskEnd = availableTime[j][1][0] + tasks[i][1]

                    connector.cursor.execute("INSERT INTO events VALUES (?,?,?,?,?,?)",
                                           (tasks[i][0],
                                            f"""Due on {toShortHumanTime(tasks[i][4])} at {toHumanHour(tasks[i][4])}. 
                                             Level {tasks[i][2]} urgency""",
                                            taskStart,
                                            taskEnd,
                                            1, 0,))
                    connector.cursor.execute("UPDATE tasks SET scheduled = 1 WHERE task=?", (tasks[i][0],))

                    scheduledTasks.append(tasks[i])
                    # Remove this time slot from available slots to avoid double booking
                    availableTime[j][1][0] = availableTime[j][1][0] + tasks[i][1] + 300
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
