from pymisp import PyMISP
from misp_config import MISP_URL, MISP_KEY, VERIFY_CERT

misp = PyMISP(MISP_URL, MISP_KEY, VERIFY_CERT)

try:
    # Test en récupérant le premier événement
    events = misp.search(controller='events', limit=1)


    if events:
        print("[+] Connexion réussie à MISP !")
        print(f"Premier événement : {events[0]['info']}")
    else:
        print("[+] Connexion réussie, mais aucun événement trouvé.")
except Exception as e:
    print("[-] Échec de la connexion ou erreur de requête :", e)
