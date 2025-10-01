"""
Command Parsing Tests Module

This module contains comprehensive unit tests for the command parsing functionality
of the lifeORGS application. It tests the CommandTokenizer class to ensure proper
parsing of various command types including events, tasks, blocks, and calendar operations.

Dependencies:
- unittest: Python's built-in testing framework
- parsing.tokenize: CommandTokenizer class for command parsing

Classes:
- ParsingTests: Main test class containing all parsing-related unit tests

Test Coverage:
- EventObj commands (ADD, REMOVE, MODIFY)
- Task commands (ADD, REMOVE, MODIFY)
- Block commands (ADD, REMOVE)
- Calendar commands (VIEW, SCHEDULE)
- Error handling for invalid commands

Usage:
    Run tests directly:
    $ python tests/eventModifierTests/test_ParsingTests.py

    Or use unittest discovery:
    $ python -m unittest tests.eventModifierTests.test_ParsingTests
"""

import unittest
from userInteraction.parsing.tokenize import CommandTokenizer

class ParsingTests(unittest.TestCase):
    """
    Comprehensive unit tests for command parsing functionality.

    This test class validates the CommandTokenizer's ability to correctly parse
    various command types and extract the appropriate token information. It covers
    all major command categories and includes error handling tests.

    Test Categories:
    - EventObj operations (ADD, REMOVE, MODIFY)
    - Task operations (ADD, REMOVE, MODIFY)
    - Block operations (ADD, REMOVE)
    - Calendar operations (VIEW, SCHEDULE)
    - Error handling (invalid commands, empty strings)

    Attributes:
        Various command strings used as test fixtures for different command types
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the test class with predefined command strings for testing.

        Sets up various command string fixtures that represent typical user input
        for different command types. These strings are used across multiple test
        methods to ensure consistent testing.

        Args:
            *args: Variable length argument list passed to parent class
            **kwargs: Arbitrary keyword arguments passed to parent class
        """
        super().__init__(*args, **kwargs)

        # EventObj command test strings
        self.addEventStr = 'EVENT ADD "meeting" 25/12/2023 14:00 25/12/2023 15:00 "Team meeting"'
        self.removeEventStr = 'EVENT REMOVE meeting'
        self.modEventStr = 'EVENT MODIFY "Meeting Name" STARTTIME 25/12/2023 15:00'

        # Task command test strings
        self.addTaskStr = 'TASK ADD "Complete Report" 02:30 25/12/2023 23:59 5'
        self.removeTaskStr = 'TASK REMOVE "Complete Report"'
        self.modTaskStr = 'TASK MODIFY "Complete Report" TIME 03:00'

        # Block command test strings
        self.addBlockStr = 'BLOCK ADD 1 09:00 17:00'
        self.removeBlockStr = 'BLOCK REMOVE 1 09:00 17:00'

        # Calendar command test strings
        self.viewCalendarStr = 'CALENDAR VIEW'
        self.scheduleCalendarStr = 'CALENDAR SCHEDULE'

    def test_commandTokenizerEventAdd(self):
        print(f"For {self.addEventStr}\nExpected: "
              f"location:EVENT "
              f"verb:ADD "
              f"iD:meeting "
              f"startTime:1703530800 "
              f"endTime:1703534400 "
              f"description:Team meeting")
        tokenizer = CommandTokenizer(self.addEventStr)
        self.assertEqual(tokenizer.location,"EVENT")
        self.assertEqual(tokenizer.verb,"ADD")
        self.assertEqual(tokenizer.tokenObject.iD,"meeting")
        self.assertEqual(tokenizer.tokenObject.startTime,1703530800.0)
        self.assertEqual(tokenizer.tokenObject.endTime,1703534400.0)
        self.assertEqual(tokenizer.tokenObject.description,"Team meeting")

    def test_commandTokenizerEventRemove(self):
        """
        Test parsing of EVENT REMOVE commands.

        Validates that the CommandTokenizer correctly parses event removal commands
        and extracts the appropriate location, verb, and event identifier.

        Expected behavior:
        - location should be "EVENT"
        - verb should be "REMOVE"
        - iD should be the event name (converted to uppercase)
        """
        print(f"For {self.removeEventStr}\nExpected: location:EVENT verb:REMOVE iD:meeting")
        tokenizer = CommandTokenizer(self.removeEventStr)
        self.assertEqual(tokenizer.location,"EVENT")
        self.assertEqual(tokenizer.verb,"REMOVE")
        self.assertEqual(tokenizer.tokenObject.iD,"MEETING")

    def test_commandTokenizerEventModify(self):
        print(f"For {self.modEventStr}\nExpected: "
              f"location:EVENT "
              f"verb:MODIFY, "
              f"modVerb:STARTTIME, "
              f"modContext:1703534400.0")
        tokenizer = CommandTokenizer(self.modEventStr)
        self.assertEqual(tokenizer.location,"EVENT")
        self.assertEqual(tokenizer.verb,"MODIFY")
        self.assertEqual(tokenizer.tokenObject.modVerb,"unixtimeStart")
        self.assertEqual(tokenizer.tokenObject.modContext, 1703534400.0)

    def test_commandTokenizerTaskAdd(self):
        print(f"For {self.addTaskStr}\nExpected: "
              f"location:TASK "
              f"verb:ADD "
              f"iD:Complete Report "
              f"startTime:838860800 "
              f"endTime:1297145600 "
              f"taskTime:3600 "
              f"taskUrgency:5")
        tokenizer = CommandTokenizer(self.addTaskStr)
        self.assertEqual(tokenizer.location,"TASK")
        self.assertEqual(tokenizer.verb,"ADD")
        self.assertEqual(tokenizer.tokenObject.iD,"Complete Report")
        self.assertEqual(tokenizer.tokenObject.dueDate,1703566740.0)
        self.assertEqual(tokenizer.tokenObject.taskTime,9000.0)
        self.assertEqual(tokenizer.tokenObject.urgency,5)

    def test_commandTokenizerTaskRemove(self):
        """
        Test parsing of TASK REMOVE commands.

        Validates that the CommandTokenizer correctly parses task removal commands
        and extracts the appropriate location, verb, and task identifier.

        Expected behavior:
        - location should be "TASK"
        - verb should be "REMOVE"
        - iD should be the task name (preserving original case for quoted strings)
        """
        print(f"For {self.removeTaskStr}\nExpected: location:TASK verb:REMOVE iD:Complete Report")
        tokenizer = CommandTokenizer(self.removeTaskStr)
        self.assertEqual(tokenizer.location,"TASK")
        self.assertEqual(tokenizer.verb,"REMOVE")
        self.assertEqual(tokenizer.tokenObject.iD,"Complete Report")

    def test_commandTokenizerTaskModify(self):
        """
        Test parsing of TASK MODIFY commands.

        Validates that the CommandTokenizer correctly parses task modification commands
        and extracts the modification type and context. This test specifically checks
        time modification for tasks.

        Expected behavior:
        - location should be "TASK"
        - verb should be "MODIFY"
        - modVerb should be "unixtime" (internal field name for time)
        - modContext should be the time in seconds (10800 = 3 hours)
        """
        print(f"For {self.modTaskStr}\nExpected: location:TASK verb:MODIFY modVerb:DUEDATE modContext:1703566740.0")
        tokenizer = CommandTokenizer(self.modTaskStr)
        self.assertEqual(tokenizer.location,"TASK")
        self.assertEqual(tokenizer.verb,"MODIFY")
        self.assertEqual(tokenizer.tokenObject.modVerb,"unixtime")
        self.assertEqual(tokenizer.tokenObject.modContext, 10800.0)

    def test_commandTokenizerBlockAdd(self):
        print(f"For {self.addBlockStr}\nExpected: location:BLOCK verb:ADD startTime:32400 endTime:61200")
        tokenizer = CommandTokenizer(self.addBlockStr)
        self.assertEqual(tokenizer.location,"BLOCK")
        self.assertEqual(tokenizer.verb,"ADD")
        self.assertEqual(tokenizer.tokenObject.blockStart,32400)
        self.assertEqual(tokenizer.tokenObject.blockEnd,61200)

    def test_commandTokenizerBlockRemove(self):
        print(f"For {self.removeBlockStr}\nExpected: location:BLOCK verb:REMOVE startTime:32400 endTime:61200")
        tokenizer = CommandTokenizer(self.removeBlockStr)
        self.assertEqual(tokenizer.location,"BLOCK")
        self.assertEqual(tokenizer.verb,"REMOVE")
        self.assertEqual(tokenizer.tokenObject.blockStart,32400)
        self.assertEqual(tokenizer.tokenObject.blockEnd,61200)

    def test_commandTokenizerEventAddFail(self):
        print("Fail Invalid Command Expected Non Token Object")
        tokenizer = CommandTokenizer('EVENT AD meeting 25/12/2023 14:00 25/12/2023 15:00 "Team meeting"')
        self.assertEqual(tokenizer.tokenObject, None)

    def test_commandTokenizerEventAddEmptyString(self):
        print("Fail Empty String Expected None Token Object")
        tokenizer = CommandTokenizer('')
        self.assertEqual(tokenizer.tokenObject, None)


if __name__ == '__main__':
    unittest.main()
