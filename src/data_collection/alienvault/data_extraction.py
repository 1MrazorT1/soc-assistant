from OTXv2 import OTXv2, IndicatorTypes
import json
from dotenv import load_dotenv

load_dotenv()

# === CONFIG ===
API_KEY = os.getenv(OTX_API_KEY)
otx = OTXv2(API_KEY)

# === STEP 1: Search for recent pulses (example with "malware")
search_results = otx.search_pulses("malware", max_results=1)

pulses = []
for pulse in search_results['results']:
    pulse_id = pulse['id']
    indicators = otx.get_pulse_indicators(pulse_id)
    pulses.append({
        "pulse_id": pulse_id,
        "name": pulse['name'],
        "indicators": indicators
    })

# === SAVE TO FILE
import os
os.makedirs("../data", exist_ok=True)

with open("../data/alienvault_pulses.json", "w") as f:
    json.dump(pulses, f, indent=2)

print(f"Saved indicators from {len(pulses)} pulses.")
