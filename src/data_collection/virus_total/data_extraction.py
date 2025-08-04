from flask import Flask, jsonify, request
from flask_cors import CORS
import base64
import requests
import os
from dotenv import load_dotenv

load_dotenv()
VT_API_KEY = os.getenv("VT_API_KEY")
BASE_URL   = os.getenv("BASE_URL", "https://www.virustotal.com/api/v3")

if not VT_API_KEY:
    raise RuntimeError("Please set VT_API_KEY in your .env file")

HEADERS = {
    "x-apikey": VT_API_KEY
}

app = Flask(__name__)

def vt_lookup(type_, value):
    """
    Build the correct VT endpoint for `type_` and `value`, perform the GET,
    and return the 'data.attributes' dict (or an {'error': ...} if something went wrong).
    """
    t = type_.lower()
    url = None

    if t in ("sha256", "sha1", "md5", "file", "hash"):
        url = f"{BASE_URL}/files/{value}"
    elif t in ("ip", "ipv4", "ip-src"):
        url = f"{BASE_URL}/ip_addresses/{value}"
    elif t in ("domain",):
        url = f"{BASE_URL}/domains/{value}"
    elif t in ("url",):
        try:
            b64 = base64.urlsafe_b64encode(value.encode()).decode().rstrip("=")
            url = f"{BASE_URL}/urls/{b64}"
        except Exception:
            from urllib.parse import quote
            encoded = quote(value, safe="")
            url = f"{BASE_URL}/urls/{encoded}"
    else:
        return {"error": f"Unsupported type: {type_}"}

    resp = requests.get(url, headers=HEADERS)
    if resp.status_code == 200:
        return resp.json().get("data", {}).get("attributes", {})
    else:
        try:
            return {"error": resp.json().get("error", {})}
        except ValueError:
            return {"error": f"HTTP {resp.status_code}: {resp.text}"}

@app.route("/api/vt", methods=["GET"])
def get_vt():
    """
    Endpoint: /api/vt?type=<type>&value=<value>
    Example:
      GET /api/vt?type=sha256&value=4b825dc642cb6...
      GET /api/vt?type=domain&value=example.com
      GET /api/vt?type=ip&value=8.8.8.8
    """
    type_  = request.args.get("type")
    value  = request.args.get("value")

    if not type_ or not value:
        return jsonify({"error": "Missing 'type' or 'value' parameter"}), 400

    data = vt_lookup(type_, value)
    return jsonify(data)

if __name__ == "__main__":
    CORS(app)
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)
