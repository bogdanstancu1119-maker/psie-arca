#!/usr/bin/env python3
"""
sentinel_organ.py — Modul local de triaj și validare a sarcinilor.
Rulează autonom în GitHub Actions fără dependențe externe.
"""

import json
import pathlib
import datetime

INBOX = pathlib.Path("roiul/sentinel_inbox.json")
OUTBOX = pathlib.Path("roiul/sentinel_outbox.json")
LOG = pathlib.Path("roiul/sentinel_log.jsonl")

def evalueaza_sarcina(sarcina):
    """Calculează un scor de prioritate și fezabilitate locală."""
    titlu = sarcina.get("titlu", "Necunoscut")
    pasi = sarcina.get("pasi", [])
    urgenta = sarcina.get("urgenta", 1)  # Scara 1-5
    
    complexitate = len(pasi)
    scor_prioritate = round((urgenta * 2) / (complexitate if complexitate > 0 else 1), 2)
    
    decizie = "EXECUTA" if scor_prioritate >= 1.0 else "FRAGMENTEAZA"
    
    return {
        "id": sarcina.get("id", "task_anonim"),
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "titlu": titlu,
        "metrics": {
            "complexitate": complexitate,
            "urgenta": urgenta,
            "scor": scor_prioritate
        },
        "decizie": decizie,
        "recomandare": "Gata de procesare" if decizie == "EXECUTA" else "Necesită separare în sub-taskuri"
    }

def proceseaza():
    if not INBOX.exists():
        return
    
    try:
        date_inbox = json.loads(INBOX.read_text(encoding="utf-8"))
    except Exception:
        return

    if not date_inbox:
        return

    mesaje = date_inbox if isinstance(date_inbox, list) else [date_inbox]
    rezultate = [evalueaza_sarcina(m) for m in mesaje]

    # Citire outbox existent
    outbox_data = []
    if OUTBOX.exists():
        try:
            outbox_data = json.loads(OUTBOX.read_text(encoding="utf-8"))
        except Exception:
            outbox_data = []

    outbox_data.extend(rezultate)
    
    # Salvare și curățare inbox
    OUTBOX.write_text(json.dumps(outbox_data, indent=2, ensure_ascii=False), encoding="utf-8")
    
    with open(LOG, "a", encoding="utf-8") as f:
        for r in rezultate:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    INBOX.write_text(json.dumps([], indent=2), encoding="utf-8")

if __name__ == "__main__":
    proceseaza()
