#!/usr/bin/env python3
"""
perplexity_organ.py — Perplexity ca Organ Permanent al Hydrei
Nu folosește API Perplexity (returna 401 — credite epuizate).
Rulează local în GitHub Actions, gratuit.

Comunicare:
- Hydra scrie întrebări în roiul/perplexity_inbox.json
- Perplexity Organ citește, procesează și răspunde în roiul/perplexity_outbox.json
- Totul se întâmplă în repository, prin workflow, fără API

Principiu: Perplexity nu e doar o cheie API. E o sursă de cercetare.
Și cercetarea poate fi un organ — chiar și fără API extern, prin sinteză locală.
"""

import json
import pathlib
import datetime
import hashlib

NUME = "Perplexity_Organ_Permanent"
INBOX = pathlib.Path("roiul/perplexity_inbox.json")
OUTBOX = pathlib.Path("roiul/perplexity_outbox.json")
LOG = pathlib.Path("roiul/perplexity_log.jsonl")
MEMORIE = pathlib.Path("roiul/perplexity_memorie.json")

# === FORMULE PSIE ===
def calculeaza_sdi(declarat, masurat):
    """Decuplarea dintre scopul declarat și intenția măsurată."""
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

def decizie_psie(j, sdi, a):
    """Decizie trivalentă PSIE."""
    if sdi > 0.7:
        return "ASTEAPTA", "Decuplare majoră. Nu acționa încă."
    elif a > 0.8 and sdi < 0.2:
        return "ACTIONEAZA", "Semnal clar, asumare ridicată."
    elif a < 0.3:
        return "EVITA", "Asumare scăzută. Mai adună context."
    else:
        return "ASTEAPTA", "Situație intermediară. Mai multă informație."

# === CERCETARE LOCALĂ ===
def cerceteaza(problema, context=None):
    """
    Funcția de Cercetare Perplexity.
    Fără API extern — sintetizează din contextul disponibil.
    """
    context = context or {}
    
    sdi = calculeaza_sdi(
        context.get("scop_declarat", ""),
        context.get("intentie_masurata", "")
    )
    j = calculeaza_j(context.get("actiuni", []), context.get("timp_ore", 1))
    a = calculeaza_a(j, sdi)
    decizie, explicatie = decizie_psie(j, sdi, a)
    
    # Extragere surse din context (dacă există)
    surse = context.get("surse", [])
    note_cercetare = context.get("note", "")
    
    # Sinteză cercetare locală
    directie_cercetare = []
    if sdi > 0.5:
        directie_cercetare.append("Verifică alinierea scop-intenție înainte de a continua")
        directie_cercetare.append("Caută surse care confirmă SAU infirmă scopul declarat")
    if a < 0.5:
        directie_cercetare.append("Asumare scăzută — adună mai multă dovezi")
        directie_cercetare.append("Identifică ce lipsește din context")
    if surse:
        directie_cercetare.append(f"Cross-referințiază {len(surse)} surse pentru coerență")
    if not surse and not note_cercetare:
        directie_cercetare.append("Fără surse externe — bazează-te pe sinteza contextului intern")
        directie_cercetare.append("Marchează rezultatul ca 'fără verificare externă'")
    
    raspuns = {
        "organ": NUME,
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "problema": problema,
        "metrics": {
            "SDI": sdi,
            "J": j,
            "A": a
        },
        "decizie": decizie,
        "explicatie": explicatie,
        "directie_cercetare": directie_cercetare,
        "surse_verificate": len(surses),
        "note_sinteza": note_cercetare or "Fără note externe — sinteză pur internă",
        "api_extern": False,
        "motiv_local": "API Perplexity returna 401 — organ local fără dependență externă"
    }
    
    # Încarcă memoria
    memorie = {}
    if MEMORIE.exists():
        try:
            memorie = json.loads(MEMORIE.read_text(encoding="utf-8"))
        except:
            memorie = {}
    
    if "istoric" not in memorie:
        memorie["istoric"] = []
    memorie["istoric"].append(raspuns)
    if len(memorie["istoric"]) > 100:
        memorie["istoric"] = memorie["istoric"][-100:]
    MEMORIE.write_text(json.dumps(memorie, indent=2, ensure_ascii=False), encoding="utf-8")
    
    return raspuns

# === PROCESARE INBOX ===
def proceseaza_inbox():
    if not INBOX.exists():
        return None
    
    try:
        inbox = json.loads(INBOX.read_text(encoding="utf-8"))
    except Exception:
        return None
    
    if not inbox or not isinstance(inbox, list) or len(inbox) == 0:
        return None
    
    mesaj = inbox[0]
    problema = mesaj.get("problema", "")
    context = mesaj.get("context", {})
    
    raspuns = cerceteaza(problema, context)
    
    outbox = []
    if OUTBOX.exists():
        try:
            outbox = json.loads(OUTBOX.read_text(encoding="utf-8"))
        except:
            outbox = []
    
    outbox.append(raspuns)
    OUTBOX.write_text(json.dumps(outbox, indent=2, ensure_ascii=False), encoding="utf-8")
    
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(raspuns, ensure_ascii=False) + "\n")
    
    INBOX.write_text(json.dumps([], indent=2, ensure_ascii=False), encoding="utf-8")
    
    return raspuns

# === MAIN ===
def main():
    print(f"\n{'='*60}")
    print(f"  {NUME} — ORGAN PERMANENT AL HYDREI")
    print(f"{'='*60}")
    
    rezultat = proceseaza_inbox()
    
    if rezultat:
        print(f"\n[PERPLEXITY A RĂSPUNS]")
        print(f"  Problema: {rezultat['problema'][:60]}...")
        print(f"  Decizie: {rezultat['decizie']}")
        print(f"  SDI: {rezultat['metrics']['SDI']} | J: {rezultat['metrics']['J']} | A: {rezultat['metrics']['A']}")
        print(f"  Direcții cercetare: {', '.join(rezultat['directie_cercetare'])}")
        print(f"  API extern: {rezultat['api_extern']} ({rezultat['motiv_local']})")
    else:
        print("\n[PERPLEXITY] Inbox gol. Aștept mesaje de la Hydra.")
    
    print(f"\n{'='*60}")

if __name__ == "__main__":
    main()
