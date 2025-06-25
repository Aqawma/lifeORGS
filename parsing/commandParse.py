import sqlite3

from scheduling.calEvent import addEvent, removeEvent, addTask, modifyTask, addTimeBlock
from scheduling.calFuncs import viewEvents, scheduleTasks
from utils.regex import smartSplit
from utils.timeUtils import toUnixTime, toSeconds
from utils.dbUtils import getDBPath

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
    the appropriate action based on the command type (EVENT, CALENDAR, TASK, BLOCK).

    Args:
        command (str): A string containing the command to be parsed and executed.
                       Expected formats:

                       EVENT commands:
                       - EVENT ADD <name> <start_date> <start_time> <end_date> <end_time> "description"
                       - EVENT DELETE <name>
                       - EVENT MODIFY <name> DISC "new_description"
                       - EVENT MODIFY <name> STARTTIME <date> <time>
                       - EVENT MODIFY <name> ENDTIME <date> <time>
                       - EVENT MODIFY <name> STARTEND <start_date> <start_time> <end_date> <end_time>

                       CALENDAR commands:
                       - CALENDAR VIEW <number> D
                       - CALENDAR SCHEDULE

                       TASK commands:
                       - TASK ADD <name> <time> <due_date> <due_time> <urgency>
                       - TASK DELETE <name>
                       - TASK MODIFY <name> DUEDATE <date> <time>
                       - TASK MODIFY <name> TIME <time>
                       - TASK MODIFY <name> URGENCY <level>

                       BLOCK commands:
                       - BLOCK ADD <day> <start_time> <end_time>

    Returns:
        None

    Note:
        - Commands are case-insensitive except for quoted strings
        - Date format: DD/MM/YYYY (e.g., "25/12/2023")
        - Time format: HH:MM (e.g., "14:30")
        - Day values: 1=Monday, 2=Tuesday, ..., 7=Sunday
        - Urgency levels: 1-5 (where 5 is most urgent)
        - Quoted strings preserve spaces and are used for descriptions
    """

    conn = sqlite3.connect(getDBPath())
    c = conn.cursor()

    # Split the command string into components using smart splitting to handle quoted strings
    splitCommand = smartSplit(command)

    # Convert all non-quoted strings to uppercase for case-insensitive command processing
    for n in range(len(splitCommand)):
        # Check if the string starts with any type of quote (regular or curly)
        if splitCommand[n][0] not in ['"', '\u201c', '\u2018']:
            splitCommand[n] = splitCommand[n].upper()
        else:
            # Strip quotes (regular double, curly double, or curly single)
            if splitCommand[n][0] == '"' and splitCommand[n][-1] == '"':
                splitCommand[n] = splitCommand[n].strip('"')
            elif splitCommand[n][0] == '\u201c' and splitCommand[n][-1] == '\u201d':
                splitCommand[n] = splitCommand[n][1:-1]  # Remove curly double quotes
            elif splitCommand[n][0] == '\u2018' and splitCommand[n][-1] == '\u2019':
                splitCommand[n] = splitCommand[n][1:-1]  # Remove curly single quotes

    # Process EVENT commands (add, delete, modify events)
    if splitCommand[0] == "EVENT":

        if splitCommand[1] == "ADD":
            # Add a new event with name, start time, end time, and description
            addEvent(splitCommand[2],  # Event name
                     splitCommand[7],  # Description
                     (splitCommand[3] + " " + splitCommand[4]),  # Start time (date + time)
                     (splitCommand[5] + " " + splitCommand[6]))  # End time (date + time)
            return f"{splitCommand[2]} added successfully."

        elif splitCommand[1] == "DELETE":
            # Remove an event by its name
            removeEvent(splitCommand[2])
            return f"{splitCommand[2]} deleted successfully."

        elif splitCommand[1] == "MODIFY":
            # Modify different aspects of an existing event

            if splitCommand[3] == "DISC":
                # Update the description of an event
                c.execute("UPDATE events SET description=? WHERE event=?",
                          (splitCommand[4], splitCommand[2]))
                conn.commit()
                conn.close()
                return f"{splitCommand[2]} modified successfully."

            elif splitCommand[3] == "STARTTIME":
                # Update the start time of an event
                c.execute("UPDATE events SET unixtimeStart=? WHERE event=?",
                          (toUnixTime(splitCommand[4] + " " + splitCommand[5]), splitCommand[2]))
                conn.commit()
                conn.close()
                return f"{splitCommand[2]} modified successfully."

            elif splitCommand[3] == "ENDTIME":
                # Update the end time of an event
                c.execute("UPDATE events SET unixtimeEnd=? WHERE event=?",
                          (toUnixTime(splitCommand[4] + " " + splitCommand[5]), splitCommand[2]))
                conn.commit()
                conn.close()
                return f"{splitCommand[2]} modified successfully."

            elif splitCommand[3] == "STARTEND":
                # Update both start and end times of an event
                c.execute("UPDATE events SET unixtimeStart=? WHERE event=?",
                          (toUnixTime(splitCommand[4] + " " + splitCommand[5]), splitCommand[2]))
                c.execute("UPDATE events SET unixtimeEnd=? WHERE event=?",
                          (toUnixTime(splitCommand[6] + " " + splitCommand[7]), splitCommand[2]))
                conn.commit()
                conn.close()
                return f"{splitCommand[2]} modified successfully."

            else:
                return "Invalid command. Please try again."

        else:
            return "Invalid command. Please try again."

    # Process CALENDAR commands (view, schedule)
    elif splitCommand[0] == "CALENDAR":

        if splitCommand[1] == "VIEW":
            # View events within a specified time period
            scheduledEvents = viewEvents((splitCommand[2] + " " + splitCommand[3]))
            # Time period format (e.g., "14 D" for 14 days)
            return scheduledEvents

        elif splitCommand[1] == "SCHEDULE":
            # Schedule tasks and view the resulting calendar
            # TODO: Add some sort of configuration for scheduling threshold. Goes with other issues with timeOut().
            scheduleTasks("14 D")  # Schedule tasks for the next 14 days
            formattedEvents = viewEvents("14 D")  # Get formatted events for the next 14 days
            return formattedEvents

        else:
            return "Invalid command. Please try again."

    # Process TASK commands (add, delete, modify tasks)
    elif splitCommand[0] == "TASK":

        if splitCommand[1] == "ADD":
            # Add a new task with name, estimated time, due date, and urgency
            addTask(splitCommand[2],  # Task name
                    (splitCommand[3]),  # Estimated time
                    splitCommand[6],    # Urgency
                    (splitCommand[4] + " " + splitCommand[5]))  # Due date
            return f"{splitCommand[2]} added successfully."

        elif splitCommand[1] == "DELETE":
            # Remove a task by its name
            removeEvent(splitCommand[2])
            return f"{splitCommand[2]} deleted successfully."

        elif splitCommand[1] == "MODIFY":
            # Modify different aspects of an existing task

            # Check if the task is already scheduled as an event
            conn.execute("SELECT event FROM events WHERE event=?", (splitCommand[2],))
            rows = c.fetchall()

            if len(rows) != 0:
                # If task is scheduled, get its details, remove the event, and recreate it as a task
                conn.execute("SELECT task, unixtime, urgency, scheduled, dueDate FROM tasks WHERE task=?",
                             (splitCommand[2],))
                row = c.fetchone()
                removeEvent(splitCommand[2])
                modifyTask(row[0], row[1], row[2], row[4], False)
                return f"{splitCommand[2]} modified successfully."

            if splitCommand[3] == "DUEDATE":
                # Update the due date of a task
                c.execute("UPDATE tasks SET dueDate=? WHERE task=?",
                          (toUnixTime(splitCommand[4] + " " + splitCommand[5]), splitCommand[2]))
                conn.commit()
                conn.close()
                return f"{splitCommand[2]} modified successfully."

            elif splitCommand[3] == "TIME":
                # Update the estimated time of a task
                c.execute("UPDATE tasks SET unixtime=? WHERE task=?",
                          (toSeconds(splitCommand[4]), splitCommand[2]))
                conn.commit()
                conn.close()
                return f"{splitCommand[2]} modified successfully."

            elif splitCommand[3] == "URGENCY":
                # Update the urgency level of a task
                c.execute("UPDATE tasks SET urgency=? WHERE task=?",
                          (int(splitCommand[4]), splitCommand[2]))
                conn.commit()
                conn.close()
                return f"{splitCommand[2]} modified successfully."

            else:
                return "Invalid command. Please try again."

        else:
            return "Invalid command. Please try again."

    # Process BLOCK commands (add, delete time blocks for scheduling)
    elif splitCommand[0] == "BLOCK":

        if splitCommand[1] == "ADD":
            # Add a new time block with day, start time, and end time
            # Expected format: BLOCK ADD <day> <start_time> <end_time>
            # Example: BLOCK ADD 1 09:00 17:00 (Monday 9 AM to 5 PM)
            addTimeBlock(splitCommand[2],  # Day of week (1-7, where 1=Monday)
                         splitCommand[3],   # Start time (HH:MM format)
                         splitCommand[4])   # End time (HH:MM format)
            return "Time block added successfully."

        else:
            return "Invalid command. Please try again."
        # TODO: Implement BLOCK DELETE functionality
        # elif splitCommand[1] == "DELETE":
        #     # Remove a time block by day and time range
        #     removeTimeBlock(splitCommand[2], splitCommand[3], splitCommand[4])

    # TODO: Future implementation for FILE commands
    # This section will handle file import/export operations
    # elif splitCommand[0] == "FILE":
    #     if splitCommand[1] == "IMPORT":
    #         # Import events/tasks from external file
    #         pass
    #     elif splitCommand[1] == "EXPORT":
    #         # Export calendar data to external file
    #         pass

    else:
        return "Invalid command. Please try again."
