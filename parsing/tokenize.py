import re
from utils.timeUtils import toUnixTime, toSeconds

"""
Main module for the lifeORGS application.
This module serves as the command parser for the application, handling various commands
related to events, tasks, and calendar management. It interprets user input and routes
commands to the appropriate functions in other modules.
"""

class Tokens:
    def __init__(self, location: str, verb: str, iD: str = None, modVerb: str = None,
                 startTime: float = None, endTime: float = None, description: str = None,
                 dueDate: float = None, taskTime: float = None, urgency: int = None,
                 blockStart: float = None, blockEnd: float = None,):
        self.location = location
        self.verb = verb
        self.iD = iD
        self.modVerb = modVerb
        self.startTime = startTime
        self.endTime = endTime
        self.description = description
        self.dueDate = dueDate
        self.taskTime = taskTime
        self.urgency = urgency
        self.blockStart = blockStart
        self.blockEnd = blockEnd

class CommandTokenizer:

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
        context = []

        for token in range(len(tokens)):
            if token != 0 and token != 1:
                context.append(tokens[token])
            else:
                continue

        return context

    def _createTokenObject(self):

        tokenObj = Tokens(self.location, self.verb)

        if self.verb == "ADD":
            if tokenObj.location == "EVENT":
                tokenObj.iD = self.context[0]
                tokenObj.startTime = toUnixTime(f"{self.context[1]} {self.context[2]}")
                tokenObj.endTime = toUnixTime(f"{self.context[3]} {self.context[4]}")
                tokenObj.description = self.context[5]
                return tokenObj

            elif tokenObj.location == "TASK":
                tokenObj.iD = self.context[0]
                tokenObj.taskTime = self.context[1]
                tokenObj.dueDate = toUnixTime(f"{self.context[2]} {self.context[3]}")
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
                    tokenObj.description = self.context[2]
                    return tokenObj
                elif tokenObj.modVerb == "STARTTIME":
                    tokenObj.startTime = toUnixTime(f"{self.context[2]} {self.context[3]}")
                    return tokenObj
                elif tokenObj.modVerb == "ENDTIME":
                    tokenObj.endTime = toUnixTime(f"{self.context[2]} {self.context[3]}")
                    return tokenObj
                else:
                    raise Exception("Invalid command. Do it right.")

            elif tokenObj.location == "TASK":
                if tokenObj.modVerb == "DUEDATE":
                    tokenObj.dueDate = toUnixTime(f"{self.context[2]} {self.context[3]}")
                    return tokenObj
                elif tokenObj.modVerb == "TIME":
                    tokenObj.taskTime = self.context[2]
                    return tokenObj
                elif tokenObj.modVerb == "URGENCY":
                    tokenObj.urgency = int(self.context[2])
                    return tokenObj
                else:
                    raise Exception("Invalid command. Do it right.")

            else:
                raise Exception("Invalid command. Do it right.")

        else:
            raise Exception("Invalid command. Do it right.")

        # TODO Calendar scheduling

    def __init__(self, command):
        self.tokens = self._parseCommand(command)
        self.location = self.tokens[0]
        self.verb = self.tokens[1]
        self.context = self._getContext(self.tokens)
        self.tokenObject = self._createTokenObject()
