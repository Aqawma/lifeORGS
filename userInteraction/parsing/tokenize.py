"""
Command Tokenization Module

This module provides command parsing and tokenization functionality for the lifeORGS application.
It handles the conversion of user input strings into structured Token objects that can be
processed by other parts of the application.

The module includes:
- Tokens class: A data container for parsed command information
- CommandTokenizer class: Handles parsing and tokenization of user commands

The tokenizer supports complex command parsing including quoted strings, date/time parsing,
and command validation for events, tasks, and time blocks.
"""

import re

from utils.timeUtils import TimeUtility, toSeconds
from dataclasses import dataclass
from typing import Optional, Union


@dataclass
class Tokens:
    """A data class that represents parsed command tokens for the lifeORGS application."""
    location: str
    verb: str
    iD: Optional[str] = None
    modVerb: Optional[str] = None
    modContext: Optional[Union[str, int, float]] = None
    startTime: Optional[float] = None
    endTime: Optional[float] = None
    description: Optional[str] = None
    dueDate: Optional[float] = None
    taskTime: Optional[float] = None
    urgency: Optional[int] = None
    blockStart: Optional[float] = None
    blockEnd: Optional[float] = None
    viewTime: Optional[str] = None


class CommandTokenizer:
    """
    A command parser and tokenizer for the lifeORGS application.

    This class handles the parsing of user input commands and converts them into
    structured Token objects that can be processed by other parts of the application.
    It supports commands for managing events, tasks, and time blocks with various
    operations like ADD, REMOVE, and MODIFY.

    The tokenizer handles complex command parsing including quoted strings,
    date/time parsing, and command validation.
    """

    @staticmethod
    def _smartSplit(text) -> list[str]:
        """
        Splits a string by whitespace while preserving content within quotes, including the quotation marks.

        Args:
            text (str): The input string to split

        Returns:
            list: List of tokens where quoted content remains as single items with quotation marks preserved

        Examples:
            #>>> _smartSplit('command "first argument" second "third argument"')
            ['command', '"first argument"', 'second', '"third argument"']

            #>>> _smartSplit('simple test "with quotes" and "multiple parts"')
            ['simple', 'test', '"with quotes"', 'and', '"multiple parts"']
        """
        pattern = r'[^\s"\u201c\u201d\u2018\u2019]+|"([^"]*)"|[\u201c]([^\u201d]*)[\u201d]|[\u2018]([^\u2019]*)[\u2019]'

        # Create the result list combining non-quoted and quoted parts
        result = []
        for item in re.finditer(pattern, text):
            # Always use the full match to preserve quotation marks
            result.append(item.group(0))

        return result

    @staticmethod
    def _parseCommand(command):
        """
        Parse and execute a command string input by the user.

        This function takes a command string, splits it into components, and executes
        the appropriate action based on the command type (EVENT, CALENDAR, TASK, BLOCK).

        Args:
            command (str): A string containing the command to be parsed and executed.
                           Expected formats:

                           EVENT commands:
                           - EVENT ADD <name> <start_date> <start_time> <end_date> <end_time> "description"
                           - EVENT DELETE <name>
                           - EVENT MODIFY <name> DISC "new_description"
                           - EVENT MODIFY <name> STARTTIME <date> <time>
                           - EVENT MODIFY <name> ENDTIME <date> <time>
                           - EVENT MODIFY <name> STARTEND <start_date> <start_time> <end_date> <end_time>

                           CALENDAR commands:
                           - CALENDAR VIEW <number> D
                           - CALENDAR SCHEDULE

                           TASK commands:
                           - TASK ADD <name> <time> <due_date> <due_time> <urgency>
                           - TASK DELETE <name>
                           - TASK MODIFY <name> DUEDATE <date> <time>
                           - TASK MODIFY <name> TIME <time>
                           - TASK MODIFY <name> URGENCY <level>

                           BLOCK commands:
                           - BLOCK ADD <day> <start_time> <end_time>

        Returns:
            None

        Note:
            - Commands are case-insensitive except for quoted strings
            - Date format: DD/MM/YYYY (e.g., "25/12/2023")
            - Time format: HH:MM (e.g., "14:30")
            - Day values: 1=Monday, 2=Tuesday, ..., 7=Sunday
            - Urgency levels: 1-5 (where 5 is most urgent)
            - Quoted strings preserve spaces and are used for descriptions
        """

        # Split the command string into components using smart splitting to handle quoted strings
        splitCommand = CommandTokenizer._smartSplit(command)

        # Convert all non-quoted strings to uppercase for case-insensitive command processing
        for n in range(len(splitCommand)):
            # Check if the string starts with any type of quote (regular or curly)
            if splitCommand[n][0] not in ['"', '\u201c', '\u2018']:
                splitCommand[n] = splitCommand[n].upper()
            else:
                # Strip quotes (regular double, curly double, or curly single)
                if splitCommand[n][0] == '"' and splitCommand[n][-1] == '"':
                    splitCommand[n] = splitCommand[n].strip('"')
                elif splitCommand[n][0] == '\u201c' and splitCommand[n][-1] == '\u201d':
                    splitCommand[n] = splitCommand[n][1:-1]  # Remove curly double quotes
                elif splitCommand[n][0] == '\u2018' and splitCommand[n][-1] == '\u2019':
                    splitCommand[n] = splitCommand[n][1:-1]  # Remove curly single quotes

        return splitCommand

    @staticmethod
    def _getContext(tokens):
        """
        Extract context tokens from a parsed command.

        This method takes a list of parsed command tokens and returns all tokens
        except the first two (location and verb), which represent the command context
        or arguments needed to execute the command.

        Args:
            tokens (list): List of parsed command tokens where:
                          - tokens[0] is the location/type (EVENT, TASK, BLOCK)
                          - tokens[1] is the verb/action (ADD, REMOVE, MODIFY)
                          - tokens[2: ] are the context/arguments

        Returns:
            list: List containing all tokens from index 2 onwards, representing
                  the command arguments and context information.

        Example:
            #>>> tokens = ['EVENT', 'ADD', 'meeting', '25/12/2023', '14:00', '25/12/2023', '15:00', 'Team meeting']
            #>>> _getContext(tokens)
            ['meeting', '25/12/2023', '14:00', '25/12/2023', '15:00', 'Team meeting']
        """
        context = []

        for token in range(len(tokens)):
            if token != 0 and token != 1:
                context.append(tokens[token])
            else:
                continue

        return context

    def _createTokenObject(self):
        """
        Create and populate a Tokens object based on the parsed command.

        This method creates a Tokens object and populates it with the appropriate
        attributes based on the command location (EVENT, TASK, BLOCK) and verb
        (ADD, REMOVE, MODIFY). It handles the conversion of date/time strings to
        Unix timestamps and validates command structure.

        Returns:
            Tokens: A fully populated Tokens object with all relevant attributes
                   set based on the command type and context.

        Raises:
            Exception: If the command format is invalid or unsupported.

        Note:
            - For EVENT ADD: Expects [id, start_date, start_time, end_date, end_time, description]
            - For TASK ADD: Expects [id, task_time, due_date, due_time, urgency]
            - For BLOCK ADD: Expects [day, start_time, end_time]
            - For REMOVE commands: Expects [id] for EVENT/TASK, [day, start_time, end_time] for BLOCK
            - For MODIFY commands: Expects [id, mod_verb, ...additional_args]
        """

        tokenObj = Tokens(self.location, self.verb)

        if self.verb == "ADD":
            if tokenObj.location == "EVENT":
                tokenObj.iD = self.context[0]
                tokenObj.startTime = TimeUtility(f"{self.context[1]} {self.context[2]}").convertToUTC()
                tokenObj.endTime = TimeUtility(f"{self.context[3]} {self.context[4]}").convertToUTC()
                tokenObj.description = self.context[5]
                return tokenObj

            elif tokenObj.location == "TASK":
                tokenObj.iD = self.context[0]
                tokenObj.taskTime = toSeconds(self.context[1])
                tokenObj.dueDate = TimeUtility(f"{self.context[2]} {self.context[3]}").convertToUTC()
                tokenObj.urgency = int(self.context[4])
                return tokenObj

            elif tokenObj.location == "BLOCK":
                tokenObj.blockStart = (86400 * (int(self.context[0]) - 1)) + toSeconds(self.context[1])
                tokenObj.blockEnd = (86400 * (int(self.context[0]) - 1)) + toSeconds(self.context[2])
                return tokenObj

            else:
                raise Exception("Invalid command. Do it right.")

        elif self.verb == "REMOVE":
            if tokenObj.location == "EVENT":
                tokenObj.iD = self.context[0]
                return tokenObj

            elif tokenObj.location == "TASK":
                tokenObj.iD = self.context[0]
                return tokenObj

            elif tokenObj.location == "BLOCK":
                tokenObj.blockStart = (86400 * (int(self.context[0]) - 1)) + toSeconds(self.context[1])
                tokenObj.blockEnd = (86400 * (int(self.context[0]) - 1)) + toSeconds(self.context[2])
                return tokenObj

            else:
                raise Exception("Invalid command. Do it right.")

        elif self.verb == "MODIFY":
            tokenObj.iD = self.context[0]
            tokenObj.modVerb = self.context[1]

            if tokenObj.location == "EVENT":
                if tokenObj.modVerb == "DISC":
                    tokenObj.modVerb = "description"
                    tokenObj.modContext = self.context[2]
                    return tokenObj

                elif tokenObj.modVerb == "STARTTIME":
                    tokenObj.modVerb = "unixtimeStart"
                    tokenObj.modContext = TimeUtility(f"{self.context[2]} {self.context[3]}").convertToUTC()
                    return tokenObj

                elif tokenObj.modVerb == "ENDTIME":
                    tokenObj.modVerb = "unixtimeEnd"
                    tokenObj.modContext = TimeUtility(f"{self.context[2]} {self.context[3]}").convertToUTC()
                    return tokenObj
                else:
                    raise Exception("Invalid command. Do it right.")

            elif tokenObj.location == "TASK":
                if tokenObj.modVerb == "DUEDATE":
                    tokenObj.modVerb = "dueDate"
                    tokenObj.modContext = TimeUtility(f"{self.context[2]} {self.context[3]}").convertToUTC()
                    return tokenObj

                elif tokenObj.modVerb == "TIME":
                    tokenObj.modVerb = "unixtime"
                    tokenObj.modContext = toSeconds(self.context[2])
                    return tokenObj

                elif tokenObj.modVerb == "URGENCY":
                    tokenObj.modVerb = "urgency"
                    tokenObj.modContext = int(self.context[2])
                    return tokenObj
                else:
                    raise Exception("Invalid command. Do it right.")

            else:
                raise Exception("Invalid command. Do it right.")

        elif self.location == "CALENDAR":
            tokenObj.viewTime = "14 D"
            return tokenObj

        else:
            raise Exception("Invalid command. Do it right.")

    def __init__(self, command):
        """
        Initialize a CommandTokenizer instance and parse the given command.

        This constructor takes a command string, parses it into tokens, extracts
        the location and verb, gets the context, and creates a fully populated
        Tokens object that can be used by other parts of the application.

        Args:
            command (str): The command string to parse. Should follow the format:
                          "<LOCATION> <VERB> <context_arguments>"
                          where LOCATION is EVENT/TASK/BLOCK/CALENDAR,
                          VERB is ADD/REMOVE/MODIFY/etc., and context_arguments
                          are the specific parameters for the command.

        Attributes:
            self.tokens (list): The parsed command tokens
            self.location (str): The command location/type (first token)
            self.verb (str): The command verb/action (second token)
            self.context (list): The command arguments (remaining tokens)
            self.tokenObject (Tokens): The fully populated Tokens object

        Raises:
            Exception: If the command format is invalid or cannot be parsed.

        Example:
            >>> tokenizer = CommandTokenizer('EVENT ADD meeting 25/12/2023 14:00 25/12/2023 15:00 "Team meeting"')
            >>> tokenizer.location  # 'EVENT'
            >>> tokenizer.verb      # 'ADD'
        """
        try:
            self.tokens = self._parseCommand(command)
            self.location = self.tokens[0]
            self.verb = self.tokens[1]
            self.context = self._getContext(self.tokens)
            self.tokenObject = self._createTokenObject()
        except:
            self.tokenObject = None
