import unittest
from parsing.tokenize import CommandTokenizer

class tokenizeTests(unittest.TestCase):

    def test_commandTokenizerEventAdd(self):
        print("For \'EVENT ADD meeting 25/12/2023 14:00 25/12/2023 15:00 \"Team meeting\"\' Expected value for location is EVENT and verb is ADD")
        tokenizer = CommandTokenizer('EVENT ADD meeting 25/12/2023 14:00 25/12/2023 15:00 "Team meeting"')
        self.assertEqual(tokenizer.location,"EVENT")
        self.assertEqual(tokenizer.verb,"ADD")

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