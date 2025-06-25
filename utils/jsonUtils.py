import json
import os

def loadConfig():
    # Go up one directory from utils/ to reach the project root where config.json is located
    configPath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')
    with open(configPath) as f:
        config = json.load(f)
    return config
