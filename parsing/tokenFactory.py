from parsing.tokenize import Tokens
from scheduling.tokenAdd import TokenAdd
from scheduling.tokenModify import TokenModify
from scheduling.tokenRemove import TokenRemove


class TokenFactory:
    def __init__(self, tokenObject: Tokens):
        self.tokens = tokenObject

    def doToken(self):

        match self.tokens.verb:
            case "ADD":
                match self.tokens.location:
                    case "EVENT":
                        TokenAdd.addEvent(TokenAdd(self.tokens))
                    case "TASK":
                        TokenAdd.addTask(TokenAdd(self.tokens))
                    case "BLOCK":
                        TokenAdd.addBlock(TokenAdd(self.tokens))

            case "REMOVE":
                match self.tokens.location:
                    case "EVENT":
                        TokenRemove.removeEvent(TokenRemove(self.tokens))
                    case "TASK":
                        TokenRemove.removeTask(TokenRemove(self.tokens))
                    case "BLOCK":
                        TokenRemove.removeBlock(TokenRemove(self.tokens))

            case "MODIFY":
                match self.tokens.location:
                    case "EVENT":
                        TokenModify.modifyEvent(TokenModify(self.tokens))
                    case "TASK":
                        TokenModify.modifyTask(TokenModify(self.tokens))
