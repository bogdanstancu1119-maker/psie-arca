#!/usr/bin/env python3
import json, pathlib, datetime, math

NUME = "EmpiricOrgan"
INBOX = pathlib.Path("roiul/empiric_inbox.json")
OUTBOX = pathlib.Path("roiul/empiric_outbox.json")
LOG = pathlib.Path("roiul/empiric_log.jsonl")

def reflecta(problema, context):
    dovezi = context.get("dovezi", [])
    ipoteza = context.get("ipoteza", "Fara ipoteza")
    prior = context.get("prior", 0.5)
    
    # Calcul Bayesian: P(H|E) = P(E|H)*P(H) / [P(E|H)*P(H) + P(E|not H)*P(not H)]
    p_e_given_h = 0.8
    p_e_given_not_h = 0.2
    posterior = (p_e_given_h * prior) / (p_e_given_h * prior + p_e_given_not_h * (1 - prior))
    
    falsificatori = [f"Experimentul de a observa lipsa {d}" for d in dovezi]
    
    decizie = "ACTIONEAZA" if posterior > 0.75 else "ASTEAPTA"
    
    return {
        "oglinda": "Analiza Empirica",
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "problema": problema,
        "metrics": {"posterior": posterior, "scor_infirmabilitate": len(falsificatori) / 10.0},
        "reflexie": {"ipoteza": ipoteza, "falsificatori": falsificatori},
        "decizie": decizie
    }

def proceseaza_inbox():
    if not INBOX.exists(): return
    inbox = json.loads(INBOX.read_text(encoding="utf-8"))
    if not inbox: return
    mesaj = inbox[0]
    rezultat = reflecta(mesaj.get("problema"), mesaj.get("context", {}))
    OUTBOX.write_text(json.dumps(rezultat, indent=2))
    with LOG.open("a") as f: f.write(json.dumps(rezultat) + "\n")

if __name__ == "__main__": proceseaza_inbox()