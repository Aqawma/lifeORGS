from parsing.tokenize import Tokens
from utils.dbUtils import ConnectDB
import datetime

class TokenAdd:
    def __init__(self, tokenObject: Tokens):
        self.tokens = tokenObject

    def addEvent(self):
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

        connector.cursor.execute(table)

        currentUnixTime = datetime.datetime.now().timestamp()

        connector.cursor.execute("SELECT event FROM events WHERE event=? AND unixtimeEnd>?", (self.tokens.iD,
                                                                                            currentUnixTime,))
        rows = connector.cursor.fetchall()

        if len(rows) != 0:
            raise exec(f"{self.tokens.iD} already exists in the database.")
        else:

            connector.cursor.execute("INSERT INTO events VALUES (?,?,?,?,?,?)", (self.tokens.iD,
                                                                               self.tokens.description,
                                                                               self.tokens.startTime,
                                                                               self.tokens.endTime,
                                                                               False,
                                                                               False))
            connector.conn.commit()

            return f"{self.tokens.iD} added successfully."

    def addTask(self):

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
            raise exec(f"{self.tokens.iD} already exists in the database and is not completed.")
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
