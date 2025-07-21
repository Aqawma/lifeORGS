import random

from utils.jsonUtils import Configs


class ColorGenerator:
    def __init__(self):
        self.colorChoices = tuple(Configs().colorSchemes.keys())

    def generateColor(self):
        return random.choice(self.colorChoices)

    def generateColorList(self, numColors):
        colorList = []

        for i in range(numColors):
            tentColor = self.generateColor()

            if len(colorList) != 0:
                while tentColor == colorList[i-1]:
                    tentColor = self.generateColor()
            colorList.append(tentColor)

        return tuple(colorList)
