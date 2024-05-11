import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


class GoogleIntegration:
    def __init__(self, scopes, logger) -> None:
        self._scopes = scopes
        self._logger = logger

    def set_credentials(self, credentials, is_file=True, token_file=None):
        if not token_file:
            token_file = 'token.json'

        if is_file:
            credentials_path = credentials
            if not os.path.exists(credentials_path):
                msg = 'Arquivo de credenciais não encontrado'
                self._logger.fatal(msg)
                raise Exception(msg)

            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                self.credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", self._scopes
                )
                self.credentials = flow.run_local_server(port=0)
                self._logger.info('Openning token.json file...')
                # Save the credentials for the next run
                with open(token_file, "w") as token:
                    token.write(self.credentials.to_json())

        else:
            credentials_json = json.loads(credentials)
            self.credentials = Credentials.from_authorized_user_info(credentials_json, self._scopes)

        if self.credentials and self.credentials.expired and self.credentials.refresh_token:
            self.credentials.refresh(Request())

    def _set_service(self):
        raise NotImplementedError('O método precisa ser definido.')
