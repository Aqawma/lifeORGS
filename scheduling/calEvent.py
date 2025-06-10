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

import sqlite3
from utils.timeUtils import toUnixTime, toSeconds


def addEvent(event, description, startTime, endTime):
    # Adds a new event to the calendar database.
    #
    # Args:
    #     event (str): Name of the event
    #     description (str): Description of the event
    #     startTime (str): Start time in format 'DD/MM/YYYY HH:MM'
    #     endTime (str): End time in format 'DD/MM/YYYY HH:MM'
    #
    # Example:
    #     addEvent("Meeting", "Team sync", "26/07/2025 13:30", "26/07/2025 14:30")
    #
    # Note:
    #     Creates events table if it doesn't exist with columns:
    #     - event: text field for event name
    #     - description: text field for event details
    #     - unixtimeStart: integer field for start time in unix format
    #     - unixtimeEnd: integer field for end time in unix format
    #     - task: boolean indicating if entry is a task (default: 0)
    #     - completed: boolean indicating completion status (default: 0)

    conn = sqlite3.connect('calendar.db')

    table = """ CREATE TABLE IF NOT EXISTS events
                (
                    event         text,
                    description   text,
                    unixtimeStart integer,
                    unixtimeEnd   integer,
                    task          boolean default 0,
                    completed     boolean default 0
                ); """

    conn.execute(table)

    start = toUnixTime(startTime)
    end = toUnixTime(endTime)

    conn.execute("INSERT INTO events VALUES (?,?,?,?,?,?)", (event, description, start, end, 0, 0))
    conn.commit()
    conn.close()

def removeEvent(event):
    """
    Removes an event from the calendar database.
    
    Args:
        event (str): Name of the event to remove
    """

    conn = sqlite3.connect('calendar.db')
    conn.execute("DELETE FROM events WHERE event=?", (event,))
    conn.commit()

def modifyEvent(event, description, startTime, endTime):
    """
    Modifies an existing event in the calendar database.
    Implements modification by removing the old event and adding a new one.
    
    Args:
        event (str): Name of the event to modify
        description (str): New description
        startTime (str): New start time in format 'HH:MM'
        endTime (str): New end time in format 'HH:MM'
    """

    removeEvent(event)
    addEvent(event, description, startTime, endTime)

def addTask(task, time, urgency):
    """
    Adds a new task to the calendar database with specified execution time and urgency level.
    
    Args:
        task (str): Name of the task to be added
        time (str): Execution time in format 'HH:MM' or 'HH:MM:SS'. For example: '14:30' or '14:30:00'
        urgency (int): Urgency level of the task (1-5, where 5 is most urgent)
    
    Note:
        Creates tasks table if it doesn't exist with columns:
        - task: text field for task name
        - unixtime: integer field for execution time in unix format
        - urgency: integer field for task priority
        - scheduled: boolean field indicating if task is scheduled (default: 0)
    """

    conn = sqlite3.connect('calendar.db')

    table = """ CREATE TABLE IF NOT EXISTS tasks
                (
                    task      text,
                    unixtime  integer,
                    urgency   integer,
                    scheduled boolean default 0
                ); """

    conn.execute(table)

    time = toSeconds(time)

    conn.execute("INSERT INTO tasks VALUES (?,?,?,?)", (task, time, urgency, 0))

    conn.commit()
    conn.close()

def removeTask(task):
    """
    Removes a task from the calendar database.
    
    Args:
        task (str): Name of the task to remove
    """

    conn = sqlite3.connect('calendar.db')
    conn.execute("DELETE FROM tasks WHERE task=?", (task,))
    conn.commit()

def modifyTask(task, time, urgency):
    """
    Modifies an existing task in the calendar database.
    Implements modification by removing the old task and adding a new one.
    
    Args:
        task (str): Name of the task to modify
        time (str): New time in format 'HH:MM' or 'HH:MM:SS'
        urgency (int): New urgency level
    """

    removeTask(task)
    addTask(task, time, urgency)

def addTimeBlock(day, timeStart, timeEnd):

    conn = sqlite3.connect('calendar.db')

    table = """ CREATE TABLE IF NOT EXISTS blocks
                (
                    day      integer,
                    timeStart  integer,
                    timeEnd   integer
                ); """

    conn.execute(table)

    conn.execute("INSERT INTO blocks VALUES (?,?,?)", (day, timeStart, timeEnd))
    conn.commit()
    conn.close()

def removeTimeBlock(day, timeStart, timeEnd):

    conn = sqlite3.connect('calendar.db')
    conn.execute("DELETE FROM blocks WHERE day=? AND timeStart=? AND timeEnd=?", (day, timeStart, timeEnd))
    conn.commit()


# addTask("testTask", "01:00", 3)
# addEvent("test2", "wow", "09/06/2025 12:00", "09/06/2025 13:00")
# addEvent("test3", "wow", "10/06/2025 12:00", "10/06/2025 13:00")
# addEvent("birthday", "yay", "26/07/2025 00:00", "26/07/2025 23:59")
