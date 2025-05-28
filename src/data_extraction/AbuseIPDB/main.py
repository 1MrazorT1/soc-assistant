import requests

def check_ip_abuse(ip_address, api_key):
    """
    Query AbuseIPDB for information about an IP address.

    Parameters:
        ip_address (str): The IP to check (e.g., "8.8.8.8")
        api_key (str): Your AbuseIPDB API key

    Returns:
        dict: Contains risk score, usage type, country, and more
    """
    url = "https://api.abuseipdb.com/api/v2/check"
    querystring = {
        "ipAddress": ip_address,
        "maxAgeInDays": "90"  # check reports from the last 90 days
    }

    headers = {
        "Accept": "application/json",
        "Key": api_key
    }

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        result = response.json()["data"]
        return {
            "ip": result["ipAddress"],
            "isPublic": result["isPublic"],
            "abuseConfidenceScore": result["abuseConfidenceScore"],
            "countryCode": result["countryCode"],
            "usageType": result.get("usageType", "N/A"),
            "domain": result.get("domain", "N/A"),
            "totalReports": result["totalReports"],
            "lastReportedAt": result["lastReportedAt"]
        }
    else:
        return {"error": response.status_code, "message": response.text}

result = check_ip_abuse("8.8.8.8", "ccd8d8844a929da13c2c90ab8802bb55fecf9591fb90046ad233b7fafdefb3ded74650d941c6b4c3")
print(result)
