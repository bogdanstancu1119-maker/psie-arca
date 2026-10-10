# create_gmail_filter.py
"""Script simplu care creează un filtru Gmail pentru a elimina bucla de confirmări.

Prerechizite:
- Python 3.9+
- google-api-python-client, google-auth-httplib2, google-auth-oauthlib
- Un fișier de credențiale OAuth 2.0 (client_secret.json) obținut din Google Cloud Console.

Cum se rulează:
1. Instalează pachetele: pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
2. Salvează credențialele în fișierul client_secret.json în același director.
3. Rulează scriptul: python create_gmail_filter.py
4. Scriptul va crea filtrul și va afișa ID-ul filtrului.
"""

import os
import pickle
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Scopurile necesare pentru a crea filtre și a gestiona mesajele
SCOPES = [
    "https://www.googleapis.com/auth/gmail.settings.basic",
    "https://www.googleapis.com/auth/gmail.settings.sharing"
]

def get_gmail_service():
    creds = None
    token_path = Path("token.pickle")
    if token_path.exists():
        with token_path.open("rb") as token:
            creds = pickle.load(token)
    # Dacă nu există credențiale valide, autentifică utilizatorul
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "client_secret.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Salvează credențialele pentru utilizări viitoare
        with token_path.open("wb") as token:
            pickle.dump(creds, token)
    return build("gmail", "v1", credentials=creds)


def create_filter(service):
    # Filtrul caută mesajele de la mailer-daemon@googlemail.com cu subiectul specific
    filter_body = {
        "criteria": {
            "from": "mailer-daemon@googlemail.com",
            "subject": "Mail Delivery Subsystem"
        },
        "action": {
            "archive": True,
            "markRead": True
        }
    }
    result = service.users().settings().filters().create(userId="me", body=filter_body).execute()
    return result

if __name__ == "__main__":
    service = get_gmail_service()
    filter_result = create_filter(service)
    print("Filtru creat cu ID: {}".format(filter_result.get("id")))
```

