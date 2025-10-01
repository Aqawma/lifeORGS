"""
Token Add Module

This module contains the TokenAdd class which handles the creation of new events,
tasks, and time blocks in the lifeORGS system. It provides database operations
for adding calendar items with proper validation and error handling.

The module interacts with the SQLite database to create the necessary tables
and insert new records based on the tokenized command information.
"""

from userInteraction.parsing.tokenize import Tokens
from utils.dbUtils import ConnectDB


class TokenAdd:
    """
    Handler class for adding new events, tasks, and time blocks to the database.

    This class processes ADD commands by creating new database entries for events,
    tasks, or time blocks based on the tokenized command information. It handles
    database table creation, duplicate checking, and data insertion.

    Attributes:
        tokens (Tokens): The tokenized command object containing all parameters
                        needed for the add operation
    """

    def __init__(self, tokenObject: Tokens):
        """
        Initialize the TokenAdd handler with a tokenized command object.

        Args:
            tokenObject (Tokens): A Tokens object containing the parsed command
                                information including ID, times, descriptions, etc.
        """
        self.tokens = tokenObject

    def addEvent(self):
        """
        Add a new event to the events database table.

        Creates the events table if it doesn't exist, checks for duplicate events
        that haven't ended yet, and inserts a new event record with the provided
        information from the tokens object.

        The method prevents duplicate events by checking if an event with the same
        name exists and has an end time in the future.

        Returns:
            str: Success message indicating the event was added successfully

        Raises:
            Exception: If an event with the same name already exists and hasn't ended

        Database Schema:
            events table contains:
            - event (text): EventObj name/identifier
            - description (text): EventObj description
            - unixtimeStart (integer): EventObj start time as Unix timestamp
            - unixtimeEnd (integer): EventObj end time as Unix timestamp
            - task (boolean): Whether this is a task (default: False)
            - completed (boolean): Whether the event is completed (default: False)
        """
        connector = ConnectDB()

        table = """ CREATE TABLE IF NOT EXISTS events
                    (
                        event         text,
                        description   text,
                        unixtimeStart integer,
                        unixtimeEnd   integer,
                        location      text,
                        summary       text,
                        status        text default 'CONFIRMED',
                        class         text default 'PRIVATE'
                    ); """
        connector.cursor.execute(table)

        connector.cursor.execute("INSERT INTO events VALUES (?,?,?,?,?,?,?,?)", (self.tokens.numID,
                                                                                 self.tokens.description,
                                                                                 self.tokens.startTime,
                                                                                 self.tokens.endTime,
                                                                                 self.tokens.physicalLocation,
                                                                                 self.tokens.iD,
                                                                                 "CONFIRMED",
                                                                                 "PRIVATE"))
        connector.conn.commit()

        return f"{self.tokens.iD} added successfully."

    def addTask(self):
        """
        Add a new task to the tasks database table.

        Creates the tasks table if it doesn't exist, checks for duplicate incomplete tasks,
        and inserts a new task record with the provided information from the tokens object.

        The method prevents duplicate tasks by checking if a task with the same name
        already exists and is not completed.

        Returns:
            str: Success message indicating the task was added successfully

        Raises:
            Exception: If a task with the same name already exists and is not completed

        Database Schema:
            tasks table contains:
            - task (text): Task name/identifier
            - unixtime (integer): Estimated time to complete task in seconds
            - urgency (integer): Task urgency level (higher numbers = more urgent)
            - scheduled (boolean): Whether the task has been scheduled (default: False)
            - dueDate (integer): Task due date as Unix timestamp
            - completed (boolean): Whether the task is completed (default: False)
        """
        connector = ConnectDB()

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
        connector.cursor.execute("SELECT task FROM tasks WHERE task=? AND completed == False", (self.tokens.iD,))
        rows = connector.cursor.fetchall()

        if len(rows) != 0:
            raise Exception(f"{self.tokens.iD} already exists in the database and is not completed.")
        else:

            connector.cursor.execute("INSERT INTO tasks VALUES (?,?,?,?,?,?)", (self.tokens.iD,
                                                                                self.tokens.taskTime,
                                                                                self.tokens.urgency,
                                                                                False,
                                                                                self.tokens.dueDate,
                                                                                False))

            connector.conn.commit()

            return f"{self.tokens.iD} added successfully."

    def addBlock(self):
        """
        Add a new time block to the blocks database table.

        Creates the blocks table if it doesn't exist and inserts a new time block
        record with the start and end times from the tokens object. Time blocks
        define available periods for automatic task scheduling.

        Unlike events and tasks, time blocks don't check for duplicates as multiple
        overlapping time blocks may be intentionally created for scheduling flexibility.

        Returns:
            str: Success message indicating the time block was added successfully

        Database Schema:
            blocks table contains:
            - timeStart (integer): Block start time as Unix timestamp
            - timeEnd (integer): Block end time as Unix timestamp
        """
        connector = ConnectDB()

        # Create blocks table if it doesn't exist
        table = """ CREATE TABLE IF NOT EXISTS blocks
                    (
                        timeStart integer,
                        timeEnd   integer
                    ); """

        connector.cursor.execute(table)

        # Insert the time block into the database
        connector.cursor.execute("INSERT INTO blocks VALUES (?,?)", (self.tokens.blockStart, self.tokens.blockEnd))
        connector.conn.commit()
        return f"Time block added."
