#!/usr/bin/env python3
# data_extraction.py

import os
import gzip
import json
import time
import requests
from dotenv import load_dotenv
from requests.exceptions import RequestException

# ── Load API key from .env ──
load_dotenv()
API_KEY = os.getenv("NVD_API_KEY")

HEADERS = {}
if API_KEY:
    HEADERS["apiKey"] = API_KEY

# ── Constants ──
YEAR = "2023"
# NVD v2.0 API endpoint
API_URL = "https://api.nvd.nist.gov/rest/json/cves/2.0"
# Fallback “feed” URL if API is unreachable
FEED_URL = f"https://nvd.nist.gov/feeds/json/cve/1.1/nvdcve-1.1-{YEAR}.json.gz"
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "../../../data/cve_data.json")


def fetch_cves_between(start_date, end_date, results_per_page=2000):
    """
    Fetch all CVEs published between start_date and end_date using the NVD v2.0 API.
    If the API is unreachable (DNS or network error), fall back to downloading the
    yearly .json.gz feed instead.
    Returns a list of simplified CVE dicts.
    """
    try:
        return _fetch_via_api(start_date, end_date, results_per_page)
    except RequestException as e:
        print(f"API unreachable ({e}). Falling back to GZIP feed…")
        return _fetch_via_feed(FEED_URL)


def _fetch_via_api(start_date, end_date, results_per_page):
    """
    Internal helper: paginate through the v2.0 API.
    """
    all_cves = []
    start_index = 0

    while True:
        params = {
            "pubStartDate": start_date,
            "pubEndDate": end_date,
            "resultsPerPage": results_per_page,
            "startIndex": start_index
        }
        resp = requests.get(API_URL, headers=HEADERS, params=params)
        if resp.status_code != 200:
            print(f"HTTP {resp.status_code} error calling API:")
            print(resp.text)
            break

        data = resp.json()
        total_results = data.get("totalResults", 0)
        vulnerabilities = data.get("vulnerabilities", [])

        for entry in vulnerabilities:
            cve = entry.get("cve", {})
            cve_id = cve.get("id", "UNKNOWN")
            description = ""
            for desc in cve.get("descriptions", []):
                if desc.get("lang") == "en":
                    description = desc.get("value")
                    break
            published = cve.get("published", "")
            metrics_list = entry.get("cveMetrics", {}).get("cvssMetricV3", [])
            if metrics_list:
                cvss = metrics_list[0].get("cvssData", {})
                cvss_score = cvss.get("baseScore")
                cvss_severity = cvss.get("baseSeverity")
            else:
                cvss_score = None
                cvss_severity = None

            all_cves.append({
                "cve_id": cve_id,
                "description": description,
                "published_date": published,
                "cvss_score": cvss_score,
                "cvss_severity": cvss_severity
            })

        fetched = start_index + len(vulnerabilities)
        if fetched >= total_results or not vulnerabilities:
            break

        start_index += results_per_page
        time.sleep(1)  # respect rate limits

    return all_cves


def _fetch_via_feed(feed_url):
    """
    Download the yearly .json.gz feed, decompress it, and extract simplified CVE list.
    """
    print(f"Téléchargement du feed NVD pour {YEAR} depuis :\n  {feed_url}")
    resp = requests.get(feed_url, stream=True)
    resp.raise_for_status()

    compressed_data = resp.content
    print("Décompression du flux…")
    decompressed_bytes = gzip.decompress(compressed_data)
    full_json = json.loads(decompressed_bytes)

    simplified = []
    for item in full_json.get("CVE_Items", []):
        cve = item.get("cve", {})
        cve_id = cve.get("CVE_data_meta", {}).get("ID", "UNKNOWN")
        description = ""
        for d in cve.get("description", {}).get("description_data", []):
            if d.get("lang") == "en":
                description = d.get("value", "")
                break
        published_date = item.get("publishedDate", "")
        impact = item.get("impact", {})
        base_metric_v3 = impact.get("baseMetricV3", {})
        cvss_v3 = base_metric_v3.get("cvssV3", {})
        cvss_score = cvss_v3.get("baseScore")
        cvss_severity = cvss_v3.get("baseSeverity")

        simplified.append({
            "cve_id": cve_id,
            "description": description,
            "published_date": published_date,
            "cvss_score": cvss_score,
            "cvss_severity": cvss_severity
        })

    print(f"→ {len(simplified)} CVE extraites depuis le feed pour {YEAR}.")
    return simplified


if __name__ == "__main__":
    START = "2023-01-01T00:00:00:000 UTC-00:00"
    END   = "2023-12-31T23:59:59:999 UTC-00:00"

    print(f"Fetching CVEs from {START} to {END} …")
    cve_list = fetch_cves_between(START, END)

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(cve_list, f, indent=2)

    print(f"Fetched {len(cve_list)} CVEs. Written to {OUTPUT_PATH}")
