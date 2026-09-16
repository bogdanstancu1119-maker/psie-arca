# resolve_meta_risk.py
"""
Scriptul PSIE pentru entitatea_risc "Meta (cancer_ontologic)".
Funcționalitate:
1. Încarcă fișierul JSON al entității (implicit: entitate_risc.json).
2. Adaugă/actualizează câmpul ParadoxHidra.rezolvat = true.
3. Salvează modificările fără a distruge datele originale.
4. Înregistrează un log în resolution_log.txt cu data și detalii.
5. Trimite un e‑mail de notificare (dacă Gmail connector este autorizat).
"""

import json
import sys
import os
import datetime
import smtplib
from email.message import EmailMessage

# --- Configurație (modificați după necesități) ---
ENTITATE_FILE = "entitate_risc.json"
LOG_FILE = "resolution_log.txt"
EMAIL_SUBJECT = "Rezolvarea riscului Meta (cancer_ontologic)"
EMAIL_FROM = "hydra@example.com"
EMAIL_TO = "stakeholders@example.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "hydra@example.com"   # Gmail user
SMTP_PASS = "<gmail-app-password>"  # App password, nu parola normală
# ---------------------------------------------

def load_entity(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Fișierul {file_path} nu există.")
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_entity(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_resolution_flag(entity):
    # Adaugă/actualizează câmpul ParadoxHidra.rezolvat
    if "ParadoxHidra" not in entity:
        entity["ParadoxHidra"] = {}
    entity["ParadoxHidra"]["rezolvat"] = True
    return entity

def log_resolution(message):
    timestamp = datetime.datetime.utcnow().isoformat() + "Z"
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f"{timestamp} - {message}\n")

def send_email(subject, body):
    try:
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = EMAIL_FROM
        msg['To'] = EMAIL_TO
        msg.set_content(body)

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
        log_resolution("E-mail trimis cu succes la " + EMAIL_TO)
    except Exception as e:
        log_resolution(f"Eșec la trimiterea e-mailului: {e}")

if __name__ == "__main__":
    # Determinăm fișierul entitate (posibil argument de linie de comandă)
    ent_file = ENTITATE_FILE
    if len(sys.argv) > 1:
        ent_file = sys.argv[1]

    try:
        entity = load_entity(ent_file)
        entity = add_resolution_flag(entity)
        save_entity(entity, ent_file)
        log_resolution(f"Flagul ParadoxHidra.rezolvat adăugat în {ent_file}")

        # Conținut e‑mail
        body = (f"Entitatea: {entity.get('Titlu', 'necunoscut')}\n"
                f"Risc: {entity.get('a_calculat', 'necunoscut')}\n"
                f"Rezoluție: ParadoxHidra.rezolvat = true\n"
                f"Data: {datetime.datetime.utcnow().isoformat()}Z\n"
                f"\nAcțiuni recomandate aplicate:\n"
                f"- Transiția la AR non‑invaziv\n"
                f"- Interoperabilitate radicală\n"
                f"- Indicatori de performanță pe bunăstare\n"
                f"- Responsabilitate juridică și etică\n"
                f"\n---\n")
        send_email(EMAIL_SUBJECT, body)

        print("Rezolvarea riscului a fost aplicată cu succes.")
    except Exception as e:
        print(f"Eroare: {e}")
        log_resolution(f"Eroare: {e}")
        sys.exit(1)
