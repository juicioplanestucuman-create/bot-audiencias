import os
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta

def get_service():
    scopes = ['https://www.googleapis.com/auth/calendar']
    credentials = ServiceAccountCredentials.from_json_keyfile_dict({
        "private_key": os.environ["PRIVATE_KEY"].replace('\\n', '\n'),
        "client_email": os.environ["CLIENT_EMAIL"],
        "token_uri": "https://oauth2.googleapis.com/token",
        "type": "service_account",
        "project_id": os.environ["PROJECT_ID"],
        "private_key_id": os.environ["PRIVATE_KEY_ID"],
        "client_id": os.environ["CLIENT_ID"]
    }, scopes)
    return build('calendar', 'v3', credentials=credentials)

def crear_evento_desde_sheet():
    # esto lo usás con script de AppsScript, no desde acá
    pass
