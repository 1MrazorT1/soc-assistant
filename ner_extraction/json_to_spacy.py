import spacy
from spacy.tokens import DocBin
import json

nlp = spacy.blank("en")
doc_bin = DocBin()

with open("spacy_data.json", "r") as f:
    training_data = json.load(f)

for item in training_data:
    doc = nlp.make_doc(item["text"])
    entities = []
    seen_tokens = set()

    for start, end, label in item["entities"]:
        span = doc.char_span(start, end, label=label)
        if span is None:
            print(f"Skipping misaligned span: {item['text'][start:end]} → {label}")
            continue

        # check for token overlap
        span_tokens = set(range(span.start, span.end))
        if seen_tokens & span_tokens:
            print(f"Skipping overlapping span: {item['text'][start:end]} → {label}")
            continue

        seen_tokens.update(span_tokens)
        entities.append(span)

    doc.ents = entities
    doc_bin.add(doc)

doc_bin.to_disk("spacy_data.spacy")
print("[+] Saved binary training data to spacy_data.spacy")
