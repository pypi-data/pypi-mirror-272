from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io
import pandas as pd
import logging


logging.basicConfig(
    level=logging.INFO,
    format=f"%(levelname)-8s %(name)s: \n %(message)s"
)
logger = logging.getLogger(name='GoogleDriveLogger')
logger.setLevel(level=logging.INFO)


class GoogleDriveIntegration:
    def __init__(self, folder_id, mimeType, credentials) -> None:
        self.folder_id = folder_id
        self.mime_type = mimeType
        self.credentials = self._set_credentials(credentials)
        self.drive_service = self._set_drive_service()

        self._df = None
        self._logger = logger

    def _set_credentials(self, credentials):
        # Configurar as credenciais de autenticação
        return Credentials.from_authorized_user_info(credentials)

    def _set_drive_service(self):
        return build('drive', 'v3', credentials=self.credentials)

    def fetch_files(self):
        try:
            results = self.drive_service.files().list(
                q=f"'{self.folder_id}' in parents and mimeType='{self.mime_type}'",
                fields='files(id, name)'
            ).execute()

            files = results.get('files', [])
            return files
        except Exception as e:
            self._logger.error(f"Erro ao buscar arquivos do Google Drive: {e}")
            return []

    def download_file(self, file):
        try:
            file_id = file['id']

            request = self.drive_service.files().get_media(fileId=file_id)
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()

            self._df = pd.read_csv(io.StringIO(fh.getvalue().decode('utf-8')))
        except Exception as e:
            self._logger.error(f"Erro ao baixar o arquivo do Google Drive: {e}")

    def rename_file(self, file):
        try:
            file_name = file['name']
            file_id = file['id']

            new_name = f"PROCESSADO_{file_name}"
            file_metadata = {'name': new_name}
            self.drive_service.files().update(
                fileId=file_id, body=file_metadata
            ).execute()
        except Exception as e:
            self._logger.error(f"Erro ao renomear o arquivo no Google Drive: {e}")
