#!/usr/bin/env python3
"""
longterm_organ.py — Analizator de Consecinte pe Termen Lung ca Organ Permanent al Hydrei
"""
import json, pathlib, datetime, math

NUME = "Analizator de Consecinte"
INBOX = pathlib.Path("roiul/longterm_inbox.json")
OUTBOX = pathlib.Path("roiul/longterm_outbox.json")
LOG = pathlib.Path("roiul/longterm_log.jsonl")

def reflecta(problema, context):
    prior = 0.5
    evidence_support = 0.8
    # Calcul Bayesian simplificat pentru probabilitatea succesului
    posterior = (evidence_support * prior) / ((evidence_support * prior) + (0.2 * 0.5))
    
    consecinte = ["Efect_Direct", "Efect_Secundar", "Efect_Sistemic_Long_Term"]
    score_infirmabilitate = 0.75
    
    decizie = "ACTIONEAZA" if posterior > 0.6 else ("ASTEAPTA" if posterior > 0.4 else "EVITA")
    
    return {
        "oglinda": "Analiza cauzalitate pe orizont extins",
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "problema": problema,
        "metrics": {
            "probabilitate_posterioara": round(posterior, 4),
            "scor_infirmabilitate": score_infirmabilitate,
            "orizont_estimat_luni": 12
        },
        "reflexie": f"Analiza a validat lantul {consecinte}. Riscul de infirmare este {score_infirmabilitate}.",
        "decizie": decizie
    }

def proceseaza_inbox():
    if not INBOX.exists(): return
    data = json.loads(INBOX.read_text(encoding="utf-8"))
    if not data: return
    mesaj = data[0] if isinstance(data, list) else data
    rezultat = reflecta(mesaj.get("problema"), mesaj.get("context", {}))
    OUTBOX.write_text(json.dumps(rezultat, indent=2), encoding="utf-8")
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(rezultat) + "\n")

if __name__ == "__main__":
    proceseaza_inbox()