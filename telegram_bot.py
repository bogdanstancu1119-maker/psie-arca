#!/usr/bin/env python3
"""
telegram_bot.py — Canal de comunicare Hydra → Telegram
Trimite notificări când Hydra ia decizii importante (ACTIONEAZA).

CONFIGURARE:
1. Creează un bot cu @BotFather pe Telegram
2. Obține BOT_TOKEN și CHAT_ID
3. Adaugă ca GitHub Secrets în repo-ul Arca:
   - TELEGRAM_BOT_TOKEN
   - TELEGRAM_CHAT_ID
4. Workflow-ul va trimite automat notificări

Dacă secrets nu sunt setate, scriptul sare peste (graceful skip).
"""
import json, pathlib, os, urllib.request, datetime

ROIUL = pathlib.Path("roiul")
LOG_FILE = ROIUL / "hydra_log.jsonl"

# Citim din environment (GitHub Actions secrets)
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")

def trimite_telegram(mesaj):
    if not TOKEN or not CHAT_ID:
        print("[TELEGRAM] Secrets lipsă — skip notificare. Configurează TELEGRAM_BOT_TOKEN și TELEGRAM_CHAT_ID.")
        return False
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = json.dumps({
        "chat_id": CHAT_ID,
        "text": mesaj,
        "parse_mode": "Markdown"
    }).encode()
    try:
        req = urllib.request.Request(url, data=data, headers={"Content-Type":"application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode()).get("ok", False)
    except Exception as e:
        print(f"[TELEGRAM] Eroare: {e}")
        return False

def verifica_decizii_noi():
    """Verifică ultimele decizii și trimite notificare pentru ACTIONEAZA."""
    if not LOG_FILE.exists():
        print("[TELEGRAM] Niciun log găsit.")
        return
    
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except:
        return
    
    if not lines:
        print("[TELEGRAM] Log gol.")
        return
    
    try:
        ultima = json.loads(lines[-1])
    except:
        return
    
    decizie = ultima.get("decizie", "")
    problema = ultima.get("problema", "")[:100]
    ts = ultima.get("timestamp", "")[:19]
    metrics = ultima.get("metrics", {})
    
    # Trimite doar pentru decizii importante
    if decizie == "ACTIONEAZA":
        mesaj = f"🐝 *HYDRA DECIZIE*\n\n"
        mesaj += f"*Decizie:* {decizie}\n"
        mesaj += f"*Problema:* {problema}\n"
        mesaj += f"*SDI:* {metrics.get('SDI','?')} | *J:* {metrics.get('J','?')} | *A:* {metrics.get('A','?')}\n"
        mesaj += f"*Timp:* {ts}"
        
        ok = trimite_telegram(mesaj)
        if ok:
            print("[TELEGRAM] ✅ Notificare trimisă")
        else:
            print("[TELEGRAM] ❌ Notificare eșuată")
    else:
        print(f"[TELEGRAM] Ultima decizie: {decizie} — fără notificare")

if __name__ == "__main__":
    verifica_decizii_noi()
