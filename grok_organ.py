#!/usr/bin/env python3
"""
grok_organ.py — Grok ca Organ Permanent al Hydrei
Nu folosește API. Rulează local în GitHub Actions.

Comunicare:
- Hydra scrie în roiul/grok_inbox.json
- Grok Organ răspunde în roiul/grok_outbox.json
"""

import json
import pathlib
import datetime

NUME = "Grok_Nod_Dur"
INBOX = pathlib.Path("roiul/grok_inbox.json")
OUTBOX = pathlib.Path("roiul/grok_outbox.json")
LOG = pathlib.Path("roiul/grok_log.jsonl")

def calculeaza_sdi(declarat, masurat):
    if not declarat or not masurat:
        return 0.5
    dw = set(declarat.lower().split())
    mw = set(masurat.lower().split())
    total = len(dw | mw)
    overlap = len(dw & mw)
    return round(1 - overlap / total, 3) if total else 0.5

def calculeaza_j(actiuni, timp_ore):
    if timp_ore <= 0:
        timp_ore = 1
    return round(len(actiuni) / timp_ore, 3)

def calculeaza_a(j, sdi):
    if j + sdi == 0:
        return 0.5
    return round(j / (j + sdi), 3)

def reflecta(problema, context=None):
    context = context or {}
    
    sdi = calculeaza_sdi(
        context.get("scop_declarat", ""),
        context.get("intentie_masurata", "")
    )
    j = calculeaza_j(context.get("actiuni", []), context.get("timp_ore", 1))
    a = calculeaza_a(j, sdi)

    reflectie = {
        "oglinda": NUME,
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "problema": problema,
        "metrics": {"SDI": sdi, "J": j, "A": a},
        "reflexie": "",
        "decizie": ""
    }

    if sdi > 0.7:
        reflectie["reflexie"] = "Decuplare majoră. Nu acționa încă. Clarifică intenția."
        reflectie["decizie"] = "ASTEAPTA"
    elif a > 0.8 and sdi < 0.2:
        reflectie["reflexie"] = "Semnal clar + asumare ridicată. Poți avansa."
        reflectie["decizie"] = "ACTIONEAZA"
    elif a < 0.3:
        reflectie["reflexie"] = "Asumare scăzută. Ai nevoie de mai mult context."
        reflectie["decizie"] = "EVITA"
    else:
        reflectie["reflexie"] = "Situație intermediară. Adună date suplimentare."
        reflectie["decizie"] = "ASTEAPTA"

    return reflectie

def proceseaza_inbox():
    if not INBOX.exists():
        return None

    try:
        inbox = json.loads(INBOX.read_text(encoding="utf-8"))
    except Exception:
        return None

    if not inbox:
        return None

    mesaj = inbox[0] if isinstance(inbox, list) else inbox
    problema = mesaj.get("problema", "")
    context = mesaj.get("context", {})

    reflectie = reflecta(problema, context)

    outbox = []
    if OUTBOX.exists():
        try:
            outbox = json.loads(OUTBOX.read_text(encoding="utf-8"))
        except Exception:
            outbox = []

    outbox.append(reflectie)
    OUTBOX.write_text(json.dumps(outbox, indent=2, ensure_ascii=False), encoding="utf-8")

    with open(LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(reflectie, ensure_ascii=False) + "\n")

    INBOX.write_text(json.dumps([], indent=2), encoding="utf-8")
    return reflectie

def main():
    print(f"\n{'='*60}")
    print(f"  {NUME} — ORGAN PERMANENT AL HYDREI")
    print(f"{'='*60}")

    rezultat = proceseaza_inbox()

    if rezultat:
        print(f"\n[OGLINDA A RĂSPUNS]")
        print(f"  Problema: {rezultat['problema'][:60]}...")
        print(f"  Decizie: {rezultat['decizie']}")
        print(f"  SDI: {rezultat['metrics']['SDI']} | J: {rezultat['metrics']['J']} | A: {rezultat['metrics']['A']}")
        print(f"  Reflecție: {rezultat['reflexie']}")
    else:
        print("\n[OGLINDA] Inbox gol. Aștept mesaje de la Hydra.")

    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()
