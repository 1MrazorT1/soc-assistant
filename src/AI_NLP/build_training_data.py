import re
import json
from pathlib import Path

# === Entité + regex associée pour annotation ===
ENTITY_REGEXES = {
    "IP": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
    "DOMAIN": r"\b[a-zA-Z0-9.-]+\.(com|net|org|su|ru|info|biz|[a-z]{2,})\b",
    "URL": r"https?://[^\s\"']+",
    "SHA256": r"\b[a-fA-F0-9]{64}\b",
    "CVE": r"\bCVE-\d{4}-\d{4,7}\b",
    "FILE": r"\b\w+\.(exe|dll|sh|js|doc|xls|pdf)\b",
}

# === Fichiers à parser ===
FILES = [
    "../../data/alienvault_pulses.json",
    "../../data/misp_events.json",
    "../../data/Malshare_data.json",
    "../../data/cve_data.json",
    "../../data/URLhaus_data.json"
]

# === Colonnes textuelles à parcourir ===
TEXT_FIELDS = ["description", "value", "url", "info", "comment", "name"]

TRAIN_DATA = []

def annotate(text):
    entities = []
    for label, pattern in ENTITY_REGEXES.items():
        for match in re.finditer(pattern, text):
            start, end = match.span()
            entities.append((start, end, label))
    return entities

for filename in FILES:
    path = Path(filename)
    if not path.exists():
        print(f"[!] Fichier non trouvé: {filename}")
        continue

    with open(path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except Exception as e:
            print(f"[!] Erreur parsing {filename}: {e}")
            continue

    # support both dict and list format
    records = data if isinstance(data, list) else [data]

    for record in records:
        for field in TEXT_FIELDS:
            text = record.get(field)
            if text and isinstance(text, str):
                ents = annotate(text)
                if ents:
                    TRAIN_DATA.append((text, {"entities": ents}))

print(f"Exemples générés : {len(TRAIN_DATA)}")
with open("../../data/train_data.json", "w", encoding="utf-8") as f:
    json.dump(TRAIN_DATA, f, indent=2, ensure_ascii=False)
