import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from calendarORGS.eventModifiers.calendarAccess import EventObj
from utils.jsonUtils import Configs
from utils.timeUtilitities.timeUtil import TimeConverter
from utils.projRoot import getProjRoot

# If modifying these scopes, delete the file token.json.

class gCalInteract:
    def __init__(self):
        SCOPES = ["https://www.googleapis.com/auth/calendar"]
        creds = None

        # Get absolute paths for credentials and token files
        projRoot = getProjRoot()
        token_path = os.path.join(projRoot, "calendarORGS", "eventModifiers", "token.json")
        credentials_path = os.path.join(projRoot, "calendarORGS", "eventModifiers", "credentials.json")

        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_path, SCOPES
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(token_path, "w") as token:
                token.write(creds.to_json())

        self.service = build("calendar", "v3", credentials=creds)

    def insertEvent(self, eventObject: EventObj):
        startDatetime = TimeConverter(timeDataObj=eventObject.startParsed).convertToDateTime()
        endDatetime = TimeConverter(timeDataObj=eventObject.endParsed).convertToDateTime()
        payload = {
            'summary': eventObject.summary,
            'description': eventObject.description,
            'start': {
                'dateTime': startDatetime.isoformat(),
                'timeZone': Configs().mainConfig['USER_TIMEZONE']
            },
            'end': {
                'dateTime': endDatetime.isoformat(),
                'timeZone': Configs().mainConfig['USER_TIMEZONE']
            },
        }
        print(payload)

        if eventObject.location:
            payload['location'] = eventObject.location

        try:
            event = self.service.events().insert(calendarId='primary', body=payload).execute()
            print(f'Event created: {event.get("htmlLink")}')
            return event
        except HttpError as error:
            print(f'An error occurred: {error}')
            return None
