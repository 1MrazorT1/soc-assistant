import json
import re

with open("misp_ner_dataset.json", "r") as f:
    raw_data = json.load(f)

spacy_data = []

for item in raw_data:
    text = item["text"] + " " + " ".join(ent["text"] for ent in item["entities"])
    entities = []

    for ent in item["entities"]:
        value = ent["text"]
        label = ent["label"]

        match = re.search(re.escape(value), text)
        if match:
            start, end = match.start(), match.end()
            entities.append([start, end, label])

    if entities:
        spacy_data.append({
            "text": text,
            "entities": entities
        })

with open("spacy_data.json", "w") as f:
    json.dump(spacy_data, f, indent=2)

print(f"[+] {len(spacy_data)} exemples écrits dans spacy_data.json ")
