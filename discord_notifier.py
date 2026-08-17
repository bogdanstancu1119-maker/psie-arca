#!/usr/bin/env python3
"""discord_notifier.py — Notificări Discord prin webhook (gratuit).
Adaugă DISCORD_WEBHOOK_URL ca GitHub Secret.
Mergi la: Discord → Setări canal → Integrations → Webhooks → New Webhook → Copy URL.
"""
import json, pathlib, urllib.request, os

DISCORD_WEBHOOK = os.environ.get("DISCORD_WEBHOOK_URL", "")
ROIUL = pathlib.Path("roiul")
LOG_FILE = ROIUL / "hydra_log.jsonl"

def trimite_discord(mesaj):
    if not DISCORD_WEBHOOK:
        print("[DISCORD] Webhook lipsă — skip. Adaugă DISCORD_WEBHOOK_URL ca GitHub Secret.")
        return False
    try:
        data = json.dumps({"content": f"🐝 **HYDRA**\n\n{mesaj}", "username": "Hydra Bot"}).encode()
        req = urllib.request.Request(DISCORD_WEBHOOK, data=data, headers={"Content-Type":"application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=10) as r:
            print("[DISCORD] ✅ Notificare trimisă")
            return True
    except Exception as e:
        print(f"[DISCORD] ❌ Eroare: {e}")
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
        mesaj = f"**DECIZIE:** {decizie}\n**Problema:** {problema}\nSDI: {metrics.get('SDI','?')} | J: {metrics.get('J','?')} | A: {metrics.get('A','?')}"
        trimite_discord(mesaj)
    else:
        print(f"[DISCORD] Ultima decizie: {decizie} — fără notificare")

if __name__ == "__main__":
    verifica_decizii_noi()
