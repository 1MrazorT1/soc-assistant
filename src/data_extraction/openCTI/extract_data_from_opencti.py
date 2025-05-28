from pycti import OpenCTIApiClient
import json
import os

# ─── CONFIGURATION ──────────────────────────────────────────────────────────────
OPENCTI_URL   = "http://localhost:8080"            # 4000 is the API port
OPENCTI_TOKEN = "cbe26b42-41d3-4782-81be-5e7bd346b2f7"                  # put your personal token
OUTPUT_DIR    = "opencti_by_author"
MAX_PER_ENTITY = 1000                              # pagination size
# ────────────────────────────────────────────────────────────────────────────────

client = OpenCTIApiClient(OPENCTI_URL, OPENCTI_TOKEN)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ----------------------------------------------------------------------------- #
# helpers
# ----------------------------------------------------------------------------- #
def get_all_creators() -> dict:
    """Return {id: name} for every Organization registered in OpenCTI."""
    creators = client.identity.list(entity_type="Organization", first=MAX_PER_ENTITY)
    return {c["id"]: c["name"] for c in creators}

def list_with_creator(entity_fn, creator_id):
    flt = {
        "mode": "and",                   # combine all filters with AND
        "filters": [
            {
                "key":      "createdBy",
                "operator": "eq",        # equals
                "values":   [creator_id]
            }
        ],
        "filterGroups": []               # no sub-groups
    }
    return entity_fn(filters=flt, first=MAX_PER_ENTITY)

def dump_author(author_id: str, author_name: str):
    types = {
        "indicators":     client.indicator.list,
        "reports":        client.report.list,
        "threat_actors":  client.threat_actor.list,
        "malware":        client.malware.list,
        "tools":          client.tool.list,
        "vulnerabilities":client.vulnerability.list,
        "attack_patterns":client.attack_pattern.list,
    }

    author_data = {}
    for label, fn in types.items():
        results = list_with_creator(fn, author_id)
        print(f"{author_name:<20} {label:<15} {len(results):>6} items")
        author_data[label] = results

    out_file = os.path.join(OUTPUT_DIR, f"{author_name.replace(' ', '_')}.json")
    with open(out_file, "w") as f:
        json.dump(author_data, f, indent=2)
    print(f"saved → {out_file}\n")

# ----------------------------------------------------------------------------- #
# main
# ----------------------------------------------------------------------------- #
if __name__ == "__main__":
    creators = get_all_creators()
    for creator_id, name in creators.items():
        dump_author(creator_id, name)
