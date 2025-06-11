import requests
import zipfile
import io
import json
import csv

url = "https://urlhaus.abuse.ch/downloads/json/"
response = requests.get(url)

if response.status_code == 200:
    with zipfile.ZipFile(io.BytesIO(response.content)) as thezip:
        for name in thezip.namelist():
            if name.endswith(".json"):
                with thezip.open(name) as json_file:
                    data = json.load(json_file)
                    extracted = []
                    for entry_id, entry_list in data.items():
                        if isinstance(entry_list, list) and len(entry_list) > 0 and isinstance(entry_list[0], dict):
                            entry = entry_list[0]
                            url = entry.get("url")
                            threat = entry.get("threat", "").lower()
                            if "malware" in threat or "phish" in threat:
                                tags = entry.get("tags")
                                if isinstance(tags, list):
                                    tags_str = ", ".join(tags)
                                else:
                                    tags_str = "N/A"
                                extracted.append({
                                    "id": entry_id,
                                    "url": url,
                                    "threat": threat,
                                    "tags": tags_str,
                                    "status": entry.get("url_status", "N/A"),
                                    "last_online": entry.get("last_online", "N/A")
                                })
                    with open("../../../data/URLhaus_data.json", "w") as jf:
                        json.dump(extracted, jf, indent=2)
                    print(f"\nSauvegardé : {len(extracted)} IOCs -> filtered_iocs.json")
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")
