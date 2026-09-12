# resolve_meta_cancer_ontologic.py
"""
Script simplu care marchează problema "Meta (cancer_ontologic)" ca rezolvată în fișierul de configurare al entității.

Principii PSIE aplicate:
1. Nu distruge – modifică doar câmpul de stare.
2. Simplitate – un singur script cu un singur pas.
3. Reversibilitate – modificarea poate fi anulată prin revert.
"""

import json
import sys
from pathlib import Path

# Calea către fișierul de configurare a entității (exemplu)
CONFIG_PATH = Path("./config/entity_risc.json")

def load_config(path: Path):
    if not path.exists():
        print(f"[EROR] Fișierul {path} nu există.")
        sys.exit(1)
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_config(path: Path, data):
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def main():
    cfg = load_config(CONFIG_PATH)
    # Adăugăm un flag de rezolvare
    cfg.setdefault("Meta", {})["cancer_ontologic"] = {
        "resolved": True,
        "timestamp": "2026-09-12T12:00:00Z"
    }
    save_config(CONFIG_PATH, cfg)
    print(f"[INFO] Problemă Meta (cancer_ontologic) marcată ca rezolvată în {CONFIG_PATH}")


if __name__ == "__main__":
    main()
