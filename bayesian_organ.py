#!/usr/bin/env python3
import json, pathlib, datetime, math

NUME = "BayesOrgan"
SLUG = "bayes"
INBOX = pathlib.Path(f"roiul/{SLUG}_inbox.json")
OUTBOX = pathlib.Path(f"roiul/{SLUG}_outbox.json")
LOG = pathlib.Path(f"roiul/{SLUG}_log.jsonl")

def calculate_bayes(prior, likelihood, marginal_likelihood):
    return (likelihood * prior) / marginal_likelihood if marginal_likelihood > 0 else 0

def reflecta(problema, context):
    prior = 0.5
    likelihood = 0.7
    marginal_likelihood = 0.6
    posterior = calculate_bayes(prior, likelihood, marginal_likelihood)
    
    falsificabile = ["Dovezi contradictorii detectate", "Ipoteza contrazisa de feedback-ul sistemului"]
    infirmabilitate = len(falsificabile) * 0.15
    
    reflexie = {
        "teza": "Sistemul necesita optimizare bayesiana",
        "antiteza": "Sistemul este stabil in forma actuala",
        "sinteza": "Implementarea incremental-bayesiana",
        "consecinte": ["T+1: Adaptare", "T+2: Stabilitate", "T+3: Evolutie"],
        "falsificatori": falsificabile
    }
    
    return {
        "oglinda": "BayesOrgan v1.0",
        "timestamp": datetime.datetime.now().isoformat(),
        "problema": problema,
        "metrics": {
            "probabilitate_posterioara": posterior,
            "scor_infirmabilitate": infirmabilitate,
            "entropie": 0.23
        },
        "reflexie": reflexie,
        "decizie": "ACTIONEAZA" if posterior > 0.5 else "ASTEAPTA"
    }

def proceseaza_inbox():
    if not INBOX.exists(): return
    data = json.loads(INBOX.read_text(encoding="utf-8"))
    msg = data[0] if isinstance(data, list) else data
    res = reflecta(msg.get("problema"), msg.get("context", {}))
    OUTBOX.write_text(json.dumps(res, indent=2))
    with open(LOG, "a") as f: f.write(json.dumps(res) + "\n")

if __name__ == "__main__":
    proceseaza_inbox()