import warnings
warnings.filterwarnings("ignore")

from pymisp import ExpandedPyMISP
from misp_config import MISP_URL, MISP_KEY, VERIFY_CERT
import json

misp = ExpandedPyMISP(MISP_URL, MISP_KEY, VERIFY_CERT)

try:
    events = misp.search(controller='events', limit=3)
    print(json.dumps(events, indent=2))
except Exception as e:
    print("[-] Erreur :", e)
