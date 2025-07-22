import spacy
nlp = spacy.load("ner_cti_model/model-best")

examples = [
    "On July 10, 2024, the threat actor APT29 exploited CVE-2024-1234 to gain initial access to the network. The attack originated from the IP address 185.100.87.202 and targeted a US-based defense contractor. Indicators of compromise included domain name secure-update.microsoft-login[.]com and SHA256 hash d2d2d2a1b3c4f5a6d7e8e9f0a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0."
]

for text in examples:
    doc = nlp(text)
    for ent in doc.ents:
        print(f"  {ent.text} → {ent.label_}")
