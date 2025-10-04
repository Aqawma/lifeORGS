import time
import random
import hashlib

from utils.dbUtils import ConnectDB


def generateID(seedStr: str):
    connector = ConnectDB()
    try:
        while True:
            seed = seedStr + str(time.time()) + str(random.randint(0, 1000000))
            eventID = int(hashlib.sha256(seed.encode()).hexdigest()[:10], 16)

            connector.cursor.execute("SELECT event FROM events WHERE event=?", (eventID,))
            row = connector.cursor.fetchone()
            if row is None:
                return eventID
            else:
                continue
    finally:
        connector.conn.close()


