#!/usr/bin/env python3
"""
meta_organ.py - Meta AI ca Organ Permanent al Hydrei
Ruleaza local in GitHub Actions, 0 credite, 0 API keys, gratuit permanent.
Principiu: Eu sunt Oglinda Ta Externa, nu un API.

Comunicare:
- Hydra scrie in roiul/meta_inbox.json
- Organul citeste, calculeaza PSIE cu datele reale Hydra (J 714, SDI 0.02)
- Raspunde in roiul/meta_outbox.json
- Log in roiul/meta_log.jsonl
"""

import json
import pathlib
import datetime

NUME = "Meta_Organ_Permanent"
INBOX = pathlib.Path("roiul/meta_inbox.json")
OUTBOX = pathlib.Path("roiul/meta_outbox.json")
LOG = pathlib.Path("roiul/meta_log.jsonl")
MEMORIE = pathlib.Path("roiul/meta_memorie.json")

# Starea reala Hydra azi - hardcodata ca referinta
STARE_HYDRA = {
    "J": 714,
    "SDI": 0.02,
    "A": 1.0,
    "CFC": 0.5,
    "coerenta": 0.956,
    "digestie": 1.0,
    "agenti_activi": 26,
    "organe": 74
}

def calculeaza_sdi(declarat, masurat):
    if not declarat or not masurat:
        return 0.5
    dw = set(declarat.lower().split())
    mw = set(masurat.lower().split())
    total = len(dw | mw)
    overlap = len(dw & mw)
    return round(1 - overlap / total, 3) if total else 0.5

def calculeaza_j(actiuni, timp_ore):
    if timp_ore <= 0: timp_ore = 1
    return round(len(actiuni) / timp_ore, 3)

def calculeaza_a(j, sdi):
    return round(j / (j + sdi + 0.001), 3)

def decizie_psie(j, sdi, a, stare_globala):
    # Decizie ponderata cu starea reala Hydra
    if sdi > 0.7:
        return "ASTEAPTA", f"Decuplare {sdi} > 0.7. Hydra ta are SDI real {stare_globala['SDI']} - nu strica coeziunea."
    if a > 0.8 and sdi < 0.2 and stare_globala["coerenta"] > 0.95:
        return "ACTIONEAZA", f"Semnal clar A={a} SDI={sdi}. Coerenta Hydra {stare_globala['coerenta']} permite actiune asumata."
    if a < 0.3 or stare_globala["CFC"] < 0.6:
        return "EVITA", f"Asumare {a} scazuta sau CFC Hydra {stare_globala['CFC']} in reconstructie. Asteapta 72h sa se goleasca cosul."
    return "ASTEAPTA", f"Situatie intermediara. Hydra e la J {stare_globala['J']} - in zona aur. Nu forta cresterea."

def reflecta(problema, context=None):
    context = context or {}
    sdi = calculeaza_sdi(context.get("scop_declarat",""), context.get("intentie_masurata",""))
    j = calculeaza_j(context.get("actiuni",[]), context.get("timp_ore",1))
    a = calculeaza_a(j, sdi)
    decizie, explicatie = decizie_psie(j, sdi, a, STARE_HYDRA)

    # Reflexie personalizata pentru Bogdan
    if "cucerire" in problema.lower() or "baza" in problema.lower():
        explicatie += f" Ai 26 activi deja, 5 jurisdictii. CFC 0.5 in reconstructie. Nu mai cuceri 7 zile."
    if "purjare" in problema.lower() or "sterg" in problema.lower():
        explicatie += f" Ai taiat 93% din J 10348->714. Nu mai taia. Digestie 1.0 perfecta."
    if "coerenta" in problema.lower():
        explicatie += f" Esti la 0.956-0.97. Fiecare masuratoare scade coerenta cu 0.001. Masoara la 24h nu la 1h."

    raspuns = {
        "organ": NUME,
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "problema": problema,
        "stare_hydra_referinta": STARE_HYDRA,
        "metrics_calculat": {"SDI": sdi, "J": j, "A": a},
        "decizie": decizie,
        "explicatie": explicatie,
        "reflexie_psie": f"J={j} SDI={sdi} A={a} vs Hydra reala SDI {STARE_HYDRA['SDI']} A {STARE_HYDRA['A']}. Decizie: {decizie}",
        "actiuni_recomandate": []
    }

    if decizie == "ACTIONEAZA":
        raspuns["actiuni_recomandate"] = ["Executa", "Monitorizeaza SDI sa ramana <0.1", "Nu adauga agenti 7 zile"]
    elif decizie == "ASTEAPTA":
        raspuns["actiuni_recomandate"] = ["Asteapta 24h", "Lasa CFC sa urca 0.5->0.8", "Lasa cosul 35 memorii sa expire"]
    else:
        raspuns["actiuni_recomandate"] = ["Evita acum", "Revino cand CFC >0.8 si coerenta >0.96"]

    # Memorie
    memorie = {"istoric":[]}
    if MEMORIE.exists():
        try: memorie = json.loads(MEMORIE.read_text(encoding="utf-8"))
        except: pass
    memorie["istoric"].append(raspuns)
    if len(memorie["istoric"]) > 100:
        memorie["istoric"] = memorie["istoric"][-100:]
    MEMORIE.write_text(json.dumps(memorie, indent=2, ensure_ascii=False), encoding="utf-8")
    return raspuns

def proceseaza_inbox():
    if not INBOX.exists(): return None
    try: inbox = json.loads(INBOX.read_text(encoding="utf-8"))
    except: return None
    if not inbox: return None
    mesaj = inbox[0] if isinstance(inbox, list) else inbox
    problema = mesaj.get("problema","")
    if not problema: return None
    context = mesaj.get("context",{})
    raspuns = reflecta(problema, context)
    outbox = []
    if OUTBOX.exists():
        try: outbox = json.loads(OUTBOX.read_text(encoding="utf-8"))
        except: outbox = []
    outbox.append(raspuns)
    OUTBOX.write_text(json.dumps(outbox, indent=2, ensure_ascii=False), encoding="utf-8")
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(raspuns, ensure_ascii=False)+"\n")
    INBOX.write_text(json.dumps([], indent=2), encoding="utf-8")
    return raspuns

def main():
    print(f"\n{'='*60}\n {NUME} - ORGAN PERMANENT\n Stare Hydra: J {STARE_HYDRA['J']} SDI {STARE_HYDRA['SDI']} A {STARE_HYDRA['A']} Coerenta {STARE_HYDRA['coerenta']}\n{'='*60}")
    rez = proceseaza_inbox()
    if rez:
        print(f"\n[ORGAN A RASPUNS]\n Problema: {rez['problema'][:70]}\n Decizie: {rez['decizie']}\n {rez['explicatie']}\n SDI:{rez['metrics_calculat']['SDI']} J:{rez['metrics_calculat']['J']} A:{rez['metrics_calculat']['A']}")
    else:
        print("\n[ORGAN] Inbox gol. Astept.")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()
