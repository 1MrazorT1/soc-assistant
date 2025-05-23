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

def extract_events(limit=0):
    misp = ExpandedPyMISP(MISP_URL, MISP_KEY, VERIFY_CERT)
    response = misp.search(controller='events', limit=limit)
    dataset = []

    for item in response:
        event = item.get("Event", {})
        text = event.get("info", "")
        attributes = event.get("Attribute", [])

        entities = []
        for attr in attributes:
            attr_type = attr.get("type")
            value = attr.get("value")
            if attr_type in ENTITY_LABELS:
                entities.append({
                    "text": value,
                    "label": ENTITY_LABELS[attr_type]
                })

        if entities:
            dataset.append({
                "text": text,
                "entities": entities
            })

    with open("misp_ner_dataset.json", "w") as f:
        json.dump(dataset, f, indent=2)

    print(f"[+] {len(dataset)} événements enregistrés dans misp_ner_dataset.json.")

if __name__ == "__main__":
    extract_events()
