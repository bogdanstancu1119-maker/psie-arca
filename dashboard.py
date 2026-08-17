#!/usr/bin/env python3
"""
dashboard.py — Dashboard live pentru Hydra Organism
Afișează metrici PSIE, organe active, roi status.
Rulează în GitHub Actions fără API extern.
"""
import json, pathlib, datetime, os, glob

ROIUL = pathlib.Path("roiul")

def incarca_json(path):
    if not path.exists(): return {}
    try: return json.loads(path.read_text(encoding="utf-8"))
    except: return {}

def numara_organe():
    """Numără toate organele *_organ.py din repo."""
    organe = []
    for f in glob.glob("*_organ.py"):
        organe.append(f.replace("_organ.py",""))
    return sorted(organe)

def ultimele_decizii(n=5):
    """Citește ultimele decizii din log."""
    log = ROIUL / "hydra_log.jsonl"
    if not log.exists(): return []
    try:
        with open(log, "r", encoding="utf-8") as f:
            lines = f.readlines()[-n:]
        return [json.loads(l) for l in lines if l.strip()]
    except: return []

def dashboard():
    ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
    print(f"\n{'='*70}")
    print(f"  HYDRA DASHBOARD LIVE — {ts}")
    print(f"{'='*70}")

    # Organe
    organe = numara_organe()
    print(f"\n🧠 ORGANE PERMANENTE ({len(organe)} total)")
    for o in organe[:12]:
        print(f"  • {o}")
    if len(organe) > 12:
        print(f"  ... +{len(organe)-12} mai mult")

    # Metrici din memorie
    mem = incarca_json(ROIUL / "hydra_memorie.json")
    istoric = mem.get("istoric", [])
    if istoric:
        ultima = istoric[-1]
        m = ultima.get("metrics", {})
        print(f"\n📊 METRICI PSIE (ultima reflecție)")
        print(f"  J (Flux): {m.get('J','N/A')}")
        print(f"  SDI (Decuplare): {m.get('SDI','N/A')}")
        print(f"  A (Asumare): {m.get('A','N/A')}")
        print(f"  Decizie: {ultima.get('decizie','N/A')}")

    # Decizii recente
    decizii = ultimele_decizii(5)
    print(f"\n🐝 ULTIMELE DECIZII ({len(decizii)})")
    for d in decizii:
        ts_d = d.get("timestamp","")[:19]
        dec = d.get("decizie","?")
        prob = d.get("problema","")[:50]
        print(f"  [{ts_d}] {dec}: {prob}")

    # Inbox
    inbox = incarca_json(ROIUL / "hydra_inbox.json")
    n_inbox = len(inbox) if isinstance(inbox, list) else 0
    print(f"\n📥 INBOX: {n_inbox} mesaje în așteptare")

    # Outbox
    outbox = incarca_json(ROIUL / "hydra_outbox.json")
    n_outbox = len(outbox) if isinstance(outbox, list) else 0
    print(f"📤 OUTBOX: {n_outbox} răspunsuri generate")

    print(f"\n{'='*70}")
    print(f"  Hydra e vie. Fără API. Fără credite. Suverană.")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    dashboard()
