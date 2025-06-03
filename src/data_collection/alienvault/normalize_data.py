import json

# Charger les pulses
with open("../data/alienvault_indicators.json", "r") as f:
    raw_pulses = json.load(f)

# Extraire et normaliser les IOCs
normalized_iocs = []
for pulse in raw_pulses:
    for ioc in pulse.get("indicators", []):
        normalized_iocs.append({
            "source": "AlienVault",
            "type": ioc.get("type"),
            "value": ioc.get("indicator")
        })

# Sauvegarder les IOCs normalisés
with open("../data/alienvault_iocs_normalized.json", "w") as f:
    json.dump(normalized_iocs, f, indent=2)

print(f"Extracted {len(normalized_iocs)} indicators.")
