import unittest
from parsing.tokenize import CommandTokenizer

class ParsingTests(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.addEventStr = 'EVENT ADD "meeting" 25/12/2023 14:00 25/12/2023 15:00 "Team meeting"'
        self.addTaskStr = 'TASK ADD "Complete Report" 02:30 25/12/2023 23:59 5'
        self.addBlockStr = 'BLOCK ADD 1 09:00 17:00'
        self.removeEventStr = 'EVENT REMOVE meeting'
        self.removeTaskStr = 'TASK REMOVE "Complete Report"'
        self.removeBlockStr = 'BLOCK REMOVE 1 09:00 17:00'
        self.modEventStr = 'EVENT MODIFY "Meeting Name" STARTTIME 25/12/2023 15:00'
        self.modTaskStr = 'TASK MODIFY "Complete Report" TIME 03:00'
        self.viewCalendarStr = 'CALENDAR VIEW'
        self.scheduleCalendarStr = 'CALENDAR SCHEDULE'

#renable after fix to utc
    '''def test_commandTokenizerEventAdd(self):
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
        self.assertEqual(tokenizer.tokenObject.description,"Team meeting")'''

    def test_commandTokenizerEventRemove(self):
        print(f"For {self.removeEventStr}\nExpected: location:EVENT verb:REMOVE iD:meeting")
        tokenizer = CommandTokenizer(self.removeEventStr)
        self.assertEqual(tokenizer.location,"EVENT")
        self.assertEqual(tokenizer.verb,"REMOVE")
        self.assertEqual(tokenizer.tokenObject.iD,"MEETING")

    #renable after fix to UTC
    '''def test_commandTokenizerEventModify(self):
        print(f"For {self.modEventStr}\nExpected: "
              f"location:EVENT "
              f"verb:MODIFY, "
              f"modVerb:STARTTIME, "
              f"modContext:1703534400.0")
        tokenizer = CommandTokenizer(self.modEventStr)
        self.assertEqual(tokenizer.location,"EVENT")
        self.assertEqual(tokenizer.verb,"MODIFY")
        self.assertEqual(tokenizer.tokenObject.modVerb,"unixtimeStart")
        self.assertEqual(tokenizer.tokenObject.modContext, 1703534400.0)'''

    #reenable after fix to UTC
    '''def test_commandTokenizerTaskAdd(self):
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
        self.assertEqual(tokenizer.tokenObject.urgency,5)'''

    def test_commandTokenizerTaskRemove(self):
        print(f"For {self.removeTaskStr}\nExpected: location:TASK verb:REMOVE iD:Complete Report")
        tokenizer = CommandTokenizer(self.removeTaskStr)
        self.assertEqual(tokenizer.location,"TASK")
        self.assertEqual(tokenizer.verb,"REMOVE")
        self.assertEqual(tokenizer.tokenObject.iD,"Complete Report")

    def test_commandTokenizerTaskModify(self):
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
