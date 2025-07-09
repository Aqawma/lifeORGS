"""
Token Factory Module

This module contains the TokenFactory class which serves as the main command router
for the lifeORGS application. It processes tokenized commands and delegates them
to appropriate handler classes based on the command verb and location.

The TokenFactory implements a factory pattern to create and execute the appropriate
token handler based on the parsed command structure.
"""

from parsing.tokenize import Tokens
from calendarORGS.scheduling.calendarViews.calendarView import CalendarView
from calendarORGS.scheduling.eventScheduler import Scheduler
from calendarORGS.scheduling.eventModifiers.tokenAdd import TokenAdd
from calendarORGS.scheduling.eventModifiers.tokenModify import TokenModify
from calendarORGS.scheduling.eventModifiers.tokenRemove import TokenRemove


class TokenFactory:
    """
    Factory class for processing tokenized commands and routing them to appropriate handlers.

    This class serves as the central command processor that takes a Tokens object
    and executes the appropriate action based on the command verb (ADD, REMOVE, MODIFY, VIEW, SCHEDULE)
    and location (EVENT, TASK, BLOCK).

    Attributes:
        tokens (Tokens): The tokenized command object containing all parsed command information
    """

    def __init__(self, tokenObject: Tokens):
        """
        Initialize the TokenFactory with a tokenized command object.

        Args:
            tokenObject (Tokens): A Tokens object containing the parsed command information
                                including verb, location, and all relevant parameters
        """
        self.tokens = tokenObject

    def doToken(self):
        """
        Process the tokenized command and execute the appropriate action.

        This method uses pattern matching to route commands based on the verb and location
        attributes of the tokens object. It supports the following command patterns:

        - ADD: Creates new events, tasks, or time blocks
        - REMOVE: Deletes existing events, tasks, or time blocks  
        - MODIFY: Updates existing events or tasks
        - VIEW: Displays calendar events for a specified time period
        - SCHEDULE: Automatically schedules tasks and displays the updated calendar

        Returns:
            str or list: Success message for operations, or formatted event list for VIEW/SCHEDULE
            None: If the command pattern is not recognized

        Raises:
            Exception: May raise exceptions from underlying token handler classes
                      for database errors, invalid parameters, etc.
        """

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
                return "Action could not be completed please check your input."

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
                return "Action could not be completed please check your input."

            case "MODIFY":
                match self.tokens.location:
                    case "EVENT":
                        TokenModify.modifyEvent(TokenModify(self.tokens))
                        return f"{self.tokens.iD} modified successfully."
                    case "TASK":
                        TokenModify.modifyTask(TokenModify(self.tokens))
                        return f"{self.tokens.iD} modified successfully."
                return "Action could not be completed please check your input."

            case "VIEW":
                eventList = CalendarView.viewEvents(self.tokens.viewTime)
                formattedEventStr = CalendarView.convertListToText(eventList)
                return formattedEventStr

            case "SCHEDULE":
                Scheduler.scheduleTasks(self.tokens.viewTime)
                eventList = CalendarView.viewEvents(self.tokens.viewTime)
                formattedEventStr = CalendarView.convertListToText(eventList)
                return formattedEventStr
        return "Action could not be completed please check your input."
