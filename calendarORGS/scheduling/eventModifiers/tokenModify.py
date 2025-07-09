from parsing.tokenize import Tokens
from utils.dbUtils import ConnectDB
from calendarORGS.scheduling.eventModifiers.tokenRemove import TokenRemove

class TokenModify:
    def __init__(self, tokenObject: Tokens):
        self.tokens = tokenObject

    def modifyEvent(self):
        connector = ConnectDB()
        connector.cursor.execute(f"UPDATE events SET {self.tokens.modVerb}=? WHERE event=?",
                                 (self.tokens.modContext, self.tokens.iD))
        connector.conn.commit()

    def modifyTask(self):
        connector = ConnectDB()
        connector.cursor.execute("SELECT event FROM events WHERE event=?", (self.tokens.iD,))
        row = connector.cursor.fetchone()

        if row is not None:
            TokenRemove.removeEvent(TokenRemove(self.tokens))

        connector.cursor.execute(f"UPDATE tasks SET {self.tokens.modVerb}=? WHERE task=?",
                                 (self.tokens. modContext, self.tokens.iD))
        connector.cursor.execute("UPDATE tasks SET scheduled=0 WHERE task=?", (self.tokens.iD,))

        connector.conn.commit()
