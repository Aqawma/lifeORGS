import sqlite3
from os import WCONTINUED

from scheduling.calEvent import addEvent, removeEvent, addTask, modifyTask
from scheduling.calFuncs import viewEvents, scheduleTasks
from utils.regex import smartSplit
from utils.timeUtils import toUnixTime, toSeconds


"""
Main module for the lifeORGS application.
This module serves as the command parser for the application, handling various commands
related to events, tasks, and calendar management. It interprets user input and routes
commands to the appropriate functions in other modules.
"""


def parseCommand(command):
    """
    Parse and execute a command string input by the user.

    This function takes a command string, splits it into components, and executes
    the appropriate action based on the command type (EVENT, CALENDAR, TASK).

    Args:
        command (str): A string containing the command to be parsed and executed.
                       Expected format varies based on command type.

    Returns:
        None

    Note:
        Commands are case-insensitive except for quoted strings.
        The first element of the command is typically the application name,
        followed by the command type (EVENT, CALENDAR, TASK).
    """

    conn = sqlite3.connect('calendar.db')
    c = conn.cursor()

    # Split the command string into components using smart splitting to handle quoted strings
    splitCommand = smartSplit(command)

    # Convert all non-quoted strings to uppercase for case-insensitive command processing
    for n in range(len(splitCommand)):
        if splitCommand[n][0] != '"':
            splitCommand[n] = splitCommand[n].upper()
        else:
            continue

    # Process EVENT commands (add, delete, modify events)
    if splitCommand[1] == "EVENT":

        if splitCommand[2] == "ADD":
            # Add a new event with name, start time, end time, and description
            addEvent(splitCommand[3],
                     (splitCommand[4] + " " + splitCommand[5]),  # Start time (date + time)
                     (splitCommand[6] + " " + splitCommand[7]),  # End time (date + time)
                     splitCommand[8])  # Description

        elif splitCommand[2] == "DELETE":
            # Remove an event by its name
            removeEvent(splitCommand[3])

        elif splitCommand[2] == "MODIFY":
            # Modify different aspects of an existing event

            if splitCommand[4] == "DISC":
                # Update the description of an event
                c.execute("UPDATE events SET description=? WHERE event=?",
                          (splitCommand[5], splitCommand[3]))
                conn.commit()
                conn.close()

            elif splitCommand[4] == "STARTTIME":
                # Update the start time of an event
                c.execute("UPDATE events SET unixtimeStart=? WHERE event=?",
                          (toUnixTime(splitCommand[5] + " " + splitCommand[6]), splitCommand[3]))
                conn.commit()
                conn.close()

            elif splitCommand[4] == "ENDTIME":
                # Update the end time of an event
                c.execute("UPDATE events SET unixtimeEnd=? WHERE event=?",
                          (toUnixTime(splitCommand[5] + " " + splitCommand[6]), splitCommand[3]))
                conn.commit()
                conn.close()

            elif splitCommand[4] == "STARTEND":
                # Update both start and end times of an event
                c.execute("UPDATE events SET unixtimeStart=? WHERE event=?",
                          (toUnixTime(splitCommand[5] + " " + splitCommand[6]), splitCommand[3]))
                c.execute("UPDATE events SET unixtimeEnd=? WHERE event=?",
                          (toUnixTime(splitCommand[7] + " " + splitCommand[8]), splitCommand[3]))
                conn.commit()
                conn.close()

    # Process CALENDAR commands (view, schedule)
    elif splitCommand[1] == "CALENDAR":

        if splitCommand[2] == "VIEW":
            # View events within a specified time period
            viewEvents((splitCommand[3] + " " + splitCommand[4]))  # Time period format (e.g., "14 D" for 14 days)

        elif splitCommand[2] == "SCHEDULE":
            # Schedule tasks and view the resulting calendar
            #TODO Add some sort of configuration for scheduling threshold. Goes with other issues with timeOut().
            scheduleTasks("14 D")  # Schedule tasks for the next 14 days
            viewEvents("14 D")     # View events for the next 14 days

    # Process TASK commands (add, delete, modify tasks)
    elif splitCommand[1] == "TASK":

        if splitCommand[2] == "ADD":
            # Add a new task with name, estimated time, due date, and urgency
            addTask(splitCommand[3],                            # Task name
                    (splitCommand[4] + " " + splitCommand[5]),  # Estimated time
                    (splitCommand[6] + " " + splitCommand[7]),  # Due date
                    splitCommand[8])                            # Urgency

        elif splitCommand[2] == "DELETE":
            # Remove a task by its name
            removeEvent(splitCommand[3])

        elif splitCommand[2] == "MODIFY":
            # Modify different aspects of an existing task

            # Check if the task is already scheduled as an event
            conn.execute("SELECT event FROM events WHERE event=?", (splitCommand[3],))
            rows = c.fetchall()

            if len(rows) != 0:
                # If task is scheduled, get its details, remove the event, and recreate it as a task
                conn.execute("SELECT task, unixtime, urgency, scheduled, dueDate FROM tasks WHERE task=?", 
                             (splitCommand[3],))
                row = c.fetchone()
                removeEvent(splitCommand[3])
                modifyTask(row[0], row[1], row[2], row[4], False)

            if splitCommand[4] == "DUEDATE":
                # Update the due date of a task
                c.execute("UPDATE tasks SET dueDate=? WHERE task=?", 
                          (toUnixTime(splitCommand[5] + " " + splitCommand[6]), splitCommand[3]))
                conn.commit()
                conn.close()

            elif splitCommand[4] == "TIME":
                # Update the estimated time of a task
                c.execute("UPDATE tasks SET unixtime=? WHERE task=?", 
                          (toSeconds(splitCommand[5]), splitCommand[3]))
                conn.commit()
                conn.close()

            elif splitCommand[4] == "URGENCY":
                # Update the urgency level of a task
                c.execute("UPDATE tasks SET urgency=? WHERE task=?", 
                          (int(splitCommand[5]), splitCommand[3]))
                conn.commit()
                conn.close()

    # Future implementation for FILE commands
    # elif splitCommand[1] == "FILE":
