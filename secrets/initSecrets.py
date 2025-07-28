"""
Secrets Initialization Module

This module provides functionality for creating and managing the secrets.json file
that contains API tokens and configuration secrets for the lifeORGS application.
It handles the interactive creation of secrets files and provides secure loading
of existing secrets.

Dependencies:
- os: For file path operations and directory management
- json: For JSON file creation and parsing

Classes:
- SecretCreator: Main class for secrets file management

Usage:
    This module can be run directly to create a new secrets.json file:
    $ python secrets/initSecrets.py

    Or imported and used programmatically:
    # >>> from secrets.initSecrets import SecretCreator
    # >>> creator = SecretCreator()
    # >>> secrets = creator.loadedSecrets
"""

import os
import json

class SecretCreator:
    """
    Manages the creation and loading of secrets.json file for API configuration.

    This class handles the interactive creation of a secrets.json file containing
    WhatsApp Business API tokens and other configuration secrets. It provides
    functionality to create new secrets files and load existing ones with
    proper error handling.

    Attributes:
        secretPath (str): Full path to the secrets.json file
        secretBool (bool): Whether the secrets.json file exists
        loadedSecrets (dict): Dictionary containing loaded secrets data

    Example:
        >>> creator = SecretCreator()
        >>> access_token = creator.loadedSecrets.get('ACCESS_TOKEN')
        >>> print(f"Access token: {access_token}")
    """

    def __init__(self):
        """
        Initialize the SecretCreator and handle secrets file creation/loading.

        Sets up the path to secrets.json, checks if it exists, creates it if needed,
        and loads the secrets data into memory.
        """
        # Construct path to secrets.json in the same directory as this script
        self.secretPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'secrets.json')

        # Check if secrets file already exists
        self.secretBool = os.path.exists(self.secretPath)

        # Create secrets file if it doesn't exist
        self.createSecrets() if not self.secretBool else None

        # Load secrets data into memory
        self.loadedSecrets = self.loadSecrets()

    def createSecrets(self):
        """
        Interactively creates a new secrets.json file with WhatsApp API configuration.

        Prompts the user for all required WhatsApp Business API tokens and configuration
        values, then creates a properly formatted JSON file. If a secrets file already
        exists, asks for confirmation before overwriting.

        Required secrets collected:
        - APP_ID: WhatsApp Business App ID
        - APP_SECRET: WhatsApp Business App Secret
        - RECIPIENT_WAID: Default recipient WhatsApp ID
        - VERSION: WhatsApp API version
        - PHONE_NUMBER_ID: WhatsApp Business Phone Number ID
        - VERIFY_TOKEN: Webhook verification token
        - ACCESS_TOKEN: WhatsApp Business API access token

        Note:
            This method uses input() for interactive prompts, making it suitable
            for command-line usage but not for automated scripts.
        """
        overwriteConfirm = "y"

        # If secrets file exists, ask for confirmation to overwrite
        if self.secretBool:
            overwriteConfirm = input("A secrets.json file already exists. Do you want to overwrite it? (y/n): ")

        if overwriteConfirm == "y":
            # Ensure the secrets directory exists
            os.makedirs(os.path.dirname(self.secretPath), exist_ok=True)

            # Collect all required API tokens and configuration values
            print("Please enter your WhatsApp Business API configuration:")
            APP_ID = input("Enter your app ID: ")
            APP_SECRET = input("Enter your app secret: ")
            RECIPIENT_WAID = input("Enter your recipient WaID: ")
            VERSION = input("Enter your version: ")
            PHONE_NUMBER_ID = input("Enter your phone number ID: ")
            VERIFY_TOKEN = input("Enter your verify token: ")
            ACCESS_TOKEN = input("Enter your access token: ")

            # Create secrets dictionary with all configuration values
            secrets = {
                "APP_ID": APP_ID,
                "APP_SECRET": APP_SECRET,
                "RECIPIENT_WAID": RECIPIENT_WAID,
                "VERSION": VERSION,
                "PHONE_NUMBER_ID": PHONE_NUMBER_ID,
                "VERIFY_TOKEN": VERIFY_TOKEN,
                "ACCESS_TOKEN": ACCESS_TOKEN
            }

            # Write secrets to JSON file with proper formatting
            with open(self.secretPath, 'w') as f:
                json.dump(secrets, f, indent=4)

            print(f"Secrets file created successfully at: {self.secretPath}")

        else:
            print("Operation cancelled.")

    def loadSecrets(self):
        """
        Loads secrets from the secrets.json file with comprehensive error handling.

        Attempts to read and parse the secrets.json file, returning the configuration
        data as a dictionary. Provides detailed error messages for common issues
        like missing files or invalid JSON format.

        Returns:
            dict: Dictionary containing all secrets and configuration values,
                  or empty dict if loading fails

        Raises:
            No exceptions are raised - all errors are handled gracefully with
            appropriate error messages printed to console.

        Example:
            # >>> creator = SecretCreator()
            # >>> secrets = creator.loadSecrets()
            # >>> access_token = secrets.get('ACCESS_TOKEN', 'default_token')
        """
        try:
            # Attempt to read and parse the secrets file
            with open(self.secretPath, 'r') as f:
                secrets = json.load(f)
            return secrets

        except FileNotFoundError:
            # Handle case where secrets.json doesn't exist
            print(f"Error: secrets.json not found at {self.secretPath}")
            print("Please run the script again to create the secrets file.")
            return {}

        except json.JSONDecodeError:
            # Handle case where secrets.json contains invalid JSON
            print(f"Error: Invalid JSON in secrets file at {self.secretPath}")
            print("Please check the file format or recreate the secrets file.")
            return {}


if __name__ == "__main__":
    """
    Main execution block for interactive secrets file creation.

    When this module is run directly, it creates a SecretCreator instance
    which will interactively prompt for API configuration if no secrets
    file exists, then displays the loaded secrets for verification.

    Usage:
        $ python secrets/initSecrets.py
    """
    print("lifeORGS Secrets Initialization")
    print("=" * 35)

    # Create SecretCreator instance (will prompt for secrets if needed)
    secretCreator = SecretCreator()

    # Display loaded secrets for verification (tokens will be visible)
    print("\nLoaded secrets configuration:")
    if secretCreator.loadedSecrets:
        for key, value in secretCreator.loadedSecrets.items():
            # Mask sensitive tokens for security (show only first/last few characters)
            if 'TOKEN' in key or 'SECRET' in key:
                masked_value = f"{value[:4]}...{value[-4:]}" if len(value) > 8 else "***"
                print(f"  {key}: {masked_value}")
            else:
                print(f"  {key}: {value}")
    else:
        print("  No secrets loaded - please check for errors above.")
