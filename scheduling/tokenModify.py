from parsing.tokenize import Tokens
from utils.dbUtils import ConnectDB
from scheduling.tokenRemove import TokenRemove

class tokenModify:
    def __init__(self, tokenObject: Tokens):
        self.tokens = tokenObject

    def modifyEvent(self):
        connector = ConnectDB()
        connector.conn.execute("UPDATE events SET ?=? WHERE event=?", (self.tokens.modVerb,
                                                                       self.tokens.modContext,
                                                                       self.tokens.iD))
        connector.conn.commit()

    def modifyTask(self):
        connector = ConnectDB()
        connector.conn.execute("SELECT event FROM events WHERE event=?", (self.tokens.iD,))
        row = connector.c.fetchone()

        if len(row) != 0:

            TokenRemove.removeEvent(TokenRemove(self.tokens))
            connector.conn.execute("UPDATE tasks SET ?=? WHERE task=?", (self.tokens.modVerb,
                                                                         self.tokens. modContext,
                                                                         self.tokens.iD))
