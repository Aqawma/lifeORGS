from userInteraction.parsing.tokenize import Tokens
from utils.timeUtilitities.startAndEndBlocks import TimeStarts
from utils.timeUtilitities.timeUtil import TimeConverter


class PastTense:
    verbMap = {
        "ADD": "added",
        "REMOVE": "removed",
        "MODIFY": "modified",
        "SCHEDULE": "scheduled",
        "VIEW": "viewed"
    }

    @staticmethod
    def past(verb):
        return PastTense.verbMap[verb]

class TokenReturns:
    def __init__(self, tokenObject: Tokens):
        self.tokens = tokenObject
        print(vars(self.tokens))

    def returnConfirm(self):
        if self.tokens.location == "BLOCK":
            referenceTime = TimeStarts(generationTime=TimeConverter().currentTime).thisWeek["start"]
            referencedBlockStart = TimeConverter(unixtime=referenceTime + self.tokens.blockStart).generateTimeDataObj()
            referencedBlockEnd = TimeConverter(unixtime=referenceTime + self.tokens.blockEnd).generateTimeDataObj()

            if referencedBlockStart.dayOfWeek != referencedBlockEnd.dayOfWeek:
                blockStartStr = (f"{referencedBlockStart.dayOfWeek} at "
                                 f"{referencedBlockStart.hour}:{referencedBlockStart.minute}")
                blockEndStr = (f"{referencedBlockEnd.dayOfWeek} at "
                               f"{referencedBlockEnd.hour}:{referencedBlockEnd.minute}")
            else:
                blockStartStr = (f"{referencedBlockStart.day} at "
                                 f"{referencedBlockStart.hour}:{referencedBlockStart.minute}")
                blockEndStr = f"{referencedBlockEnd.hour}:{referencedBlockEnd.minute}"

            message = f"Block from {blockStartStr} to {blockEndStr} {PastTense.past(self.tokens.verb)} successfully."

        elif self.tokens.verb == "VIEW":
            message = "Please view your calendar using the link below:"
            # TODO calendar link will go here!!

        elif self.tokens.verb == "SCHEDULE":
            conflicts = 0  # TODO add a way to check for conflicts
            message = (f"Your tasks have been scheduled successfully and {conflicts} conflicts were found. "
                       f"Please view your calendar using the link below:")
            # TODO calendar link will go here!!

        else:
            message = f"{self.tokens.location.capitalize()} {PastTense.past(self.tokens.verb)} successfully."

        return message
