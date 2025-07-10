from utils.dbUtils import ConnectDB
from utils.dbUtils import setMode
from utils.timeUtils import toSeconds, TimeUtility


class TestDBUtils:
    @staticmethod
    def makeTestDB():
        setMode(True)
        connector = ConnectDB()

        connector.cursor.execute("DROP TABLE IF EXISTS events")
        connector.cursor.execute("DROP TABLE IF EXISTS tasks")
        connector.cursor.execute("DROP TABLE IF EXISTS blocks")

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
        tableBlock = """ CREATE TABLE IF NOT EXISTS blocks
                    (
                        timeStart integer,
                        timeEnd   integer
                    ); """
        connector.cursor.execute(tableBlock)

        connector.cursor.execute(f"INSERT INTO events VALUES "
                                 f"('Doctor Appointment', "
                                 f"'Annual check-up', "
                                 f"{TimeUtility('10/07/2025 10:00').convertToUTC()}, "
                                 f"{TimeUtility('10/07/2025 11:00').convertToUTC()}, "
                                 f"0, 0)")
        connector.cursor.execute(f"INSERT INTO tasks VALUES "
                                 f"('Write Essay', "
                                 f"{toSeconds('03:00')}, "
                                 f"4, "
                                 f"0, "
                                 f"{TimeUtility('10/07/2025 10:00').convertToUTC()}, "
                                 f"0)")
        connector.cursor.execute(f"INSERT INTO tasks VALUES "
                                 f"('Send Email', "
                                 f"{toSeconds('00:30')}, "
                                 f"3, "
                                 f"1, "
                                 f"{TimeUtility('10/07/2025 16:00').convertToUTC()}, "
                                 f"0)")
        connector.cursor.execute(f"INSERT INTO events VALUES "
                                 f"('Send Email', "
                                 f"'Fake description not representative of actual code', "
                                 f"{TimeUtility('08/07/2025 09:05').convertToUTC()}, "
                                 f"{TimeUtility('08/07/2025 09:35').convertToUTC()}, "
                                 f"1, 0)")
        connector.conn.commit()
        connector.conn.close()
