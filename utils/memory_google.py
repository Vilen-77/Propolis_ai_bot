import os
import io
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

# Получаем JSON из переменной окружения (установлена в Render)
SERVICE_ACCOUNT_INFO = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
GOOGLE_FOLDER_ID = os.getenv("GOOGLE_DRIVE_FOLDER_ID")  # <-- это ID папки в Google Drive

# Авторизация в Google Drive API
def get_drive_service():
    credentials_info = json.loads(SERVICE_ACCOUNT_INFO)
    credentials = service_account.Credentials.from_service_account_info(
        credentials_info,
        scopes=["https://www.googleapis.com/auth/drive"]
    )
    return build("drive", "v3", credentials=credentials)

# Создание новой папки (один раз, по команде /create_folder_test)
def create_drive_folder(folder_name: str = "SvitBotMemory") -> str:
    drive_service = get_drive_service()
    file_metadata = {
        "name": folder_name,
        "mimeType": "application/vnd.google-apps.folder"
    }
    folder = drive_service.files().create(body=file_metadata, fields="id").execute()
    return folder.get("id")

# Загрузка содержимого файла user_<id>.txt из Google Drive
def load_memory_from_drive(user_id: int) -> str:
    drive_service = get_drive_service()
    filename = f"user_{user_id}.txt"
    query = f"name='{filename}' and '{GOOGLE_FOLDER_ID}' in parents and trashed=false"
    response = drive_service.files().list(q=query, fields="files(id)").execute()
    files = response.get("files", [])

    if not files:
        return ""

    file_id = files[0]["id"]
    content = drive_service.files().get_media(fileId=file_id).execute()
    return content.decode("utf-8")

# Сохранение или обновление файла с памятью пользователя (до 2000 символов)
def save_memory_to_drive(user_id: int, new_message: str) -> str:
    drive_service = get_drive_service()
    filename = f"user_{user_id}.txt"
    file_metadata = {
        "name": filename,
        "parents": [GOOGLE_FOLDER_ID],
        "mimeType": "text/plain"
    }

    # Получаем старую память (если есть)
    try:
        old_text = load_memory_from_drive(user_id)
    except Exception:
        old_text = ""

    # Добавим новую реплику
    combined = f"{old_text}\n{new_message}".strip()

    # Обрежем до 2000 символов с конца
    if len(combined) > 2000:
        combined = combined[-2000:]

    file_stream = io.BytesIO(combined.encode("utf-8"))
    media = MediaIoBaseUpload(file_stream, mimetype="text/plain")

    # Сохраняем (создаём или обновляем)
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
