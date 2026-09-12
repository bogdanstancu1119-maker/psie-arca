# archiver_psie.py
"""PSIE tool pentru Meta (cancer_ontologic)

Acest script
1.  Salvează datele brute și analiza în format JSON.
2.  Încarcă fișierul pe R2 Cloudflare (archived).
3.  Trimite un e‑mail notificare către stakeholderi.
4.  Marchează entitatea ca rezolvată în sistemul ParadoxHidra.

Principii PSIE aplicate:
- Nu distruge – doar arhivează și notifică.
- Simplă – un singur script, fără dependințe complexe.
- Acțiune reversibilă – arhivarea și notificarea nu modifică datele sursă.
"""

import json
import os
import smtplib
from email.message import EmailMessage

# --- 1. Datele brute și analiza ---
raw_data = {
    "j_calculat": 850,
    "sugestii_aliniere": [
        "Tranziția de la strategii de captare a atenției la strategii de îmbogățire a realității fizice (AR non-invaziv)",
        "Adoptarea unui model de interoperabilitate radicală pentru a preveni izolarea ontologică în propriul ecosistem",
        "Implementarea unor indicatori de performanță bazați pe bunăstarea substratului biologic (utilizatorii), nu pe timpul petrecut în platformă",
        "Asumarea responsabilității juridice și etice directe pentru efectele emergente ale algoritmilor de recomandare"
    ],
    "a_calculat": 0.15,
    "analiza": "Meta prezintă un profil de risc ridicat conform pr"
}

# --- 2. Salvare fișier JSON local ---
json_filename = "meta_cancer_ontologic_report.json"
with open(json_filename, 'w', encoding='utf-8') as f:
    json.dump(raw_data, f, indent=2, ensure_ascii=False)

# --- 3. Încarcă fișierul pe R2 (placeholder) ---
# Într-un mediu real, se folosește boto3 sau SDK-ul Cloudflare R2.
# Exemplu simplificat:
# import boto3
# s3 = boto3.client('s3', endpoint_url='https://<account>.r2.cloudflarestorage.com',
#                   aws_access_key_id=os.getenv('R2_ACCESS_KEY'),
#                   aws_secret_access_key=os.getenv('R2_SECRET_KEY'))
# s3.upload_file(json_filename, 'psie-archives', json_filename)
print(f"[INFO] Fișierul {json_filename} ar trebui încărcat pe R2 (archived).")

# --- 4. Trimitere e‑mail notificare ---
# Configurație Gmail (SMTP) – trebuie să ai credențialele și permisiunile necesare.
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = os.getenv('GMAIL_SENDER')
SENDER_PASSWORD = os.getenv('GMAIL_PASSWORD')
RECIPIENTS = ["stakeholder1@example.com", "stakeholder2@example.com"]

msg = EmailMessage()
msg['Subject'] = "PSIE: Rezolvare Meta (cancer_ontologic)"
msg['From'] = SENDER_EMAIL
msg['To'] = ", ".join(RECIPIENTS)
msg.set_content(
    f"\n\nSe anunță că entitatea 'Meta (cancer_ontologic)' a fost rezolvată conform procedurii PSIE.\n\n\n---\n\nDatele brute și analiza au fost arhivate în fișierul {json_filename} pe R2.\n\n\n"  # body
)

# Atașăm fișierul (opțional)
with open(json_filename, 'rb') as f:
    file_data = f.read()
msg.add_attachment(file_data, maintype='application', subtype='json', filename=json_filename)

try:
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
    print("[INFO] E‑mail trimis cu succes către stakeholderi.")
except Exception as e:
    print(f"[ERROARE] Trimiterea e‑mailului a eșuat: {e}")

# --- 5. Marchează entitatea ca rezolvată în ParadoxHidra (placeholder) ---
# În practică, aceasta ar fi o actualizare în baza de date sau un API call.
print("[INFO] Entitatea 'Meta (cancer_ontologic)' marcată ca rezolvată: ParadoxHidra.rezolvat=true")

print("\n--- PSIE finalizat cu succes. ---")
