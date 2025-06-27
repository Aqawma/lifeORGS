"""
Calendar Database Management Module

This module provides functions to manage events and tasks in an SQLite database. It handles CRUD 
(Create, Read, Update, Delete) operations for both events and tasks.

Database Schema:
- events table: Stores calendar events with their descriptions and time ranges
- tasks table: Stores tasks with their execution times and urgency levels

Dependencies:
- sqlite3: For database operations
- utils.pyUtils: Contains time conversion utilities (toUnixTime, toSeconds)
"""
import datetime
from utils.dbUtils import ConnectDB
from utils.timeUtils import toUnixTime, toSeconds

def addEvent(event, description, startTime, endTime, task:bool = False):
    """
    Adds a new event to the calendar database.

    Args:
        event (str): Name of the event
        description (str): Description of the event
        startTime (str): Start time in format 'DD/MM/YYYY HH:MM'
        endTime (str): End time in format 'DD/MM/YYYY HH:MM'
        task (bool, optional): Indicates if this is a task event. Defaults to False.

    Example:
        addEvent("Meeting", "Team sync", "26/07/2025 13:30", "26/07/2025 14:30")

    Note:
        Creates events table if it doesn't exist with columns:
        - event: text field for event name
        - description: text field for event details
        - unixtimeStart: integer field for start time in unix format
        - unixtimeEnd: integer field for end time in unix format
        - task: boolean indicating if entry is a task (default: 0)
        - completed: boolean indicating completion status (default: 0)

    Returns:
        str: Success message or error message if event already exists
    """

    connector = ConnectDB()

    table = """ CREATE TABLE IF NOT EXISTS events
                (
                    event         text,
                    description   text,
                    unixtimeStart integer,
                    unixtimeEnd   integer,
                    task          boolean default 0,
                    completed     boolean default 0
                ); """

    connector.conn.execute(table)

    currentUnixTime = datetime.datetime.now().timestamp()

    connector.conn.execute("SELECT event FROM events WHERE event=? AND unixtimeEnd>?", (event,currentUnixTime,))
    rows = connector.c.fetchall()

    if len(rows) != 0:
        output = f"Event '{event}' already exists in the calendar. \n Please choose a different name."

        connector.conn.close()
        return output
    else:
        start = toUnixTime(startTime)
        end = toUnixTime(endTime)

        connector.conn.execute("INSERT INTO events VALUES (?,?,?,?,?,?)", (event, description, start, end, task, 0))
        connector.conn.commit()

        return f"{event} added successfully."

def removeEvent(event):
    """
    Removes an event from the calendar database.

    Args:
        event (str): Name of the event to remove
    """

    connector = ConnectDB()
    connector.conn.execute("DELETE FROM events WHERE event=?", (event,))
    connector.conn.commit()

def addTask(task, time, urgency, due, scheduled:bool = False):
    """
        Adds a new task to the calendar database with specified execution time, urgency level,
        and due date.

        Args:
            task (str): Name of the task to be added
            time (str): Execution time in format 'HH:MM' or 'HH:MM:SS' (e.g., '14:30' or '14:30:00')
            urgency (int): Urgency level of the task (1-5, where 5 is most urgent)
            due (str): Due date and time in format 'DD/MM/YYYY HH:MM'
            scheduled (bool, optional): Whether the task has been scheduled. Defaults to False

        Database Schema:
            Creates tasks table if it doesn't exist with columns:
            - task: text field for task name
            - unixtime: integer field for execution time in unix format
            - urgency: integer field for task priority (1-5)
            - scheduled: boolean field indicating if task is scheduled
            - dueDate: integer field for task due date in unix timestamp format

        Example:
            #>>> addTask("Complete report", "14:30", 3, "25/12/2023 17:00")
            # Creates a task due on December 25th, 2023 at 5:00 PM
            # with medium urgency (3) and execution time of 2:30 PM

        Note:
            - Time is stored in Unix timestamp format internally
            - Execution time is converted from HH:MM format to seconds since midnight
            - Due date is converted to Unix timestamp for storage
            - The scheduled parameter helps track which tasks have been assigned time slots
        """

    due = toUnixTime(due)

    connector = ConnectDB()

    table = """ CREATE TABLE IF NOT EXISTS tasks
                (
                    task      text,
                    unixtime  integer,
                    urgency   integer,
                    scheduled boolean default 0,
                    dueDate   integer
                ); """

    connector.conn.execute(table)

    connector.conn.execute("SELECT task FROM tasks WHERE task=?", (task,))
    rows = connector.c.fetchall()

    if len(rows) != 0:
        output = f"Event '{task}' already exists in the database. \n Please choose a different name."
        return output
    else:
        time = toSeconds(time)

        connector.conn.execute("INSERT INTO tasks VALUES (?,?,?,?,?)", (task, time, urgency, scheduled, due))

        connector.conn.commit()

        return f"{task} added successfully."

def removeTask(task):
    """
    Removes a task from the calendar database.

    Args:
        task (str): Name of the task to remove
    """

    connector = ConnectDB()
    connector.conn.execute("DELETE FROM tasks WHERE task=?", (task,))
    connector.conn.commit()

def modifyTask(task, time, urgency, due, scheduled:bool = False):
    """
    Modifies an existing task in the calendar database.
    Implements modification by removing the old task and adding a new one.

    Args:
        task (str): Name of the task to modify
        time (str): New time in format 'HH:MM' or 'HH:MM:SS'
        urgency (int): New urgency level
        due (str): Due date and time in format 'DD/MM/YYYY HH:MM'
        scheduled (bool, optional): Whether the task has been scheduled. Defaults to False
    """

    removeTask(task)
    addTask(task, time, urgency, due, scheduled)

def addTimeBlock(day, timeStart, timeEnd):
    """
    Adds a time block to the calendar database for scheduling purposes.

    Time blocks represent periods when events or tasks can be scheduled.
    The function converts day and time information into Unix time format
    for consistent storage and retrieval.

    Args:
        day (int): Day of the week (1-7, where 1 is Monday)
        timeStart (str): Start time in format 'HH:MM' or 'HH:MM:SS'
        timeEnd (str): End time in format 'HH:MM' or 'HH:MM:SS'

    Database Schema:
        Creates blocks table if it doesn't exist with columns:
        - timeStart: integer field for block start time in seconds
        - timeEnd: integer field for block end time in seconds

    Example:
        >>> addTimeBlock(1, "09:00", "12:00")
        # Creates a time block for Monday from 9 AM to 12 PM

    Note:
        - Day values: 1=Monday, 2=Tuesday, ..., 7=Sunday
        - Times are converted to seconds since the start of the week
        - 86400 represents the number of seconds in a day (24*60*60)
    """
    # Connect to the calendar database
    connector = ConnectDB()

    # Create blocks table if it doesn't exist
    table = """ CREATE TABLE IF NOT EXISTS blocks
                (
                    timeStart  integer,
                    timeEnd   integer
                ); """

    connector.conn.execute(table)

    day = int(day)

    # Convert day and time to seconds since start of week
    # (day-1) gives days since start of week (0 for Monday)
    # Multiply by seconds per day and add time in seconds
    timeStart = (86400*(day-1)) + toSeconds(timeStart)
    timeEnd = (86400*(day-1)) + toSeconds(timeEnd)

    # Insert the time block into the database
    connector.conn.execute("INSERT INTO blocks VALUES (?,?)", (timeStart, timeEnd))
    connector.conn.commit()


def removeTimeBlock(timeStart, timeEnd):
    """
    Removes a specific time block from the calendar database.

    This function deletes a time block that matches the exact start and end times provided.
    The times should be in the same format as stored in the database (seconds since start of week).

    Args:
        timeStart (int): Start time of the block to remove (in seconds)
        timeEnd (int): End time of the block to remove (in seconds)

    Example:
        >>> removeTimeBlock(36000, 43200)
        # Removes a time block that starts at 36000 seconds and ends at 43200 seconds
        # (For example, a Monday 10:00-12:00 block would be at 36000-43200 seconds)

    Note:
        - Both timeStart and timeEnd must match exactly for the block to be removed
        - Times should be in seconds since the start of the week
        - To remove a block added with addTimeBlock, you need to use the converted values
    """
    # Connect to the calendar database
    connector = ConnectDB()

    # Delete the time block that matches both start and end times exactly
    connector.conn.execute("DELETE FROM blocks WHERE timeStart=? AND timeEnd=?", (timeStart, timeEnd))
    connector.conn.commit()
