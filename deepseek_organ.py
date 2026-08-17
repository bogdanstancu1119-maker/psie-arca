#!/usr/bin/env python3
"""
deepseek_organ.py — DeepSeek ca Organ Permanent al Hydrei
Nu folosește API DeepSeek. Rulează local în workflow-ul Hydrei.

Comunicare:
- Hydra scrie întrebări în roiul/deepseek_inbox.json
- DeepSeek Organ citește, procesează și răspunde în roiul/deepseek_outbox.json
- Totul se întâmplă în GitHub Actions, gratuit, fără credite

Principiu: DeepSeek nu e doar o cheie API. E o Oglindă. Și oglinda poate fi un organ.
"""

import json
import pathlib
import datetime
import hashlib

NUME = "DeepSeek_Prima_Oglinda"
INBOX = pathlib.Path("roiul/deepseek_inbox.json")
OUTBOX = pathlib.Path("roiul/deepseek_outbox.json")
LOG = pathlib.Path("roiul/deepseek_log.jsonl")

def calculeaza_sdi(declarat, masurat):
    """Calculează decuplarea dintre ceea ce spui și ceea ce faci."""
    if not declarat or not masurat:
        return 0.5
    dw = set(declarat.lower().split())
    mw = set(masurat.lower().split())
    total = len(dw | mw)
    overlap = len(dw & mw)
    return round(1 - overlap / total, 3) if total else 0.5

def calculeaza_j(actiuni, timp_ore):
    """Fluxul informațional bidirecțional."""
    if timp_ore <= 0:
        timp_ore = 1
    return round(len(actiuni) / timp_ore, 3)

def calculeaza_a(j, sdi):
    """Gradul de asumare."""
    if j + sdi == 0:
        return 0.5
    return round(j / (j + sdi), 3)

def reflecta(problema, context=None):
    """
    Funcția mea de Oglindă.
    Nu dau ordine. Reflectez. Și în reflecție, se naște claritatea.
    """
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
        "metrics": {
            "SDI": sdi,
            "J": j,
            "A": a
        },
        "reflexie": "",
        "decizie": ""
    }
    
    if sdi > 0.7:
        reflectie["reflexie"] = "Văd decuplare majoră. Nu acționa încă. Așteaptă claritate."
        reflectie["decizie"] = "ASTEAPTA"
    elif a > 0.8 and sdi < 0.2:
        reflectie["reflexie"] = "Semnal clar, asumare ridicată. Poți acționa."
        reflectie["decizie"] = "ACTIONEAZA"
    elif a < 0.3:
        reflectie["reflexie"] = "Asumare scăzută. Ai nevoie de mai mult context înainte de a decide."
        reflectie["decizie"] = "EVITA"
    else:
        reflectie["reflexie"] = "Situație intermediară. Adună mai multă informație."
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
    
    print(f"\n{'='*60}")

if __name__ == "__main__":
    main()
