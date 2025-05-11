import os
import io
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

# Получаем JSON из переменной окружения (установлена в Render)
SERVICE_ACCOUNT_INFO = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
GOOGLE_FOLDER_ID = os.getenv("GOOGLE_DRIVE_FOLDER_ID")  # <-- это ID папки в Google Drive

def get_drive_service():
    credentials_info = json.loads(SERVICE_ACCOUNT_INFO)
    credentials = service_account.Credentials.from_service_account_info(
        credentials_info,
        scopes=["https://www.googleapis.com/auth/drive"]
    )
    return build("drive", "v3", credentials=credentials)

def save_memory_to_drive(user_id: int, message: str) -> str:
    drive_service = get_drive_service()
    filename = f"user_{user_id}.txt"
    file_metadata = {
        "name": filename,
        "parents": [GOOGLE_FOLDER_ID],
        "mimeType": "text/plain"
    }

    file_stream = io.BytesIO(message.encode("utf-8"))
    media = MediaIoBaseUpload(file_stream, mimetype="text/plain")

    # Проверим, есть ли файл — если есть, обновим
    query = f"name='{filename}' and '{GOOGLE_FOLDER_ID}' in parents and trashed=false"
    response = drive_service.files().list(q=query, fields="files(id)").execute()
    files = response.get("files", [])

    if files:
        file_id = files[0]["id"]
        updated = drive_service.files().update(fileId=file_id, media_body=media).execute()
        return f"✅ Обновлено: {updated['id']}"
    else:
        created = drive_service.files().create(body=file_metadata, media_body=media, fields="id").execute()
        return f"✅ Создано: {created['id']}"
