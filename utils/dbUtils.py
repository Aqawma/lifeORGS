import os
import sqlite3

class ConnectDB:
    
    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super(ConnectDB, cls).__new__(cls)
        return cls.instance

    def _getDBPath(self):
        """
        Returns the absolute path to the calendar database file.

        This ensures that the database file is always accessed from the correct location,
        regardless of the current working directory.

        Returns:
            str: Absolute path to the calendar.db file
        """
        # Get the directory of the current file (dbUtils.py)
        currentDir = os.path.dirname(os.path.abspath(__file__))

        # Navigate up to the project root (parent of utils directory)
        projectRoot = os.path.dirname(currentDir)

        # Construct the path to the database file
        dbPath = os.path.join(projectRoot, 'calendar.db')

        return dbPath

    def initConnection(self, dbPath):
        conn = sqlite3.connect(dbPath)
        c = conn.cursor()
        return conn, c

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.conn, self.c = self.initConnection(self._getDBPath())
            self.initialized = True

def convertListToText(lists):
    outputString = "\n".join(lists)
    return outputString