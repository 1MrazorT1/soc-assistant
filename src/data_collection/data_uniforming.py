import json
from datetime import datetime
import os

os.makedirs("../data", exist_ok=True)

# === Helper to convert timestamp ===
def ts_to_date(ts):
    try:
        return datetime.utcfromtimestamp(int(ts)).strftime('%Y-%m-%d')
    except:
        return None

# === Load AlienVault Pulses ===
with open("data/alienvault_pulses.json", "r") as f:
    alienvault_raw = json.load(f)

alienvault_data = []
for pulse in alienvault_raw:
    indicators = []
    for ioc in pulse.get("indicators", []):
        indicators.append({
            "value": ioc.get("indicator"),
            "type": ioc.get("type"),
            "category": None,
            "to_ids": None,
            "first_seen": ioc.get("created", "")[:10]  # ISO date
        })
    alienvault_data.append({
        "id": pulse.get("pulse_id"),
        "name": pulse.get("name"),
        "source": "AlienVault",
        "date": indicators[0]["first_seen"] if indicators else None,
        "ioc_count": len(indicators),
        "iocs": indicators
    })

# === Load MISP Events ===
with open("data/misp_events.json", "r") as f:
    misp_raw = json.load(f)

misp_data = []
for event_wrapper in misp_raw:
    event = event_wrapper["Event"]
    attributes = event.get("Attribute", [])
    iocs = []
    for attr in attributes:
        iocs.append({
            "value": attr.get("value"),
            "type": attr.get("type"),
            "category": attr.get("category"),
            "to_ids": attr.get("to_ids"),
            "first_seen": ts_to_date(attr.get("timestamp"))
        })
    misp_data.append({
        "id": event.get("uuid"),
        "name": event.get("info"),
        "source": "MISP",
        "date": event.get("date"),
        "ioc_count": len(iocs),
        "iocs": iocs
    })

# === Merge and save ===
dashboard_data = misp_data + alienvault_data

with open("data/dashboard_data.json", "w") as f:
    json.dump(dashboard_data, f, indent=2)

print(f"Dashboard data ready: {len(dashboard_data)} entries saved.")
