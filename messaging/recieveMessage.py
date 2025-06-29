"""
WhatsApp Webhook Receiver Module

This module implements a FastAPI-based webhook server for receiving WhatsApp messages
through the Meta WhatsApp Business API. It handles webhook verification and processes
incoming messages by echoing them back to the sender.

Key Features:
- Webhook verification for Meta WhatsApp Business API
- Incoming message processing and extraction
- Automatic message echo functionality
- Error handling for malformed webhook payloads

Dependencies:
- fastapi: Web framework for creating the webhook endpoints
- messaging.sendMessage: For sending response messages
- utils.jsonUtils: For loading configuration settings

Webhook Endpoints:
- GET /webhook: Webhook verification endpoint for Meta API setup
- POST /webhook: Incoming message processing endpoint

Configuration Requirements:
- VERIFY_TOKEN: Token for webhook verification (must match Meta app configuration)
"""

from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from messaging.sendMessage import messageUser
from parsing.tokenFactory import TokenFactory
from parsing.tokenize import CommandTokenizer
from utils.jsonUtils import loadConfig

# Initialize FastAPI application
app = FastAPI()

# Load verification token from configuration
verifyToken = loadConfig()['VERIFY_TOKEN']

@app.get("/webhook")
def verify(request: Request):
    """
    Webhook verification endpoint for Meta WhatsApp Business API.

    This endpoint is called by Meta during the webhook setup process to verify
    that the webhook URL is valid and controlled by the application owner.
    It validates the verification token and returns the challenge if successful.

    Args:
        request (Request): FastAPI request object containing query parameters

    Query Parameters:
        hub.mode (str): Should be "subscribe" for verification
        hub.verify_token (str): Verification token that must match configured token
        hub.challenge (str): Challenge string to return if verification succeeds

    Returns:
        PlainTextResponse: Challenge string if verification succeeds (HTTP 200),
                          or "Forbidden" message if verification fails (HTTP 403)

    Note:
        - This endpoint must be accessible via HTTPS for Meta webhook verification
        - The verify_token must match the token configured in the Meta app settings
    """
    # Extract verification parameters from query string
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    # Verify that this is a subscription request with correct token
    if mode == "subscribe" and token == verifyToken:
        return PlainTextResponse(content=challenge)
    return PlainTextResponse(status_code=403, content="Forbidden")

@app.post("/webhook")
async def receive(request: Request):
    """
    Webhook endpoint for receiving incoming WhatsApp messages.

    This endpoint processes incoming messages from the Meta WhatsApp Business API.
    It extracts the message text from the webhook payload and echoes it back
    to the sender using the messageUser function.

    Args:
        request (Request): FastAPI request object containing the webhook payload

    Returns:
        dict: Status response indicating the message was received

    Webhook Payload Structure:
        The expected JSON structure follows Meta's WhatsApp webhook format:
        {
            "entry": [
                {
                    "changes": [
                        {
                            "value": {
                                "messages": [
                                    {
                                        "text": {
                                            "body": "message content"
                                        }
                                    }
                                ]
                            }
                        }
                    ]
                }
            ]
        }

    Note:
        - Currently implements a simple echo bot functionality
        - Errors in message extraction are logged but don't prevent response
        - Always returns success status to acknowledge receipt to Meta
    """
    # Parse the incoming webhook payload
    body = await request.json()

    try:
        # Extract message text from the nested JSON structure
        # Following Meta's WhatsApp webhook payload format
        message = body["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"]
        print("User message:", message)
        tokened = CommandTokenizer(message)
        toSend = TokenFactory.doToken(tokened.tokens)
        messageUser(toSend)
    except Exception as e:
        # Log extraction errors but continue processing
        print("Could not extract message:", e)

    # Always return success to acknowledge receipt
    return {"status": "received"}
