import os
import yagmail
from dotenv import load_dotenv

load_dotenv()

ALERT_EMAIL = os.getenv("ALERT_EMAIL")
ALERT_PASS = os.getenv("ALERT_PASS")
ALERT_TO   = os.getenv("ALERT_TO", ALERT_EMAIL)

if not ALERT_EMAIL or not ALERT_PASS:
    raise RuntimeError("Missing ALERT_EMAIL or ALERT_PASS in .env")

yag = yagmail.SMTP(ALERT_EMAIL, ALERT_PASS)

def is_critical(ioc):
    """
    Determines whether an IOC should trigger an alert.
    """
    critical_keywords = ["ransom", "apt", "cobalt", "black vine", "critical", "exploit", "zero-day"]
    value = ioc.get("value", "").lower()
    category = ioc.get("category", "").lower()
    ioc_type = ioc.get("type", "").lower()

    # Alert if value mentions known threat actors or tools
    if any(k in value for k in critical_keywords):
        return True

    # Alert if it's a domain/IP with to_ids set to True (meaning actionable)
    if ioc_type in ["ip-dst", "domain", "url"] and ioc.get("to_ids", False):
        return True

    return False

def send_alert(ioc):
    """
    Send an alert email with IOC details.
    """
    subject = f"[CRITICAL IOC] {ioc.get('value', 'Unknown')}"
    body = f"""Critical IOC detected:

- Value: {ioc.get('value')}
- Type: {ioc.get('type')}
- Source: {ioc.get('source')}
- Category: {ioc.get('category')}
- First Seen: {ioc.get('first_seen')}
- Tags: {ioc.get('tags', '')}

Please investigate immediately."""
    yag.send(ALERT_TO, subject, body)
    print(f"Alert sent for IOC: {ioc.get('value')}")
