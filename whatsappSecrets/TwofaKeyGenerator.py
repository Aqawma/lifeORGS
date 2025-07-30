import secrets
import hashlib
import json
import os

from utils.timeUtilitities.timeDataClasses import UnixTimePeriods
from utils.timeUtilitities.timeUtil import TimeConverter


class TwoFAKey:
    def __init__(self):
        self.keyFilePath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tfaKey.json')

    def generate2faKey(self):
        rawHash = hashlib.sha256(str(secrets.randbits(256)).encode()).hexdigest()[:64]
        tfaKey = ''.join([secrets.choice(rawHash) for _ in range(6)])

        tfaDict = {
            "key": tfaKey,
            "genTime": TimeConverter().currentTime,
            "expTime": TimeConverter().currentTime + (10 * UnixTimePeriods.minute)
        }

        with open(self.keyFilePath, "w") as f:
            json.dump(tfaDict, f, indent=4)

        return tfaKey

    def view2faKey(self):
        try:
            with open(self.keyFilePath, "r") as f:
                tfaDict = json.load(f)

            return tfaDict['key']

        except FileNotFoundError:
            raise FileNotFoundError("No key generated yet. Please generate a key first.")

    def check2faKey(self, key):
        try:
            with open(self.keyFilePath, "r") as f:
                tfaDict = json.load(f)

            if key == tfaDict['key'] and tfaDict['genTime'] < TimeConverter().currentTime < tfaDict['expTime']:
                return True
            else:
                return False

        except FileNotFoundError:
            raise FileNotFoundError("No key generated yet. Please generate a key first.")
