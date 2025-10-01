"""
Token Factory Module

This module contains the TokenFactory class which serves as the main command router
for the lifeORGS application. It processes tokenized commands and delegates them
to appropriate handler classes based on the command verb and location.

The TokenFactory implements a factory pattern to create and execute the appropriate
token handler based on the parsed command structure.
"""
from calendarORGS.eventModifiers.calendarAccess import EventObj
from calendarORGS.eventModifiers.gCal import gCalInteract
from userInteraction.parsing.tokenize import Tokens
from calendarORGS.scheduling.eventScheduler import Scheduler
from calendarORGS.eventModifiers.tokenAdd import TokenAdd
from calendarORGS.eventModifiers.tokenModify import TokenModify
from calendarORGS.eventModifiers.tokenRemove import TokenRemove


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
                        gCalInteract().insertEvent(eventObject=EventObj().returnEventFromDB(self.tokens.numID))
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

            case "VIEW":
                pass

            case "SCHEDULE":
                Scheduler.scheduleTasks(self.tokens.viewTime)
