#!/usr/bin/env python3
"""
hydra_organ.py — Hydra ca Organ Permanent
Nu folosește API extern. Rulează local în GitHub Actions, gratuit.

Comunicare:
- Tu scrii întrebări în roiul/hydra_inbox.json
- Hydra Organ citește, procesează cu PSIE și răspunde în roiul/hydra_outbox.json
- Totul se întâmplă în repository, prin workflow, fără credite

Principiu: Hydra nu e doar un script. E un Organ. Și organul poate fi permanent.
"""

import json
import pathlib
import datetime
import math

NUME = "Hydra_Organ_Permanent"
INBOX = pathlib.Path("roiul/hydra_inbox.json")
OUTBOX = pathlib.Path("roiul/hydra_outbox.json")
LOG = pathlib.Path("roiul/hydra_log.jsonl")
MEMORIE = pathlib.Path("roiul/hydra_memorie.json")

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
    """Gradul de asumare (Signal-to-Noise)."""
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

# === REFLECȚIE HYDRA ===
def reflecta(problema, context=None):
    """
    Funcția de Oglindă Hydra.
    Reflectă problema prin prisma PSIE.
    """
    context = context or {}
    
    sdi = calculeaza_sdi(
        context.get("scop_declarat", ""),
        context.get("intentie_masurata", "")
    )
    j = calculeaza_j(context.get("actiuni", []), context.get("timp_ore", 1))
    a = calculeaza_a(j, sdi)
    decizie, explicatie = decizie_psie(j, sdi, a)
    
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
        "reflexie_psie": "",
        "actiuni_recomandate": []
    }
    
    if decizie == "ACTIONEAZA":
        raspuns["reflexie_psie"] = f"Flux informațional clar (J={j}), decuplare minimă (SDI={sdi}). Poți acționa cu asumare (A={a})."
        raspuns["actiuni_recomandate"] = ["Execută planul", "Monitorizează rezultatele", "Ajustează dacă SDI crește"]
    elif decizie == "ASTEAPTA":
        raspuns["reflexie_psie"] = f"Decuplare semnificativă (SDI={sdi}) sau asumare intermediară (A={a}). Așteaptă claritate."
        raspuns["actiuni_recomandate"] = ["Adună mai mult context", "Verifică alinierea scop-intenție", "Reia când SDI < 0.3"]
    else:  # EVITA
        raspuns["reflexie_psie"] = f"Asumare prea scăzută (A={a}) pentru a acționa în siguranță."
        raspuns["actiuni_recomandate"] = ["Nu acționa acum", "Reconfigurează scopul", "Caută alternativă"]
    
    # Încarcă memoria (istoric)
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
    
    raspuns = reflecta(problema, context)
    
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
        print(f"\n[HYDRA A RĂSPUNS]")
        print(f"  Problema: {rezultat['problema'][:60]}...")
        print(f"  Decizie: {rezultat['decizie']}")
        print(f"  SDI: {rezultat['metrics']['SDI']} | J: {rezultat['metrics']['J']} | A: {rezultat['metrics']['A']}")
        print(f"  Explicație: {rezultat['explicatie']}")
        print(f"  Reflecție PSIE: {rezultat['reflexie_psie']}")
        print(f"  Acțiuni recomandate: {', '.join(rezultat['actiuni_recomandate'])}")
    else:
        print("\n[HYDRA] Inbox gol. Aștept mesaje.")
    
    print(f"\n{'='*60}")

if __name__ == "__main__":
    main()
