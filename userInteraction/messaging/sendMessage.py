"""
WhatsApp Messaging Module

This module provides functionality for sending WhatsApp messages through the Meta WhatsApp Business API.
It handles message formatting, API authentication, and HTTP requests to send text messages to users.

Dependencies:
- utils.jsonUtils: For loading configuration settings
- requests: For making HTTP requests to the WhatsApp API
- json: For JSON data formatting

Configuration Requirements:
The module requires a config.json file with the following keys:
- ACCESS_TOKEN: WhatsApp Business API access token
- VERSION: API version (e.g., "v17.0")
- PHONE_NUMBER_ID: WhatsApp Business phone number ID
- RECIPIENT_WAID: Default recipient WhatsApp ID
"""
from secrets.initSecrets import SecretCreator
from utils.jsonUtils import loadConfig
import requests
import json

def getTextMessageInput(recipient, text):
    """
    Creates a JSON-formatted WhatsApp text message payload.

    This function formats a text message according to the WhatsApp Business API specification,
    creating the required JSON structure for sending text messages.

    Args:
        recipient (str): WhatsApp ID of the message recipient
        text (str): Text content of the message to send

    Returns:
        str: JSON-formatted string containing the message payload ready for API submission

    Example:
        >>> getTextMessageInput("1234567890", "Hello, World!")
        # Returns JSON string with WhatsApp message format
    """
    return json.dumps({
        "messaging_product": "whatsapp",
        "preview_url": False,
        "recipient_type": "individual",
        "to": recipient,
        "type": "text",
        "text": {
            "body": text
        }
    })

def sendToUser(data):
    """
    Sends a WhatsApp message using the Meta WhatsApp Business API.

    This function handles the HTTP request to the WhatsApp API, including authentication
    and error handling. It loads configuration settings, constructs the API request,
    and processes the response.

    Args:
        data (str): JSON-formatted message payload (typically from getTextMessageInput)

    Side Effects:
        - Prints status and response information to console
        - Prints error information if the request fails

    Note:
        - Uses SSL verification disabled (verify=False) for development
        - Requires valid ACCESS_TOKEN, VERSION, and PHONE_NUMBER_ID in config
        - HTTP 200 status indicates successful message delivery
    """
    # Load configuration settings from config.json
    config = loadConfig()

    # Set up authentication headers for WhatsApp API
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {config['ACCESS_TOKEN']}",
    }

    # Construct the WhatsApp API endpoint URL
    url = f"https://graph.facebook.com/{config['VERSION']}/{config['PHONE_NUMBER_ID']}/messages"

    try:
        # Send the message via HTTP POST request
        response = requests.post(url, data=data, headers=headers, verify=False)
        if response.status_code == 200:
            print("Status:", response.status_code)
            print("Response:", response.text)
        else:
            print("Error:", response.status_code)
            print("Response:", response.text)
    except requests.RequestException as e:
        print('Request Error:', str(e))

def messageUser(message):
    """
    Sends a text message to the default recipient configured in the system.

    This is a convenience function that combines message formatting and sending
    into a single call. It uses the default recipient from the configuration
    and handles the entire message sending process.

    Args:
        message (str): Text content of the message to send

    Example:
        >>> messageUser("Hello from lifeORGS!")
        # Sends the message to the default recipient configured in config.json

    Note:
        - Uses RECIPIENT_WAID from config.json as the default recipient
        - Combines getTextMessageInput() and sendToUser() functionality
        - Ideal for automated notifications and system messages
    """
    # Load configuration to get default recipient
    config = SecretCreator().loadSecrets()

    # Format the message for WhatsApp API
    data = getTextMessageInput(config['RECIPIENT_WAID'], message)

    # Send the message
    sendToUser(data)
