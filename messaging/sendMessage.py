from utils.jsonUtils import loadConfig
import requests
import json

def getTextMessageInput(recipient, text):
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

    config = loadConfig()

    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {config['ACCESS_TOKEN']}",
    }

    url = f"https://graph.facebook.com/{config['VERSION']}/{config['PHONE_NUMBER_ID']}/messages"

    try:
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
    config = loadConfig()
    data = getTextMessageInput(config['RECIPIENT_WAID'], message)
    sendToUser(data)


messageUser(input("Enter message to send to user:"))
