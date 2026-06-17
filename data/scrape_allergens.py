import json
import os
import time
import requests
import re

API_BASE = "https://api.fda.gov/drug/label.json"
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "allergens_extended.json")
REQUEST_DELAY = 0.5

ALLERGEN_CLASS_KEYWORDS = [
    "penicillin", "sulfa", "cephalosporin", "aspirin", "nsaid",
    "opioid", "codeine", "statin", "ace inhibitor",
]


def normalize_class(text):
    text = text.lower().strip()
    class_map = {
        "penicillin": "Penicillin",
        "sulfa": "Sulfa", "sulfonamide": "Sulfa",
        "cephalosporin": "Cephalosporin",
        "aspirin": "Salicylate/NSAID",
        "nsaid": "Salicylate/NSAID", "salicylate": "Salicylate/NSAID",
        "opioid": "Opioid",
        "codeine": "Opioid",
        "statin": "Statin",
        "ace inhibitor": "ACE Inhibitor",
    }
    for key, val in class_map.items():
        if key in text:
            return val
    return text.title()


def search_labels(keyword, max_results=50):
    results = []
    skip = 0
    page = 0

    while len(results) < max_results:
        page += 1
        params = {
            "search": f"contraindications:{keyword}",
            "limit": 500,
            "skip": skip,
        }
        try:
            resp = requests.get(API_BASE, params=params, timeout=60)
            resp.raise_for_status()
        except requests.RequestException as e:
            print(f"    Request failed: {e}")
            break

        data = resp.json()
        batch = data.get("results", [])
        if not batch:
            break

        results.extend(batch)
        total = data.get("meta", {}).get("results", {}).get("total", 0)
        skip += 500
        print(f"    page {page}: skip={skip} / {total} | collected={len(results)}")

        if skip >= total:
            break
        time.sleep(REQUEST_DELAY)

    return results[:max_results]


def fetch_allergens():
    known_pairs = {}

    for keyword in ALLERGEN_CLASS_KEYWORDS:
        print(f"\nSearching: '{keyword}'...")
        sys.stdout.flush()
        results = search_labels(keyword, max_results=50)

        for r in results:
            ofda = r.get("openfda", {})
            drug = (ofda.get("generic_name", [""])[0] or
                    ofda.get("brand_name", [""])[0] or
                    ofda.get("substance_name", [""])[0] or "").strip()
            if not drug:
                continue

            text = " ".join(r.get("contraindications", []) or [])
            for kw in ALLERGEN_CLASS_KEYWORDS:
                if re.search(rf"\b{re.escape(kw)}\b", text.lower()):
                    cls = normalize_class(kw)
                    known_pairs[(drug.lower(), cls)] = {"drug": drug, "allergen_class": cls}

        print(f"  Found {len(results)} labels, {sum(1 for p in known_pairs.values() if True)} unique drug-class pairs so far")

    class_drugs = {}
    for pair in known_pairs.values():
        cls = pair["allergen_class"]
        class_drugs.setdefault(cls, set()).add(pair["drug"])

    allergens = []
    for cls in sorted(class_drugs):
        drugs = sorted(class_drugs[cls])
        for drug in drugs:
            cross = [d for d in drugs if d.lower() != drug.lower()]
            allergens.append({
                "drug": drug,
                "allergen_class": cls,
                "cross_reactives": cross,
            })

    print(f"\nTotal entries: {len(allergens)}")
    print(f"Classes: {sorted(class_drugs.keys())}")
    for cls, drugs in sorted(class_drugs.items()):
        print(f"  {cls}: {len(drugs)} drugs")
    return allergens


def save_to_json(allergens, filepath=OUTPUT_FILE):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(allergens, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(allergens)} entries to {filepath}")


if __name__ == "__main__":
    import sys
    print("=" * 50)
    print("Fetching allergen data from OpenFDA drug labels...")
    print("=" * 50)

    allergens = fetch_allergens()
    if not allergens:
        print("ERROR: No data found.")
        exit(1)

    save_to_json(allergens)
    print("Done!")
