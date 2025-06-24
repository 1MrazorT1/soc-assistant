import spacy
nlp = spacy.load("ner_cti_model/model-best")

examples = [
    "Zeus malware exploited CVE-2023-9999 and targeted 8.8.8.8.",
    "APT28 actors were linked to domain evil.example.com",
    "Malware Joker was seen on 10.0.0.5 in phishing campaigns."
]

for text in examples:
    doc = nlp(text)
    print(f"\n{text}")
    for ent in doc.ents:
        print(f"  {ent.text} → {ent.label_}")
