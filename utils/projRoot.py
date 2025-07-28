import os

def getProjRoot():
    scriptDir = os.path.dirname(os.path.abspath(__file__))
    lifeOrgsRoot = os.path.dirname(scriptDir)
    return lifeOrgsRoot
