import cupy
import spacy

# Force CuPy to use the first GPU
cupy.cuda.Device(0).use()

if spacy.prefer_gpu():
    print("✔ spaCy is using GPU")
else:
    print("✘ spaCy fell back to CPU")

nlp = spacy.load("en_core_web_trf")
doc = nlp("APT29 is targeting NATO with phishing emails from domains like secure-login.org")
print([(ent.text, ent.label_) for ent in doc.ents])
