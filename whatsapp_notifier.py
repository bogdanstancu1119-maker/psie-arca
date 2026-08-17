#!/usr/bin/env python3
"""whatsapp_notifier.py — Notificări WhatsApp prin Twilio (free tier).
Adaugă ca GitHub Secrets:
  TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_NUMBER, USER_WHATSAPP_NUMBER
Obține credențiale de la twilio.com (free trial include WhatsApp sandbox).
"""
import json, pathlib, os

TWILIO_SID = os.environ.get("TWILIO_ACCOUNT_SID", "")
TWILIO_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN", "")
TWILIO_WHATSAPP = os.environ.get("TWILIO_WHATSAPP_NUMBER", "")
USER_WHATSAPP = os.environ.get("USER_WHATSAPP_NUMBER", "")
ROIUL = pathlib.Path("roiul")
LOG_FILE = ROIUL / "hydra_log.jsonl"

def trimite_whatsapp(mesaj):
    if not all([TWILIO_SID, TWILIO_TOKEN, TWILIO_WHATSAPP, USER_WHATSAPP]):
        print("[WHATSAPP] Secrets Twilio lipsă — skip. Adaugă TWILIO_* ca GitHub Secrets.")
        return False
    try:
        from twilio.rest import Client
        client = Client(TWILIO_SID, TWILIO_TOKEN)
        msg = client.messages.create(
            body=f"🐝 HYDRA\n\n{mesaj}",
            from_=f'whatsapp:{TWILIO_WHATSAPP}',
            to=f'whatsapp:{USER_WHATSAPP}'
        )
        print(f"[WHATSAPP] ✅ Notificare trimisă (sid: {msg.sid})")
        return True
    except ImportError:
        print("[WHATSAPP] twilio package lipsă — pip install twilio")
        return False
    except Exception as e:
        print(f"[WHATSAPP] ❌ Eroare: {e}")
        return False

def verifica_decizii_noi():
    if not LOG_FILE.exists(): return
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f: lines = f.readlines()
    except: return
    if not lines: return
    try: ultima = json.loads(lines[-1])
    except: return
    decizie = ultima.get("decizie", "")
    if decizie == "ACTIONEAZA":
        problema = ultima.get("problema", "")[:200]
        metrics = ultima.get("metrics", {})
        mesaj = f"DECIZIE: {decizie}\nProblema: {problema}\nSDI: {metrics.get('SDI','?')} | J: {metrics.get('J','?')} | A: {metrics.get('A','?')}"
        trimite_whatsapp(mesaj)
    else:
        print(f"[WHATSAPP] Ultima decizie: {decizie} — fără notificare")

if __name__ == "__main__":
    verifica_decizii_noi()
