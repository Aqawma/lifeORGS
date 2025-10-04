"""
Test Database Utilities Module

This module provides utilities for creating and populating test databases
for the lifeORGS application. It sets up a clean test environment with
sample data for testing various application features.

Dependencies:
- utils.dbUtils: For database connection and test mode management
- utils.timeUtils: For time conversion and Unix timestamp generation

Classes:
- TestDBUtils: Main utility class for test database operations

Usage:
    This module is typically used in test setups to create a fresh
    test database with known sample data:

    >>> from tests.TestUtils.makeTestDB import TestDBUtils
    >>> TestDBUtils.makeTestDB()

    Or run directly to create a test database:
    $ python tests/TestUtils/makeTestDB.py
"""
from tests.TestUtils.testEnv import setTestEnv
from utils.dbUtils import ConnectDB
from utils.timeUtilitities.timeUtil import toSeconds, TimeConverter


class TestDBUtils:
    """
    Utility class for creating and managing test databases.

    This class provides static methods for setting up clean test databases
    with predefined sample data. It handles the creation of all necessary
    tables and populates them with realistic test data for comprehensive
    testing of the lifeORGS application.

    Methods:
        makeTestDB(): Creates a fresh test database with sample data
    """

    @staticmethod
    @setTestEnv
    def makeTestDB():
        """
        Creates a fresh test database with sample data for testing.

        This method performs the following operations:
        1. Enables test mode to use the test database
        2. Drops existing tables to ensure a clean state
        3. Creates all necessary tables (events, tasks, blocks)
        4. Populates tables with realistic sample data
        5. Commits changes and closes the connection

        Sample data includes:
        - Events: Doctor appointments and scheduled tasks
        - Tasks: Various tasks with different urgency levels and due dates
        - Blocks: Time blocks for scheduling constraints

        Note:
            This method uses setMode(True) to ensure operations are performed
            on the test database rather than the production database.

        Example:
            >>> TestDBUtils.makeTestDB()
            # Creates fresh test database with sample data
        """
        # Enable test mode to use test database instead of production
        connector = ConnectDB()

        # Drop existing tables to ensure clean state
        print("Dropping existing tables...")
        connector.cursor.execute("DROP TABLE IF EXISTS events")
        connector.cursor.execute("DROP TABLE IF EXISTS tasks")
        connector.cursor.execute("DROP TABLE IF EXISTS blocks")

        # Create events table for calendar events and scheduled tasks
        print("Creating events table...")
        tableEvent = """ CREATE TABLE IF NOT EXISTS events
                    (
                        event         text,
                        description   text,
                        unixtimeStart integer,
                        unixtimeEnd   integer,
                        task          boolean default 0,
                        completed     boolean default 0
                    ); """
        connector.cursor.execute(tableEvent)

        # Create tasks table for unscheduled tasks with urgency and due dates
        print("Creating tasks table...")
        tableTask = """ CREATE TABLE IF NOT EXISTS tasks
                    (
                        task      text,
                        unixtime  integer,
                        urgency   integer,
                        scheduled boolean default 0,
                        dueDate   integer,
                        completed boolean default 0
                    ); """
        connector.cursor.execute(tableTask)

        # Create blocks table for available time slots
        print("Creating blocks table...")
        tableBlock = """ CREATE TABLE IF NOT EXISTS blocks
                    (
                        timeStart integer,
                        timeEnd   integer
                    ); """
        connector.cursor.execute(tableBlock)

        # Insert sample event data for testing
        print("Inserting sample events...")

        # Regular calendar event: Doctor appointment
        connector.cursor.execute(f"INSERT INTO events VALUES "
                                 f"('Doctor Appointment', "
                                 f"'Annual check-up', "
                                 f"{TimeConverter('10/07/2025 10:00').convertToUTC()}, "
                                 f"{TimeConverter('10/07/2025 11:00').convertToUTC()}, "
                                 f"0, 0)")  # Not a task, not completed

        # Scheduled task event: Email task that has been scheduled
        connector.cursor.execute(f"INSERT INTO events VALUES "
                                 f"('Send Email', "
                                 f"'Fake description not representative of actual code', "
                                 f"{TimeConverter('08/07/2025 09:05').convertToUTC()}, "
                                 f"{TimeConverter('08/07/2025 09:35').convertToUTC()}, "
                                 f"1, 0)")  # Is a task, not completed

        # Insert sample task data for testing
        print("Inserting sample tasks...")

        # High-priority unscheduled task: Essay writing
        connector.cursor.execute(f"INSERT INTO tasks VALUES "
                                 f"('Write Essay', "
                                 f"{toSeconds('03:00')}, "  # 3 hours estimated time
                                 f"4, "                     # High urgency (4/5)
                                 f"0, "                     # Not scheduled yet
                                 f"{TimeConverter('10/07/2025 10:00').convertToUTC()}, "  # Due date
                                 f"0)")                     # Not completed

        # Medium-priority scheduled task: Email sending
        connector.cursor.execute(f"INSERT INTO tasks VALUES "
                                 f"('Send Email', "
                                 f"{toSeconds('00:30')}, "  # 30 minutes estimated time
                                 f"3, "                     # Medium urgency (3/5)
                                 f"1, "                     # Already scheduled
                                 f"{TimeConverter('10/07/2025 16:00').convertToUTC()}, "  # Due date
                                 f"0)")                     # Not completed

        # Commit all changes and close connection
        print("Committing changes and closing connection...")
        connector.conn.commit()
        connector.conn.close()

        print("Test database created successfully with sample data!")
