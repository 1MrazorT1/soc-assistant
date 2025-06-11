import os
import requests
import uuid
from datetime import datetime, timezone
import json
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("Malshare_URL")  # Should look like: https://malshare.com/api.php?api_key=XXX&action=getsamples
response = requests.get(url)

try:
    samples = response.json()  # Malshare now returns JSON array
except json.JSONDecodeError:
    print("Failed to decode JSON.")
    print(response.text[:300])
    exit()

formatted_output = {
    "id": str(uuid.uuid4()),
    "name": "OSINT Malshare Feed",
    "source": "Malshare",
    "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
    "ioc_count": len(samples),
    "iocs": []
}

for sample in samples:
    sha256 = sample.get("sha256")
    if sha256:
        formatted_output["iocs"].append({
            "value": sha256,
            "type": "sha256",
            "category": "Payload delivery",
            "to_ids": True,
            "first_seen": datetime.now(timezone.utc).strftime("%Y-%m-%d")  # No timestamp in response, so use now
        })

# Save to file
save_path = "../../../data/Malshare_data.json"
with open(save_path, "w") as f:
    json.dump(formatted_output, f, indent=2)

print(f"\nSauvegardé : {len(formatted_output['iocs'])} IOCs -> {save_path}")
