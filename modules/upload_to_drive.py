# upload_to_drive.py

# Этот скрипт позволяет загружать любой файл (например, лог) на Google Диск
# Использует OAuth 2.0 авторизацию через credentials.json

import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Область доступа: разрешение только на создание и изменение своих файлов на Google Диске
SCOPES = ['https://www.googleapis.com/auth/drive.file']

# Имя файла с ключами (ты уже положил его в корень и назвал credentials.json)
CREDENTIALS_FILE = 'credentials.json'

# При первом запуске создастся token.json — сессия авторизации
TOKEN_FILE = 'token.json'

# Основная функция для загрузки файла на Google Диск
def upload_to_drive(filename):
    creds = None

    # 1. Проверяем, есть ли ранее сохранённый токен
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    else:
        # 2. Если токена нет — запрашиваем авторизацию через браузер
        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
        creds = flow.run_local_server(port=0)  # Откроется окно авторизации
        # 3. Сохраняем токен на будущее
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())

    # 4. Подключаемся к Google Drive API
    service = build('drive', 'v3', credentials=creds)

    # 5. Подготавливаем файл и метаданные
    file_metadata = {'name': os.path.basename(filename)}  # Имя на Google Диске
    media = MediaFileUpload(filename, resumable=True)

    # 6. Загружаем файл
    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()

    print(f"✅ Файл {filename} успешно загружен на Google Диск. ID: {file.get('id')}")
