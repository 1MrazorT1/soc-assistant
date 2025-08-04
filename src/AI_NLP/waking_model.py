from flask import Flask, request, jsonify
from flask_cors import CORS
import spacy
import os

app = Flask(__name__)
CORS(app)
MODEL_PATH = os.path.join("ner_cti_model", "model-best")
nlp = spacy.load(MODEL_PATH)

@app.route('/api/analyze', methods=['POST'])
def analyze_text():
    data = request.get_json()
    input_text = data.get("text", "")
    if not input_text:
        return jsonify({"error": "No text provided"}), 400

    doc = nlp(input_text)
    results = [{"text": ent.text, "label": ent.label_} for ent in doc.ents]
    return jsonify({"entities": results})

@app.route('/api/status', methods=['GET'])
def status():
    return jsonify({"status": "ok", "model": "loaded"}), 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)
