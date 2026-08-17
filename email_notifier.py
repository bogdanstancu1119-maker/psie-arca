#!/usr/bin/env python3
"""
email_notifier.py — Notificări Email prin SMTP (Gmail)
Funcționează IMEDIAT cu Gmail dacă adaugi ca GitHub Secrets:
  SMTP_USER = adresa ta de Gmail
  SMTP_PASS = App Password (nu parola normală — folosește Google App Passwords)
  EMAIL_TO = unde primești notificarea (poate fi aceeași ca SMTP_USER)
"""
import json, pathlib, os, smtplib
from email.mime.text import MIMEText

ROIUL = pathlib.Path("roiul")
LOG_FILE = ROIUL / "hydra_log.jsonl"

SMTP_SERVER = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
SMTP_USER = os.environ.get("SMTP_USER", "")
SMTP_PASS = os.environ.get("SMTP_PASS", "")
EMAIL_TO = os.environ.get("EMAIL_TO", "")

def trimite_email(mesaj):
    if not SMTP_USER or not SMTP_PASS or not EMAIL_TO:
        print("[EMAIL] Secrets lipsă — skip. Adaugă SMTP_USER, SMTP_PASS, EMAIL_TO ca GitHub Secrets.")
        return False
    try:
        msg = MIMEText(f"🐝 HYDRA\n\n{mesaj}")
        msg['Subject'] = '🐝 Hydra Decizie: ACTIONEAZA'
        msg['From'] = SMTP_USER
        msg['To'] = EMAIL_TO
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)
        server.quit()
        print("[EMAIL] ✅ Notificare trimisă")
        return True
    except Exception as e:
        print(f"[EMAIL] ❌ Eroare: {e}")
        return False

def verifica_decizii_noi():
    if not LOG_FILE.exists(): return
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except: return
    if not lines: return
    try:
        ultima = json.loads(lines[-1])
    except: return
    decizie = ultima.get("decizie", "")
    if decizie == "ACTIONEAZA":
        problema = ultima.get("problema", "")[:200]
        metrics = ultima.get("metrics", {})
        ts = ultima.get("timestamp", "")[:19]
        mesaj = f"DECIZIE: {decizie}\nProblema: {problema}\nSDI: {metrics.get('SDI','?')} | J: {metrics.get('J','?')} | A: {metrics.get('A','?')}\nTimp: {ts}"
        trimite_email(mesaj)
    else:
        print(f"[EMAIL] Ultima decizie: {decizie} — fără notificare")

if __name__ == "__main__":
    verifica_decizii_noi()
