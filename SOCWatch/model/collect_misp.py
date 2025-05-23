from pymisp import ExpandedPyMISP
from misp_config import MISP_URL, MISP_KEY, VERIFY_CERT
import pandas as pd
import os

def collect_suspicious_logs(limit=300):
    misp = ExpandedPyMISP(MISP_URL, MISP_KEY, VERIFY_CERT)
    results = misp.search(controller='events', return_format='json', limit=limit)

    rows = []
    for ev in results:
        event = ev.get("Event", {})
        for attr in event.get("Attribute", []):
            rows.append({
                "timestamp": event.get("date"),
                "ioc_type": attr.get("type"),
                "ioc_value": attr.get("value"),
                "category": attr.get("category"),
                "comment": attr.get("comment"),
                "event_info": event.get("info"),
                "source": "MISP",
                "label": 1
            })

    os.makedirs("data", exist_ok=True)
    df = pd.DataFrame(rows)
    df.to_csv("../data/suspicious_logs.csv", index=False)
    print(f"Collected and saved {len(df)} suspicious logs to data/suspicious_logs.csv")

if __name__ == "__main__":
    collect_suspicious_logs()
