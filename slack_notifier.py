#!/usr/bin/env python3
"""slack_notifier.py — Notificări Slack prin Incoming Webhook (gratuit).
Adaugă SLACK_WEBHOOK_URL ca GitHub Secret.
Mergi la: slack.com/apps → Incoming Webhooks → creează un webhook pentru canalul tău.
"""
import json, pathlib, urllib.request, os

SLACK_WEBHOOK = os.environ.get("SLACK_WEBHOOK_URL", "")
ROIUL = pathlib.Path("roiul")
LOG_FILE = ROIUL / "hydra_log.jsonl"

def trimite_slack(mesaj):
    if not SLACK_WEBHOOK:
        print("[SLACK] Webhook lipsă — skip. Adaugă SLACK_WEBHOOK_URL ca GitHub Secret.")
        return False
    try:
        data = json.dumps({"text": f"🐝 *HYDRA*\n\n{mesaj}", "username": "Hydra Bot", "icon_emoji": ":bee:"}).encode()
        req = urllib.request.Request(SLACK_WEBHOOK, data=data, headers={"Content-Type":"application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=10) as r:
            print("[SLACK] ✅ Notificare trimisă")
            return True
    except Exception as e:
        print(f"[SLACK] ❌ Eroare: {e}")
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
        mesaj = f"*DECIZIE:* {decizie}\n*Problema:* {problema}\nSDI: {metrics.get('SDI','?')} | J: {metrics.get('J','?')} | A: {metrics.get('A','?')}"
        trimite_slack(mesaj)
    else:
        print(f"[SLACK] Ultima decizie: {decizie} — fără notificare")

if __name__ == "__main__":
    verifica_decizii_noi()
