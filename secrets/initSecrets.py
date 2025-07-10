import os
import json

class SecretCreator:
    def __init__(self):
        self.secretPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'secrets.json')
        self.secretBool = os.path.exists(self.secretPath)
        self.createSecrets() if not self.secretBool else None
        self.loadedSecrets = self.loadSecrets()

    def createSecrets(self):
        overwriteConfirm = "y"
        if self.secretBool:
            overwriteConfirm = input("A secrets.json file already exists. Do you want to overwrite it? (y/n): ")

        if overwriteConfirm == "y":
            # Ensure the directory exists
            os.makedirs(os.path.dirname(self.secretPath), exist_ok=True)
            
            APP_ID = input("Enter your app ID: ")
            APP_SECRET = input("Enter your app secret: ")
            RECIPIENT_WAID = input("Enter your recipient WaID: ")
            VERSION = input("Enter your version: ")
            PHONE_NUMBER_ID = input("Enter your phone number ID: ")
            VERIFY_TOKEN = input("Enter your verify token: ")
            ACCESS_TOKEN = input("Enter your access token: ")

            secrets = {
                "APP_ID": APP_ID,
                "APP_SECRET": APP_SECRET,
                "RECIPIENT_WAID": RECIPIENT_WAID,
                "VERSION": VERSION,
                "PHONE_NUMBER_ID": PHONE_NUMBER_ID,
                "VERIFY_TOKEN": VERIFY_TOKEN,
                "ACCESS_TOKEN": ACCESS_TOKEN
            }

            with open(self.secretPath, 'w') as f:
                json.dump(secrets, f, indent=4)

        else:
            print("Operation cancelled.")

    def loadSecrets(self):
        # Add error handling for missing file
        try:
            with open(self.secretPath, 'r') as f:
                secrets = json.load(f)
            return secrets
        except FileNotFoundError:
            print(f"Error: secrets.json not found at {self.secretPath}")
            print("Please run the script again to create the secrets file.")
            return {}
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in secrets file at {self.secretPath}")
            return {}


if __name__ == "__main__":
    secretCreator = SecretCreator()
    print(secretCreator.loadedSecrets)
