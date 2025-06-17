import spacy
from spacy.tokens import DocBin
from spacy.training.example import Example
from spacy.util import filter_spans
import json
from pathlib import Path
from tqdm import tqdm

# === Charger les données ===
with open("../../data/train_data.json", "r", encoding="utf-8") as f:
    TRAIN_DATA = json.load(f)

# === Initialiser spaCy vide (anglais) ===
nlp = spacy.blank("en")

# Ajouter le pipeline NER
if "ner" not in nlp.pipe_names:
    ner = nlp.add_pipe("ner", last=True)
else:
    ner = nlp.get_pipe("ner")

# Ajouter toutes les étiquettes à partir des données
for _, annotations in TRAIN_DATA:
    for ent in annotations["entities"]:
        ner.add_label(ent[2])

# Convertir TRAIN_DATA en DocBin
doc_bin = DocBin()
for text, annot in tqdm(TRAIN_DATA, desc="Préparation des exemples"):
    doc = nlp.make_doc(text)
    entities = annot["entities"]
    spans = []
    for start, end, label in entities:
        span = doc.char_span(start, end, label=label, alignment_mode="contract")
        if span:
            spans.append(span)
    doc.ents = spacy.util.filter_spans(spans)
    doc_bin.add(doc)

# Sauver en format binaire spaCy
doc_bin.to_disk("train.spacy")

# === Entraînement ===
from spacy.training.train import train

# Configuration minimale pour NER
config = """
[paths]
train = "train.spacy"
dev = "train.spacy"

[nlp]
lang = "en"
pipeline = ["ner"]

[components.ner]
factory = "ner"

[training]
train_corpus = "train.spacy"
dev_corpus = "train.spacy"
max_epochs = 20
dropout = 0.2
"""

# Sauver le fichier config temporaire
config_path = Path("ner_config.cfg")
config_path.write_text(config)

# Entraîner le modèle
train(config_path.as_posix(), output_path="ner_cti_model", overrides={})
