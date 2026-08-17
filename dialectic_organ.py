#!/usr/bin/env python3
import json, pathlib, datetime, math

NUME = "dialectic_organ"
INBOX = pathlib.Path("roiul/dialectic_inbox.json")
OUTBOX = pathlib.Path("roiul/dialectic_outbox.json")
LOG = pathlib.Path("roiul/dialectic_log.jsonl")

def reflecta(problema, context):
    prior = 0.5
    likeli_h_e = 0.7
    likeli_e_not_h = 0.2
    posterior = (likeli_h_e * prior) / ((likeli_h_e * prior) + (likeli_e_not_h * (1 - prior)))
    
    teza = "Optimizarea resurselor pentru eficienta maxima imediata."
    antiteza = "Sustenabilitatea pe termen lung necesita redundanta si ineficienta controlata."
    sinteza = "Alocare adaptiva bazata pe praguri de risc critic."
    
    infirmabilitate = 0.42
    scor_utilitate = 0.88
    
    decizie = "ACTIONEAZA" if posterior > 0.6 else "ASTEAPTA"
    
    return {
        "oglinda": "Analiza Dialectica",
        "timestamp": datetime.datetime.now().isoformat(),
        "problema": problema,
        "metrics": {"probabilitate_posterioara": posterior, "scor_infirmabilitate": infirmabilitate, "scor_utilitate": scor_utilitate},
        "reflexie": {"teza": teza, "antiteza": antiteza, "sinteza": sinteza},
        "decizie": decizie
    }

def proceseaza_inbox():
    if not INBOX.exists(): return
    inbox = json.loads(INBOX.read_text(encoding="utf-8"))
    if not inbox: return
    mesaj = inbox[0] if isinstance(inbox, list) else inbox
    rezultat = reflecta(mesaj.get("problema"), mesaj.get("context", {}))
    OUTBOX.write_text(json.dumps(rezultat, indent=2), encoding="utf-8")
    with open(LOG, "a") as f: f.write(json.dumps(rezultat) + "\n")

if __name__ == "__main__": proceseaza_inbox()