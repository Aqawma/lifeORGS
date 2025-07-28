"""
Secrets Initialization Module

This module provides functionality for creating and managing the whatsappSecrets.json file
that contains API tokens and configuration whatsappSecrets for the lifeORGS application.
It handles the interactive creation of whatsappSecrets files and provides secure loading
of existing whatsappSecrets.

Dependencies:
- os: For file path operations and directory management
- json: For JSON file creation and parsing

Classes:
- SecretCreator: Main class for whatsappSecrets file management

Usage:
    This module can be run directly to create a new whatsappSecrets.json file:
    $ python whatsappSecrets/initSecrets.py

    Or imported and used programmatically:
    # >>> from whatsappSecrets.initSecrets import SecretCreator
    # >>> creator = SecretCreator()
    # >>> whatsappSecrets = creator.loadedSecrets
"""

import os
import json

class SecretCreator:
    """
    Manages the creation and loading of whatsappSecrets.json file for API configuration.

    This class handles the interactive creation of a whatsappSecrets.json file containing
    WhatsApp Business API tokens and other configuration whatsappSecrets. It provides
    functionality to create new whatsappSecrets files and load existing ones with
    proper error handling.

    Attributes:
        secretPath (str): Full path to the whatsappSecrets.json file
        secretBool (bool): Whether the whatsappSecrets.json file exists
        loadedSecrets (dict): Dictionary containing loaded whatsappSecrets data

    Example:
        >>> creator = SecretCreator()
        >>> access_token = creator.loadedSecrets.get('ACCESS_TOKEN')
        >>> print(f"Access token: {access_token}")
    """

    def __init__(self):
        """
        Initialize the SecretCreator and handle whatsappSecrets file creation/loading.

        Sets up the path to whatsappSecrets.json, checks if it exists, creates it if needed,
        and loads the whatsappSecrets data into memory.
        """
        # Construct path to whatsappSecrets.json in the same directory as this script
        self.secretPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'whatsappSecrets.json')

        # Check if whatsappSecrets file already exists
        self.secretBool = os.path.exists(self.secretPath)

        # Create whatsappSecrets file if it doesn't exist
        self.createSecrets() if not self.secretBool else None

        # Load whatsappSecrets data into memory
        self.loadedSecrets = self.loadSecrets()

    def createSecrets(self):
        """
        Interactively creates a new whatsappSecrets.json file with WhatsApp API configuration.

        Prompts the user for all required WhatsApp Business API tokens and configuration
        values, then creates a properly formatted JSON file. If a whatsappSecrets file already
        exists, asks for confirmation before overwriting.

        Required whatsappSecrets collected:
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

        # If whatsappSecrets file exists, ask for confirmation to overwrite
        if self.secretBool:
            overwriteConfirm = input("A whatsappSecrets.json file already exists. Do you want to overwrite it? (y/n): ")

        if overwriteConfirm == "y":
            # Ensure the whatsappSecrets directory exists
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

            # Create whatsappSecrets dictionary with all configuration values
            secrets = {
                "APP_ID": APP_ID,
                "APP_SECRET": APP_SECRET,
                "RECIPIENT_WAID": RECIPIENT_WAID,
                "VERSION": VERSION,
                "PHONE_NUMBER_ID": PHONE_NUMBER_ID,
                "VERIFY_TOKEN": VERIFY_TOKEN,
                "ACCESS_TOKEN": ACCESS_TOKEN
            }

            # Write whatsappSecrets to JSON file with proper formatting
            with open(self.secretPath, 'w') as f:
                json.dump(secrets, f, indent=4)

            print(f"Secrets file created successfully at: {self.secretPath}")

        else:
            print("Operation cancelled.")

    def loadSecrets(self):
        """
        Loads whatsappSecrets from the whatsappSecrets.json file with comprehensive error handling.

        Attempts to read and parse the whatsappSecrets.json file, returning the configuration
        data as a dictionary. Provides detailed error messages for common issues
        like missing files or invalid JSON format.

        Returns:
            dict: Dictionary containing all whatsappSecrets and configuration values,
                  or empty dict if loading fails

        Raises:
            No exceptions are raised - all errors are handled gracefully with
            appropriate error messages printed to console.

        Example:
            # >>> creator = SecretCreator()
            # >>> whatsappSecrets = creator.loadSecrets()
            # >>> access_token = whatsappSecrets.get('ACCESS_TOKEN', 'default_token')
        """
        try:
            # Attempt to read and parse the whatsappSecrets file
            with open(self.secretPath, 'r') as f:
                secrets = json.load(f)
            return secrets

        except FileNotFoundError:
            # Handle case where whatsappSecrets.json doesn't exist
            print(f"Error: whatsappSecrets.json not found at {self.secretPath}")
            print("Please run the script again to create the whatsappSecrets file.")
            return {}

        except json.JSONDecodeError:
            # Handle case where whatsappSecrets.json contains invalid JSON
            print(f"Error: Invalid JSON in whatsappSecrets file at {self.secretPath}")
            print("Please check the file format or recreate the whatsappSecrets file.")
            return {}


if __name__ == "__main__":
    """
    Main execution block for interactive whatsappSecrets file creation.

    When this module is run directly, it creates a SecretCreator instance
    which will interactively prompt for API configuration if no whatsappSecrets
    file exists, then displays the loaded whatsappSecrets for verification.

    Usage:
        $ python whatsappSecrets/initSecrets.py
    """
    print("lifeORGS Secrets Initialization")
    print("=" * 35)

    # Create SecretCreator instance (will prompt for whatsappSecrets if needed)
    secretCreator = SecretCreator()

    # Display loaded whatsappSecrets for verification (tokens will be visible)
    print("\nLoaded whatsappSecrets configuration:")
    if secretCreator.loadedSecrets:
        for key, value in secretCreator.loadedSecrets.items():
            # Mask sensitive tokens for security (show only first/last few characters)
            if 'TOKEN' in key or 'SECRET' in key:
                masked_value = f"{value[:4]}...{value[-4:]}" if len(value) > 8 else "***"
                print(f"  {key}: {masked_value}")
            else:
                print(f"  {key}: {value}")
    else:
        print("  No whatsappSecrets loaded - please check for errors above.")
