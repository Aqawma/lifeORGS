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
    """
    Singleton configuration manager for the lifeORGS application.

    This class implements the singleton pattern to ensure that configuration files
    are loaded only once and shared across the entire application. It manages both
    the main application configuration and color schemes for calendar generation.

    Attributes:
        configDirPath (Path): Path to the configurations directory
        mainConfig (dict): Main application configuration from config.json
        colorSchemes (dict): Color scheme configuration from colorSchemes.json

    Example:
        # Get configuration instance (creates singleton if first time)
        config = Configs()

        # Access main configuration
        database_name = config.mainConfig['DATABASE_NAME']

        # Access color schemes
        primary_colors = config.colorSchemes['primary']
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        Create or return the singleton instance of the Configs class.

        Implements the singleton pattern to ensure only one instance of the
        configuration manager exists throughout the application lifecycle.

        Returns:
            Configs: The singleton instance of the Configs class
        """
        if cls._instance is None:
            cls._instance = super(Configs, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """
        Initialize the configuration manager and load configuration files.

        Sets up the path to the configurations directory and initializes empty
        dictionaries for configuration data. Automatically loads configuration
        files on first instantiation.

        Note:
            Due to singleton pattern, __init__ may be called multiple times but
            configuration loading is protected against redundant operations.
        """
        self.configDirPath = Path(getProjRoot()) / "configurations"

        self.mainConfig: dict = {}
        self.colorSchemes: dict = {}

        self._loadConfig()

    def _loadConfig(self) -> None:
        """
        Load configuration files from the configurations directory.

        Loads both config.json (main application configuration) and 
        colorSchemes.json (color schemes for calendar generation) if they
        haven't been loaded already. This method is protected against
        redundant loading.

        Raises:
            FileNotFoundError: If configuration files are not found
            json.JSONDecodeError: If configuration files contain invalid JSON
            PermissionError: If configuration files cannot be read
        """
        if not self.mainConfig or not self.colorSchemes:

            with open(self.configDirPath / "config.json") as f:
                self.mainConfig = json.load(f)

            with open(self.configDirPath / "colorSchemes.json") as f:
                self.colorSchemes = json.load(f)
