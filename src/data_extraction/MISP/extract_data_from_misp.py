from pymisp import ExpandedPyMISP
from misp_config import MISP_URL, MISP_KEY, VERIFY_CERT
import json

ENTITY_LABELS = {
    "ip-src": "IP",
    "ip-dst": "IP",
    "domain": "DOMAIN",
    "hostname": "DOMAIN",
    "url": "URL",
    "md5": "HASH",
    "sha1": "HASH",
    "sha256": "HASH",
    "cve": "CVE",
    "malware-type": "MALWARE",
    "threat-actor": "ACTOR"
}

def extract_utis_from_misp(limit=0):
    misp = ExpandedPyMISP(MISP_URL, MISP_KEY, VERIFY_CERT)
    response = misp.search(controller='events', limit=limit)
    utis_dataset = []

    for item in response:
        event = item.get("Event", {})
        attributes = event.get("Attribute", [])
        tags = [tag["name"] for tag in event.get("Tag", [])]

        threat_level = int(event.get("threat_level_id", 1))
        category = event.get("info", "Unknown")
        timestamp = event.get("date")
        source_link = f"{MISP_URL}/events/view/{event.get('id')}"
        source = "MISP"
        source_type = "Open Source"

        for attr in attributes:
            attr_type = attr.get("type")
            value = attr.get("value")

            if attr_type in ENTITY_LABELS:
                mitre_attack = [
                    tag["name"] for tag in attr.get("Tag", [])
                    if "attack-pattern" in tag["name"].lower()
                ]

                utis_entry = {
                    "source": source,
                    "timestamp": timestamp,
                    "type": ENTITY_LABELS[attr_type],
                    "value": value,
                    "threat_level": threat_level,
                    "category": category,
                    "description": attr.get("comment", ""),
                    "tags": tags,
                    "related_iocs": [],
                    "mitre_attack": mitre_attack,
                    "confidence_score": int(attr.get("to_ids", 0)) * 100,
                    "source_link": source_link,
                    "source_type": source_type
                }

                utis_dataset.append(utis_entry)

    with open("../../../data/raw_data/misp_raw_data.json", "w") as f:
        json.dump(utis_dataset, f, indent=2)

    print(f"[+] {len(utis_dataset)} indicateurs enregistrés dans misp_data.json.")

if __name__ == "__main__":
    extract_utis_from_misp()
