from parsing.tokenize import Tokens
from utils.dbUtils import ConnectDB

class TokenRemove:
    def __init__(self, tokenObject: Tokens):
        self.tokens = tokenObject

    def removeEvent(self):
        connector = ConnectDB()
        connector.conn.execute("DELETE FROM events WHERE event=?", (self.tokens.iD,))
        connector.conn.commit()
        return f"{self.tokens.iD} removed successfully."

    def removeTask(self):
        connector = ConnectDB()
        connector.conn.execute("DELETE FROM tasks WHERE task=?", (self.tokens.iD,))
        connector.conn.commit()
        return f"{self.tokens.iD} removed successfully."

    def removeBlock(self):
        connector = ConnectDB()
        connector.conn.execute("DELETE FROM blocks WHERE timeStart=? AND timeEnd=?", (self.tokens.blockStart,
                                                                                      self.tokens.blockEnd))
        connector.conn.commit()
        return f"Time block removed successfully."
