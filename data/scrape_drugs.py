import json
import os
import time
import sys
import requests

API_BASE = "https://api.fda.gov"
ENDPOINT = "/drug/ndc.json"
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "drug_names.json")
REQUEST_DELAY = 0.5
API_KEY = os.getenv("OPENFDA_API_KEY", "")


def fetch_drug_names():
    all_names = set()
    skip = 0
    limit = 1000

    while True:
        params = {
            "search": "_exists_:generic_name",
            "limit": limit,
            "skip": skip,
        }
        if API_KEY:
            params["api_key"] = API_KEY

        resp = None
        for attempt in range(3):
            try:
                resp = requests.get(API_BASE + ENDPOINT, params=params, timeout=60)
                break
            except (requests.ConnectionError, requests.Timeout) as e:
                if attempt == 2:
                    print(f"  Connection failed at skip={skip}, saving collected names.")
                    return sorted(all_names)
                print(f"  Retry {attempt+1}/3 at skip={skip}...")
                time.sleep(2 * (attempt + 1))
        if resp is None:
            return sorted(all_names)
        if resp.status_code == 400:
            print(f"  Pagination limit reached at skip={skip}. Collected {len(all_names)} names.")
            break
        resp.raise_for_status()
        data = resp.json()

        results = data.get("results", [])
        if not results:
            break

        for r in results:
            name = r.get("generic_name", "")
            if name and len(name) > 1:
                all_names.add(name.strip())

        total = data.get("meta", {}).get("results", {}).get("total", 0)
        skip += limit
        print(f"  {min(skip, total)}/{total} records  |  unique names: {len(all_names)}")

        if skip >= total:
            break

        time.sleep(REQUEST_DELAY)

    return sorted(all_names)


def save_to_json(drug_names, filepath=OUTPUT_FILE):
    data = [{"name": name} for name in drug_names]
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"\nSaved {len(data)} drug names to {filepath}")


if __name__ == "__main__":
    print("=" * 50)
    print("Fetching drug names from OpenFDA API...")
    print("=" * 50)

    drug_names = fetch_drug_names()
    if not drug_names:
        print("ERROR: No drugs found. Something went wrong.")
        sys.exit(1)

    save_to_json(drug_names)

    if "--seed" in sys.argv:
        print("\nSeeding to MongoDB...")
        sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
        from seed_data import seed_drugs_from_json
        seed_drugs_from_json(OUTPUT_FILE)

    print(f"\nDone! Total unique drugs: {len(drug_names)}")