from flask import Flask, jsonify
from flask_cors import CORS
import importlib.util
import requests
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

app = Flask(__name__)
CORS(app)

REQUIRED_ENV_VARS = [
    "MISP_URL", "MISP_API_KEY", "MISP_SSL_VERIFY", "OTX_API_KEY", "VT_API_KEY", "BASE_URL", "ABUSEIPDB_KEY", "NVD_API_KEY", "TWITTER_BEARER_TOKEN", "Malshare_URL", "Malshare_KEY", "ALERT_EMAIL", "ALERT_PASS", "ALERT_TO"
]

REQUIRED_PYTHON_PACKAGES = [
    "requests", "json5", "pathlib", "schedule", "Flask", "flask-cors", "python-dotenv", "spacy", "tqdm", "PyMISP", "OTXv2", "yagmail", "transformers", "beautifulsoup4", "lxml", "feedparser"
]

MODEL_PATH = os.path.join("..", "src", "AI_NLP", "ner_cti_model", "model-best")

@app.route("/api/status", methods=["GET"])
def check_system_status():
    missing = {
        "env_vars": [],
        "python_packages": [],
        "files": [],
        "services": []
    }

    # ENV vars
    for key in REQUIRED_ENV_VARS:
        if not os.getenv(key):
            missing["env_vars"].append(key)

    # Python packages
    for pkg in REQUIRED_PYTHON_PACKAGES:
        if not importlib.util.find_spec(pkg):
            missing["python_packages"].append(pkg)

    # Model presence
    if not os.path.exists(MODEL_PATH) or not os.path.isdir(MODEL_PATH):
        missing["files"].append("NER model-best directory")

    # Internet connectivity
    try:
        requests.get("https://www.google.com", timeout=2)
    except:
        missing["services"].append("Internet connection")

    status = "ok" if all(len(v) == 0 for v in missing.values()) else "error"

    return jsonify({
        "status": status,
        "missing": missing
    })

if __name__ == "__main__":
    app.run(debug=True, port=5001)
