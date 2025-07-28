from userInteraction.parsing.tokenize import Tokens
from utils.timeUtilitities.startAndEndBlocks import TimeStarts
from utils.timeUtilitities.timeUtil import TimeConverter
from whatsappSecrets.initSecrets import SecretCreator


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
        self.returnMessage = self.returnConfirm()

    def returnConfirm(self):
        siteLink = SecretCreator().loadSecrets()["SITE_LINK"]

        if self.tokens.location == "BLOCK":
            referenceTime = TimeStarts(generationTime=TimeConverter().currentTime).thisWeek["start"]
            referencedBlockStart = TimeConverter(unixtime=referenceTime + self.tokens.blockStart).generateTimeDataObj()
            referencedBlockEnd = TimeConverter(unixtime=referenceTime + self.tokens.blockEnd).generateTimeDataObj()

            if referencedBlockStart.dayOfWeek != referencedBlockEnd.dayOfWeek:
                blockStartStr = (f"{referencedBlockStart.dayOfWeek} at "
                                 f"{referencedBlockStart.hour}:{referencedBlockStart.minute:02d}")
                blockEndStr = (f"{referencedBlockEnd.dayOfWeek} at "
                               f"{referencedBlockEnd.hour}:{referencedBlockEnd.minute:02d}")
            else:
                blockStartStr = (f"{referencedBlockStart.dayOfWeek} at "
                                 f"{referencedBlockStart.hour}:{referencedBlockStart.minute:02d}")
                blockEndStr = f"{referencedBlockEnd.hour}:{referencedBlockEnd.minute}"

            message = f"Block from {blockStartStr} to {blockEndStr} {PastTense.past(self.tokens.verb)} successfully."

        elif self.tokens.verb == "VIEW":
            message = f"Please view your calendar using the link below: \n{siteLink}"

        elif self.tokens.verb == "SCHEDULE":
            conflicts = 0  # TODO add a way to check for conflicts
            message = (f"Your tasks have been scheduled successfully and {conflicts} conflicts were found. "
                       f"Please view your calendar using the link below: \n{siteLink}")

        else:
            message = (f"{self.tokens.location.capitalize()}: "
                       f"{self.tokens.iD} {PastTense.past(self.tokens.verb)} successfully.")

        return message
