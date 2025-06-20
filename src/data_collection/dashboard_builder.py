import json
from datetime import datetime
import os

#os.makedirs("../data", exist_ok=True)

def ts_to_date(ts):
    try:
        return datetime.utcfromtimestamp(int(ts)).strftime('%Y-%m-%d')
    except:
        return None

# === Load AlienVault Pulses ===
with open("../../data/alienvault_pulses.json", "r") as f:
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
            "first_seen": ioc.get("created", "")[:10]
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
with open("../../data/misp_events.json", "r") as f:
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

# === Load Malshare Feed ===
with open("../../data/Malshare_data.json", "r") as f:
    malshare_entry = json.load(f)

malshare_data = [  # convert to list for merging
    {
        "id": malshare_entry["id"],
        "name": malshare_entry["name"],
        "source": malshare_entry["source"],
        "date": malshare_entry["date"],
        "ioc_count": malshare_entry["ioc_count"],
        "iocs": malshare_entry["iocs"]
    }
]

# === Merge and save ===
dashboard_data = misp_data + alienvault_data + malshare_data

with open("../dashboard/public/dashboard_data.json", "w") as f:
    json.dump(dashboard_data, f, indent=2)

print(f"Dashboard data ready: {len(dashboard_data)} entries saved.")

from alerting import is_critical, send_alert

for entry in dashboard_data:
    for ioc in entry["iocs"]:
        if is_critical(ioc):
            send_alert(ioc)