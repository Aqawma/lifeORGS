import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from calendarORGS.eventModifiers.calendarAccess import EventObj
from utils.jsonUtils import Configs
from utils.timeUtilitities.timeUtil import TimeConverter

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]

class gCalInteract:
    def __init__(self):
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists("../../whatsappSecrets/token.json"):
            creds = Credentials.from_authorized_user_file("../../whatsappSecrets/token.json", SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "../../whatsappSecrets/credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("../../whatsappSecrets/token.json", "w") as token:
                token.write(creds.to_json())

        self.service = build("calendar", "v3", credentials=creds)

    def insertEvent(self, eventObject: EventObj):
        payload = {
            'summary': eventObject.summary,
            'description': eventObject.description,
            'start': {
                'dateTime': TimeConverter(unixtime=eventObject.start).generateTimeDataObj(),
                'timeZone': Configs().mainConfig['TIMEZONE']
            },
            'end': {
                'dateTime': TimeConverter(unixtime=eventObject.end).generateTimeDataObj(),
                'timeZone': Configs().mainConfig['TIMEZONE']
            },
        }

        if eventObject.location:
            payload['location'] = eventObject.location

        try:
            event = self.service.events().insert(calendarId='primary', body=payload).execute()
            print(f'Event created: {event.get("htmlLink")}')
            return event
        except HttpError as error:
            print(f'An error occurred: {error}')
            return None
