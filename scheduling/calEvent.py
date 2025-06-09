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
from utils.pyUtils import toUnixTime, toSeconds

def addEvent(event, description, startDate, endDate, startTime, endTime):
    """
    Adds a new event to the calendar database.
    
    Args:
        event (str): Name of the event
        description (str): Description of the event
        startDate (str): Start date in format 'DD/MM/YYYY'
        endDate (str): End date in format 'DD/MM/YYYY'
        startTime (str): Start time in format 'HH:MM'
        endTime (str): End time in format 'HH:MM'
    """

    conn = sqlite3.connect('calendar.db')

    table = """ CREATE TABLE IF NOT EXISTS events (
    event text,
    description text,
    unixtimeStart integer,
    unixtimeEnd integer); """

    conn.execute(table)

    start = toUnixTime(startDate, startTime)
    end = toUnixTime(endDate, endTime)

    conn.execute("INSERT INTO events VALUES (?,?,?,?)", (event, description, start, end))
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

def modifyEvent(event, description, startDate, endDate, startTime, endTime):
    """
    Modifies an existing event in the calendar database.
    Implements modification by removing the old event and adding a new one.
    
    Args:
        event (str): Name of the event to modify
        description (str): New description
        startDate (str): New start date in format 'DD/MM/YYYY'
        endDate (str): New end date in format 'DD/MM/YYYY'
        startTime (str): New start time in format 'HH:MM'
        endTime (str): New end time in format 'HH:MM'
    """

    removeEvent(event)
    addEvent(event, description, startDate, endDate, startTime, endTime)

def addTask(task, time, urgency):
    """
    Adds a new task to the calendar database.
    
    Args:
        task (str): Name of the task
        time (str): Time in format 'HH:MM' or 'HH:MM:SS'
        urgency (int): Urgency level of the task
    """

    conn = sqlite3.connect('calendar.db')

    table = """ CREATE TABLE IF NOT EXISTS tasks (
    task text,
    unixtime integer,
    urgency integer); """

    conn.execute(table)

    time = toSeconds(time)

    conn.execute("INSERT INTO tasks VALUES (?,?,?)", (task, time, urgency))

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