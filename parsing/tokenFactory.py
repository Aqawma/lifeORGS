from parsing.tokenize import Tokens
from scheduling.calendarView import CalendarView
from scheduling.eventScheduler import Scheduler
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
                        return f"{self.tokens.iD} added successfully."
                    case "TASK":
                        TokenAdd.addTask(TokenAdd(self.tokens))
                        return f"{self.tokens.iD} added successfully."
                    case "BLOCK":
                        TokenAdd.addBlock(TokenAdd(self.tokens))
                        return "Time block added."
                return None

            case "REMOVE":
                match self.tokens.location:
                    case "EVENT":
                        TokenRemove.removeEvent(TokenRemove(self.tokens))
                        return f"{self.tokens.iD} removed successfully."
                    case "TASK":
                        TokenRemove.removeTask(TokenRemove(self.tokens))
                        return f"{self.tokens.iD} removed successfully."
                    case "BLOCK":
                        TokenRemove.removeBlock(TokenRemove(self.tokens))
                        return "Time block removed successfully."
                return None

            case "MODIFY":
                match self.tokens.location:
                    case "EVENT":
                        TokenModify.modifyEvent(TokenModify(self.tokens))
                        return f"{self.tokens.iD} modified successfully."
                    case "TASK":
                        TokenModify.modifyTask(TokenModify(self.tokens))
                        return f"{self.tokens.iD} modified successfully."
                return None

            case "VIEW":
                eventList = CalendarView.viewEvents(self.tokens.viewTime)
                formattedEventStr = CalendarView.convertListToText(eventList)
                return formattedEventStr

            case "SCHEDULE":
                Scheduler.scheduleTasks(self.tokens.viewTime)
                eventList = CalendarView.viewEvents(self.tokens.viewTime)
                formattedEventStr = CalendarView.convertListToText(eventList)
                return formattedEventStr
        return None


