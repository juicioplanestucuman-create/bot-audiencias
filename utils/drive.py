import os
import io
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from oauth2client.service_account import ServiceAccountCredentials

SCOPES = ['https://www.googleapis.com/auth/drive']
FOLDER_ID = '1nwpgt6XL1SJXQAdanrkQfHfh7GI-9zlU'

def get_service():
    credentials = ServiceAccountCredentials.from_json_keyfile_dict({
        "private_key": os.environ["PRIVATE_KEY"].replace('\\n', '\n'),
        "client_email": os.environ["CLIENT_EMAIL"],
        "token_uri": "https://oauth2.googleapis.com/token",
        "type": "service_account",
        "project_id": os.environ["PROJECT_ID"],
        "private_key_id": os.environ["PRIVATE_KEY_ID"],
        "client_id": os.environ["CLIENT_ID"]
    }, SCOPES)
    return build('drive', 'v3', credentials=credentials)

def guardar_pdf_en_drive(ruta_local, nombre_archivo):
    service = get_service()
    archivo = MediaFileUpload(ruta_local, mimetype='application/pdf')
    file_metadata = {
        'name': nombre_archivo,
        'parents': [FOLDER_ID]
    }
    file = service.files().create(body=file_metadata, media_body=archivo, fields='id').execute()
    return f'https://drive.google.com/file/d/{file.get("id")}'
