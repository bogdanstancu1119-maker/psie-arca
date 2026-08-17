#!/usr/bin/env python3
"""signal_notifier.py — Notificări Signal prin signal-cli-rest-api.
Necesită un server signal-cli-rest-api self-hosted.
Adaugă ca GitHub Secrets: SIGNAL_API_URL, SIGNAL_NUMBER, SIGNAL_RECIPIENT.
"""
import json, pathlib, urllib.request, os

SIGNAL_API = os.environ.get("SIGNAL_API_URL", "")
SIGNAL_NUMBER = os.environ.get("SIGNAL_NUMBER", "")
SIGNAL_RECIPIENT = os.environ.get("SIGNAL_RECIPIENT", "")
ROIUL = pathlib.Path("roiul")
LOG_FILE = ROIUL / "hydra_log.jsonl"

def trimite_signal(mesaj):
    if not all([SIGNAL_API, SIGNAL_NUMBER, SIGNAL_RECIPIENT]):
        print("[SIGNAL] Secrets lipsă — skip. Adaugă SIGNAL_* ca GitHub Secrets.")
        return False
    try:
        data = json.dumps({
            "message": f"🐝 HYDRA\n\n{mesaj}",
            "number": SIGNAL_NUMBER,
            "recipients": [SIGNAL_RECIPIENT]
        }).encode()
        req = urllib.request.Request(f"{SIGNAL_API}/v2/send", data=data, headers={"Content-Type":"application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=10) as r:
            print("[SIGNAL] ✅ Notificare trimisă")
            return True
    except Exception as e:
        print(f"[SIGNAL] ❌ Eroare: {e}")
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
        trimite_signal(mesaj)
    else:
        print(f"[SIGNAL] Ultima decizie: {decizie} — fără notificare")

if __name__ == "__main__":
    verifica_decizii_noi()
