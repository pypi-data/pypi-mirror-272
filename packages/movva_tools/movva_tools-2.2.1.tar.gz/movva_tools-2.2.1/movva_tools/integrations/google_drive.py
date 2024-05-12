import json
import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from movva_tools.integrations.google import GoogleIntegration
import io
import pandas as pd
import logging


logging.basicConfig(
    level=logging.INFO,
    format=f"%(levelname)-8s %(name)s: \n %(message)s"
)
logger = logging.getLogger(name='GoogleDriveLogger')
logger.setLevel(level=logging.INFO)


class GoogleDriveIntegration(GoogleIntegration):
    def __init__(self, folder_id, mimeType, scopes) -> None:
        self.folder_id = folder_id
        self.mime_type = mimeType

        self.credentials = None
        self.drive_service = None

        super().__init__(scopes=scopes, logger=logger)

    def _set_service(self):
        self.drive_service = build('drive', 'v3', credentials=self.credentials)

    def set_credentials(self, credentials, is_file=True):
        super().set_credentials(credentials, is_file)
        self._set_service()

    # def set_credentials(self, credentials, is_file=True):
    #     if is_file:
    #         credentials_path = credentials
    #         if not os.path.exists(credentials_path):
    #             msg = 'Arquivo de credenciais não encontrado'
    #             self._logger.fatal(msg)
    #             raise Exception(msg)

    #         if self.credentials and self.credentials.expired and self.credentials.refresh_token:
    #             self.credentials.refresh(Request())
    #         else:
    #             flow = InstalledAppFlow.from_client_secrets_file(
    #                 "credentials.json", self._scopes
    #             )
    #             self.credentials = flow.run_local_server(port=0)
    #             self._logger.info('Openning token.json file...')
    #             # Save the credentials for the next run
    #             with open("token.json", "w") as token:
    #                 token.write(self.credentials.to_json())

    #         # with open(credentials_path, "w") as token:
    #         #     # token.write(self.credentials.to_json()
    #         #     self.credentials = Credentials.from_authorized_user_file(token, self._scopes)
    #         # if not self.credentials or not self.credentials.valid:
    #         #     flow = InstalledAppFlow.from_client_secrets_file(
    #         #         credentials_path, self._scopes
    #         #     )
    #         #     credentials = flow.run_local_server(port=0)

    #         #     self._logger.info('Openning token.json file...')
    #         #     with open(credentials_path, "w") as token:
    #         #         token.write(self.credentials.to_json())
    #     else:
    #         credentials_json = json.loads(credentials)
    #         self.credentials = Credentials.from_authorized_user_info(credentials_json, self._scopes)

    #     if self.credentials and self.credentials.expired and self.credentials.refresh_token:
    #         self.credentials.refresh(Request())

        # self._set_service()

    def fetch_files(self):
        try:
            results = (
                self.drive_service.files().list(
                    q=f"'{self.folder_id}' in parents",
                    pageSize=10,
                    fields="nextPageToken, files(id, name)"
                ).execute()
            )

            # results = self.drive_service.files().list(
            #     q=f"'{self.folder_id}' in parents and mimeType='{self.mime_type}'",
            #     fields='files(id, name)'
            # ).execute()

            files = results.get('files', [])
            return files
        except Exception as e:
            self._logger.error(f"Erro ao buscar arquivos do Google Drive: {e}")
            return []

    def convert_excel_to_google_sheets(self, file, destination_folder_id):

        name = file['name']
        id = file['id']
        try:
            # Configurar os metadados para a cópia convertida
            copy_metadata = {
                'name': name,
                'parents': [destination_folder_id],  # ID da pasta onde a cópia será armazenada
                'mimeType': 'application/vnd.google-apps.spreadsheet'  # Define o mimeType para o formato do Google Sheets
            }

            # Criar uma cópia do arquivo do Excel e convertê-lo para o formato do Google Sheets
            copied_file = self.drive_service.files().copy(fileId=id, body=copy_metadata).execute()

            return copied_file['id']  # Retorna o ID da cópia convertida
        except Exception as e:
            self._logger.error(f"Erro ao converter o arquivo Excel para o formato do Google Sheets: {e}")
            return None

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

    def rename_file(self, file, new_name):
        try:
            file_id = file['id']

            file_metadata = {'name': new_name}
            self.drive_service.files().update(
                fileId=file_id, body=file_metadata
            ).execute()
        except Exception as e:
            self._logger.error(f"Erro ao renomear o arquivo no Google Drive: {e}")
