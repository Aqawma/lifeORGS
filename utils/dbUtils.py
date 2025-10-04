"""
Database Utilities Module

This module provides database connection and management utilities for the lifeORGS application.
It handles SQLite database connections with automatic path resolution and connection management.

The module ensures that the database file is always accessed from the correct location,
regardless of the current working directory, making the application portable and reliable.
"""

import json
import os
import sqlite3

from utils.jsonUtils import Configs

class ConnectDB:
    """
    Database connection manager for the lifeORGS SQLite database.

    This class provides a convenient interface for connecting to the calendar database
    with automatic path resolution and connection management. It ensures that the
    database file is always accessed from the correct location relative to the project root.

    Attributes:
        conn (sqlite3.Connection): The SQLite database connection object
        cursor (sqlite3.Cursor): The database cursor for executing SQL commands
    """

    @staticmethod
    def getDBPath():
        """
        Returns the absolute path to the calendar database file.

        This ensures that the database file is always accessed from the correct location,
        regardless of the current working directory.

        Returns:
            str: Absolute path to the calendar.db file
        """

        dbName = Configs().mainConfig['DATABASE_NAME']

        # Get the directory of the current file (dbUtils.py)
        currentDir = os.path.dirname(os.path.abspath(__file__))

        # Navigate up to the project root (parent of utils directory)
        projectRoot = os.path.dirname(currentDir)

        # Construct the path to the database file
        dbPath = os.path.join(projectRoot, 'databases', dbName)

        return dbPath

    @staticmethod
    def initConnection(dbPath):
        """
        Initialize a SQLite database connection and cursor.

        Creates a connection to the SQLite database at the specified path
        and returns both the connection and cursor objects for database operations.

        Args:
            dbPath (str): The file path to the SQLite database

        Returns:
            tuple: A tuple containing (connection, cursor) objects
                  - connection (sqlite3.Connection): The database connection
                  - cursor (sqlite3.Cursor): The database cursor for executing commands
        """
        conn = sqlite3.connect(dbPath)
        cursor = conn.cursor()
        return conn, cursor

    def __init__(self):
        """
        Initialize the ConnectDB instance with an active database connection.

        Automatically establishes a connection to the calendar database using
        the resolved database path. The connection and cursor are stored as
        instance attributes for immediate use.

        Attributes set:
            conn (sqlite3.Connection): Active database connection
            cursor (sqlite3.Cursor): Database cursor for SQL operations
        """
        self.conn, self.cursor = self.initConnection(self.getDBPath())

    def dbCleanup(self):
        """
        Clean up the database connection by committing changes and closing.

        This method ensures that all pending database transactions are committed
        and the connection is properly closed. Should be called when database
        operations are complete to prevent connection leaks.

        Note:
            After calling this method, the connection and cursor will no longer
            be usable and a new ConnectDB instance should be created if needed.
        """
        self.conn.commit()
        self.conn.close()
