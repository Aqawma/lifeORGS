"""
JSON Configuration Utilities Module

This module provides utilities for loading and managing JSON configuration files
for the lifeORGS application. It handles path resolution to ensure configuration
files are loaded correctly regardless of the current working directory.

Dependencies:
- json: For parsing JSON configuration files
- os: For file path operations and directory navigation

Configuration File:
The module expects a config.json file in the project root directory containing
application settings such as API tokens, database paths, and other configuration
parameters.
"""

import json
from pathlib import Path

from utils.projRoot import getProjRoot

class Configs:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Configs, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.configDirPath = Path(getProjRoot()) / "configurations"

        self.mainConfig: dict = {}
        self.colorSchemes: dict = {}

        self._loadConfig()

    def _loadConfig(self) -> None:
        if not self.mainConfig or not self.colorSchemes:

            with open(self.configDirPath / "config.json") as f:
                self.mainConfig = json.load(f)

            with open(self.configDirPath / "colorSchemes.json") as f:
                self.colorSchemes = json.load(f)
