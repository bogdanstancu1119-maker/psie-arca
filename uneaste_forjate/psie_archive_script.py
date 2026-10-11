# psie_archive_script.py
"""Script Python pentru Gmail care
1. caută mesajele din subiectul „Mail Delivery Subsystem (cancer_ontologic)”,
2. le etichetează cu „PSIE‑Archive” și
3. le arhivează (înlocuiește „Trash” fără a le șterge).

Acest script respectă principiile PSIE: nu distruge datele, le arhivează și le recontextualizează.
"""

import os
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# --- Configurație ---
SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.labels"
]

# Dacă nu există token.pickle, va trebui să rulezi autorizarea manuală
TOKEN_PICKLE = 'token.pickle'
CREDENTIALS_JSON = 'credentials.json'  # fișierul OAuth 2.0 descărcat de la Google Cloud

# --- Funcții auxiliare ---

def get_gmail_service():
    creds = None
    if os.path.exists(TOKEN_PICKLE):
        with open(TOKEN_PICKLE, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            from google_auth_oauthlib.flow import InstalledAppFlow
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_JSON, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PICKLE, 'wb') as token:
            pickle.dump(creds, token)
    return build('gmail', 'v1', credentials=creds)


def get_label_id(service, label_name):
    """Returnează ID-ul etichetei. Dacă nu există, o creează."""
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])
    for label in labels:
        if label['name'] == label_name:
            return label['id']
    # Eticheta nu există → creează
    label_object = {
        "name": label_name,
        "labelListVisibility": "labelShow",
        "messageListVisibility": "show"
    }
    created = service.users().labels().create(userId='me', body=label_object).execute()
    return created['id']


def archive_and_label(service, query, label_to_add):
    """Caută mesajele cu `query`, le adaugă eticheta `label_to_add` și le arhivează."""
    label_id = get_label_id(service, label_to_add)
    # Caută mesajele
    response = service.users().messages().list(userId='me', q=query, maxResults=100).execute()
    messages = response.get('messages', [])
    if not messages:
        print("Niciun mesaj găsit pentru interogarea: {}".format(query))
        return
    for msg in messages:
        msg_id = msg['id']
        # Adaugă eticheta
        service.users().messages().modify(
            userId='me',
            id=msg_id,
            body={"addLabelIds": [label_id]}
        ).execute()
        # Arhivează (elimină eticheta INBOX)
        service.users().messages().modify(
            userId='me',
            id=msg_id,
            body={"removeLabelIds": ["INBOX"]}
        ).execute()
        print(f"Mesaj {msg_id} arhivat și etichetat cu {label_to_add}")


def main():
    service = get_gmail_service()
    # Interogare: mesajele provenite de la mailer-daemon@googlemail.com
    query = "from:mailer-daemon@googlemail.com"
    label_to_add = "PSIE-Archive"
    archive_and_label(service, query, label_to_add)

if __name__ == "__main__":
    main()

# --- Instrucțiuni de rulare ---
# 1. Descărcați fișierul credentials.json de la Google Cloud Console (API Gmail).
# 2. Salvați-l în același director cu scriptul.
# 3. Rulați: python psie_archive_script.py
# 4. La prima rulare, va apărea o fereastră de autentificare Google.
# 5. Scriptul va crea eticheta PSIE-Archive (dacă nu există), va arhiva mesajele și le va eticheta.
# 6. Pentru verificare, mergeți în Gmail → Etichete → PSIE-Archive.
```

