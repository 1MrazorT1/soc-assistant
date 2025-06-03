from pymisp import PyMISP
import json
import os
from dotenv import load_dotenv

load_dotenv()

MISP_URL = os.getenv(MISP_URL)
MISP_KEY = os.getenv(MISP_API_KEY)
VERIFY_CERT = os.getenv(MISP_SSL_VERIFY)

misp = PyMISP(MISP_URL, MISP_KEY, VERIFY_CERT, 'json')

events = misp.search(controller='events', limit=1)

with open("../data/misp_events.json", "w") as f:
    json.dump(events, f, indent=2)

print("Events saved.")
