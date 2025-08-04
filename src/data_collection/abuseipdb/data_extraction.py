import os
import requests
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()
ABUSEIPDB_KEY = os.getenv("ABUSEIPDB_KEY")
if not ABUSEIPDB_KEY:
    raise RuntimeError("Please set ABUSEIPDB_KEY in your .env file")

app = Flask(__name__)
CORS(app)

def abuseipdb_lookup(ip):
    """
    Query AbuseIPDB for a given IP address.
    Returns the JSON response dict (or an {'error': ...} dict).
    """
    url = "https://api.abuseipdb.com/api/v2/check"
    headers = {
        "Key": ABUSEIPDB_KEY,
        "Accept": "application/json"
    }
    params = {
        "ipAddress": ip,
        "maxAgeInDays": 90
    }
    resp = requests.get(url, headers=headers, params=params)
    if resp.status_code == 200:
        return resp.json()
    else:
        try:
            return {"error": resp.json().get("error", {"message": "Unknown error"})}
        except ValueError:
            return {"error": {"message": f"HTTP {resp.status_code}: {resp.text}"}}

@app.route("/api/abuse", methods=["GET"])
def get_abuse():
    """
    Example call: GET /api/abuse?ip=8.8.8.8
    Returns JSON response from AbuseIPDB.
    """
    ip = request.args.get("ip")
    if not ip:
        return jsonify({"error": "Missing 'ip' query parameter"}), 400

    data = abuseipdb_lookup(ip)
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=False, use_reloader=False)
