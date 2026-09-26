#!/usr/bin/env python3
"""
Meta Ontology Transparency & Interoperability Tool
Author: HYDRA (FORJARUL AUTONOM)

Acest script adaugă un flag de rezolvare în metadata unei entități
ontologice și generează un raport de transparență.  În acest fel
se evită „cancerul ontologic” prin menținerea unui nivel de
interoperabilitate și control conștient al utilizatorului.
"""

import json
import os
import sys
from datetime import datetime

# Calea către fișierul de metadate al entității
ONTOLOGY_METADATA_PATH = os.getenv("ONTOLOGY_METADATA_PATH", "ontology_metadata.json")


def load_metadata(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_metadata(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def add_resolve_flag(metadata):
    metadata.setdefault("meta_ontology_resolved", False)
    metadata["meta_ontology_resolved"] = True
    metadata["resolved_at"] = datetime.utcnow().isoformat() + "Z"
    return metadata


def generate_transparency_report(metadata):
    report = {
        "entity": metadata.get("entity", "unknown"),
        "status": "resolved" if metadata.get("meta_ontology_resolved") else "unresolved",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "details": {
            "interoperability_protocols": metadata.get("interoperability_protocols", []),
            "transparency_mechanisms": metadata.get("transparency_mechanisms", []),
            "community_regeneration": metadata.get("community_regeneration", False)
        }
    }
    return report


def main():
    metadata = load_metadata(ONTOLOGY_METADATA_PATH)
    metadata = add_resolve_flag(metadata)
    save_metadata(ONTOLOGY_METADATA_PATH, metadata)

    report = generate_transparency_report(metadata)
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
