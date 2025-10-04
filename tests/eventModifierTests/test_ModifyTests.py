# import unittest
#
# from tests.TestUtils.makeTestDB import TestDBUtils
# from tests.TestUtils.testEnv import setTestEnv
# from userInteraction.parsing.tokenize import Tokens
# from calendarORGS.eventModifiers.tokenModify import TokenModify
# from utils.dbUtils import ConnectDB
# from utils.timeUtilitities.timeUtil import TimeConverter
#
# @setTestEnv
# class ModifyTests(unittest.TestCase):
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#
#         self.tokenEventDisc = Tokens('EVENT',
#                                      'MODIFY',
#                                      iD='Doctor Appointment',
#                                      modVerb='description',
#                                      modContext='Biannual Doctors Appointment')
#         self.tokenEventStartTime = Tokens('EVENT',
#                                           'MODIFY',
#                                           iD='Doctor Appointment',
#                                           modVerb='unixtimeStart',
#                                           modContext=
#                                           TimeConverter("09/07/2025 14:00").convertToUTC())
#         self.tokenEventEndTime = Tokens('EVENT',
#                                         'MODIFY',
#                                         iD='Doctor Appointment',
#                                         modVerb='unixtimeEnd',
#                                         modContext=
#                                         TimeConverter("09/07/2025 15:00").convertToUTC())
#         self.tokenTaskTaskTime = Tokens('TASK',
#                                         'MODIFY',
#                                         iD='Write Essay',
#                                         modVerb='unixtime',
#                                         modContext=9000)
#         self.tokenTaskUrgency = Tokens('TASK',
#                                        'MODIFY',
#                                        iD='Write Essay',
#                                        modVerb='urgency',
#                                        modContext=5)
#         self.tokenTaskDueDate = Tokens('TASK',
#                                        'MODIFY',
#                                        iD='Write Essay',
#                                        modVerb='dueDate',
#                                        modContext=
#                                        TimeConverter("09/07/2025 15:00").convertToUTC())
#         self.tokenTaskScheduled = Tokens('TASK',
#                                          'MODIFY',
#                                          iD='Send Email',
#                                          modVerb='urgency',
#                                          modContext=5)
#
#     def test_modifyEvent(self):
#         connector = ConnectDB()
#         TestDBUtils.makeTestDB()
#
#         print(f"For tokenEventDisc\n"
#               f"Expected: modVerb:description modContext:Biannual Doctors Appointment")
#         modifyEventDiscObj = TokenModify(self.tokenEventDisc)
#         modifyEventDiscObj.modifyEvent()
#
#         print(f"For tokenEventStartTime\n"
#               f"Expected: modVerb:unixtimeStart modContext:{self.tokenEventStartTime.modContext}")
#         modifyEventStartTimeObj = TokenModify(self.tokenEventStartTime)
#         modifyEventStartTimeObj.modifyEvent()
#
#         print(f"For tokenEventEndTime\nExpected: "
#               f"modVerb:unixtimeEnd "
#               f"modContext:{self.tokenEventEndTime.modContext}")
#         modifyEventEndTimeObj = TokenModify(self.tokenEventEndTime)
#         modifyEventEndTimeObj.modifyEvent()
#
#         connector.cursor.execute("SELECT description, unixtimeStart, unixtimeEnd FROM events WHERE event=?",
#                                  (self.tokenEventDisc.iD,))
#         modifiedDescription = connector.cursor.fetchone()
#
#         self.assertEqual(modifiedDescription[0], self.tokenEventDisc.modContext)
#         self.assertEqual(modifiedDescription[1], self.tokenEventStartTime.modContext)
#         self.assertEqual(modifiedDescription[2], self.tokenEventEndTime.modContext)
#
#     def test_modifyTask(self):
#         connector = ConnectDB()
#         TestDBUtils.makeTestDB()
#
#         print(f"For tokenTaskTaskTime\nExpected: modVerb: taskTime modContext: {self.tokenTaskTaskTime.modContext} ")
#         modifyTaskTaskTimeObj = TokenModify(self.tokenTaskTaskTime)
#         modifyTaskTaskTimeObj.modifyTask()
#
#         print(f"For tokenTaskUrgency\nExpected: modVerb: urgency modContext: {self.tokenTaskUrgency.modContext}")
#         modifyTaskUrgencyObj = TokenModify(self.tokenTaskUrgency)
#         modifyTaskUrgencyObj.modifyTask()
#
#         print(f"For tokenTaskDueDate\nExpected: modVerb: dueDate modContext: {self.tokenTaskDueDate.modContext}")
#         modifyTaskDueDateObj = TokenModify(self.tokenTaskDueDate)
#         modifyTaskDueDateObj.modifyTask()
#
#         connector.cursor.execute("SELECT unixtime, urgency, dueDate FROM tasks WHERE task=?",
#                                  (self.tokenTaskTaskTime.iD,))
#         modifiedTaskTime = connector.cursor.fetchone()
#
#         self.assertEqual(modifiedTaskTime[0], self.tokenTaskTaskTime.modContext)
#         self.assertEqual(modifiedTaskTime[1], self.tokenTaskUrgency.modContext)
#         self.assertEqual(modifiedTaskTime[2], self.tokenTaskDueDate.modContext)
#
#     def test_unscheduleModifiedTask(self):
#         connector = ConnectDB()
#         TestDBUtils.makeTestDB()
#
#         print(f"")
#         modifyTaskScheduledObj = TokenModify(self.tokenTaskScheduled)
#         modifyTaskScheduledObj.modifyTask()
#
#         connector.cursor.execute("SELECT * FROM events WHERE event=?", (self.tokenTaskScheduled.iD,))
#         scheduled = connector.cursor.fetchone()
#         self.assertEqual(scheduled, None)
#         connector.cursor.execute("SELECT scheduled FROM tasks WHERE task=?", (self.tokenTaskScheduled.iD,))
#         scheduled = connector.cursor.fetchone()
#         self.assertEqual(scheduled[0], 0)
#
#
# if __name__ == '__main__':
#     unittest.main()
