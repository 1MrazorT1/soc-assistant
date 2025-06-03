import json
from datetime import datetime

# Charger le fichier d'événement MISP
with open("../data/misp_events.json", "r") as f:
    your_data = json.load(f)

event = your_data[0]["Event"]
event_info = event["info"]
event_threat = event["threat_level_id"]
event_date = event["date"]

normalized = []
for attr in event["Attribute"]:
    normalized.append({
        "source": "MISP",
        "value": attr["value"],
        "type": attr["type"],
        "category": attr["category"],
        "to_ids": attr["to_ids"],
        "first_seen": datetime.utcfromtimestamp(int(attr["timestamp"])).strftime('%Y-%m-%d'),
        "event_info": event_info,
        "threat_level": event_threat
    })

# Sauvegarder dans un fichier JSON
with open("../data/misp_iocs_normalized.json", "w") as f:
    json.dump(normalized, f, indent=2)

print(f"Normalized {len(normalized)} attributes.")
