import os, json

# ---
# Script: mark_meta_risk.py
# Scop: detect toate fișierele JSON din repo care conțin entități cu titlul "Meta" (cancer_ontologic) și adaugă un flag de risc și un marker de rezolvare.
# Acest script nu modifică datele existente, ci le annotatează, respectând principiul "Nu distruge — arhivează/recontextualizează".
# ---

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Căutăm doar fișierele JSON din subdirectoarele relevante
JSON_EXT = '.json'

# Criteriul de identificare a entității Meta
META_TITLU = "Meta (cancer_ontologic)"

# Flag-urile care vor fi adăugate
RISK_FLAG = {"risk_level": "high", "ParadoxHidra.rezolvat": True}


def process_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            # fișierul nu este JSON valid – îl lăsăm nealterat
            return False

    # Căutăm entități cu titlul Meta
    if isinstance(data, dict):
        if data.get('titlu') == META_TITLU:
            # Adăugăm flag-urile dacă nu există deja
            changed = False
            for k, v in RISK_FLAG.items():
                if data.get(k) != v:
                    data[k] = v
                    changed = True
            if changed:
                with open(path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                print(f"[PSIE] Flag-urile au fost adăugate în {path}")
                return True
    return False


def main():
    total = 0
    flagged = 0
    for root, _, files in os.walk(REPO_ROOT):
        for name in files:
            if name.endswith(JSON_EXT):
                total += 1
                path = os.path.join(root, name)
                if process_file(path):
                    flagged += 1
    print(f"\nProcesare finalizată: {total} fișiere scanate, {flagged} entități Meta marcate")

if __name__ == "__main__":
    main()
