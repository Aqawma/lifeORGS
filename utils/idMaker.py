import time
import random
import hashlib

from utils.dbUtils import ConnectDB


def generateID(seedStr: str):
    while True:
        seed = seedStr + str(time.time()) + str(random.randint(0, 1000000))
        eventID = int(hashlib.sha256(seed.encode()).hexdigest()[:20], 16)

        connector = ConnectDB()
        connector.cursor.execute("SELECT event FROM events WHERE event=?", (eventID,))
        row = connector.cursor.fetchone()

        if row is None:
            return eventID
        else:
            continue
