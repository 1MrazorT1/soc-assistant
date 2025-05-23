import spacy

nlp = spacy.load("output/model-best")

doc = nlp("Observed activity from sofacy targeting amf-fr.org and 193.109.68.87")
for ent in doc.ents:
    print(ent.text, ent.label_)
