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
import os

def loadConfig() -> dict:
    """
    Loads the application configuration from config.json file.

    This function locates and loads the main configuration file from the project
    root directory. It uses relative path resolution to ensure the config file
    is found regardless of the current working directory.

    Returns:
        dict: Dictionary containing all configuration settings from config.json

    Raises:
        FileNotFoundError: If config.json is not found in the project root
        json.JSONDecodeError: If config.json contains invalid JSON syntax

    Example:
        >>> config = loadConfig()
        >>> access_token = config['ACCESS_TOKEN']
        >>> db_path = config['DATABASE_PATH']

    Note:
        - The config.json file should be located in the project root directory
        - Path resolution works from the utils/ subdirectory up to project root
        - Configuration keys are case-sensitive
    """
    # Navigate from utils/ directory up to project root where config.json is located
    configPath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'configurations', 'config.json')

    # Load and parse the JSON configuration file
    with open(configPath) as f:
        config = json.load(f)

    return config

class Configs:
    def __init__(self):
        self.configDirPath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'configurations')
        self.mainConfig: dict = loadConfig()
        self.colorSchemes: dict = self._colorScheme()

    def _colorScheme(self) -> dict:
        with open(os.path.join(self.configDirPath, 'colorSchemes.json')) as f:
            colorSchemes = json.load(f)
        return colorSchemes
