import json
import os
import time
import requests

API_BASE = "https://clinicaltables.nlm.nih.gov/api/icd10cm/v3/search"
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "icd10_conditions.json")
REQUEST_DELAY = 0.3

CHRONIC_SEARCH_TERMS = [
    "diabetes", "hypertension", "asthma", "COPD", "chronic",
    "heart failure", "arthritis", "thyroid", "kidney disease",
    "cancer", "epilepsy", "osteoporosis", "Parkinson",
    "dementia", "depression", "anemia", "hepatitis", "cirrhosis",
    "psoriasis", "lupus", "multiple sclerosis", "Crohn",
    "colitis", "glaucoma", "cataract", "gout", "obesity",
    "sleep apnea", "HIV", "hepatitis B", "hepatitis C",
    "chronic pain", "fibromyalgia", "migraine",
    "hyperlipidemia", "coronary artery disease",
    "peripheral vascular disease", "atrial fibrillation",
    "stroke", "Alzheimer", "chronic bronchitis",
    "emphysema", "bronchiectasis", "pulmonary fibrosis",
    "chronic liver disease", "pancreatitis", "diverticulitis",
    "irritable bowel", "celiac", "thyroiditis",
    "Addison", "Cushing", "hyperparathyroidism",
    "hypoparathyroidism", "pituitary", "menopause",
    "endometriosis", "PCOS", "BPH", "incontinence",
    "chronic sinusitis", "allergic rhinitis",
    "dermatitis", "eczema", "rosacea", "vitiligo",
    "scleroderma", "Sjogren", "sarcoidosis",
    "amyloidosis", "hemophilia", "thalassemia",
    "sickle cell", "osteomyelitis", "Paget disease",
    "carpal tunnel", "tendonitis", "bursitis",
    "gastroesophageal reflux", "peptic ulcer",
    "gallbladder disease", "cholecystitis",
]

CHRONIC_CHAPTER_FILTERS = [
    "E0", "E1", "E2", "E7", "E8",
    "F0", "F1", "F2", "F3", "F4", "F5",
    "G0", "G1", "G2", "G3", "G4",
    "I0", "I1", "I2", "I5", "I6", "I7",
    "J4", "J6",
    "K5", "K7", "K8",
    "L4", "L8",
    "M0", "M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8",
    "N0", "N1", "N2", "N3", "N4", "N8",
    "R1", "R5",
]


def search_icd10(terms, max_list=500):
    all_results = []
    offset = 0
    count = 500

    while True:
        params = {
            "sf": "code,name",
            "terms": terms,
            "count": count,
            "offset": offset,
        }

        try:
            resp = requests.get(API_BASE, params=params, timeout=60)
            resp.raise_for_status()
        except requests.RequestException as e:
            print(f"  Request failed at offset={offset}: {e}")
            break

        data = resp.json()
        total = data[0]
        codes = data[1]
        names = data[3] if len(data) > 3 else []

        if not codes:
            break

        for i, code in enumerate(codes):
            name = names[i][1] if names and len(names) > i and len(names[i]) > 1 else ""
            all_results.append({"code": code, "name": name})

        offset += count
        print(f"  {terms[:20]:20s} | offset={offset:4d} / total={total} | collected={len(all_results)}")

        if offset >= min(total, 7500):
            break

        time.sleep(REQUEST_DELAY)

    return all_results


def fetch_all_conditions():
    seen_codes = {}
    by_search = {}

    for term in CHRONIC_SEARCH_TERMS:
        print(f"\nSearching: '{term}'")
        results = search_icd10(term)
        by_search[term] = len(results)
        for r in results:
            if r["code"] not in seen_codes:
                seen_codes[r["code"]] = r["name"]

    for prefix in CHRONIC_CHAPTER_FILTERS:
        print(f"\nChapter filter: '{prefix}'")
        results = search_icd10(prefix)
        by_search[f"prefix_{prefix}"] = len(results)
        for r in results:
            if r["code"] not in seen_codes:
                seen_codes[r["code"]] = r["name"]

    print(f"\n{'='*50}")
    print(f"Total unique conditions collected: {len(seen_codes)}")
    print(f"Search breakdown: {json.dumps(by_search, indent=2)[:500]}")

    conditions = sorted(
        [{"code": code, "name": name} for code, name in seen_codes.items()],
        key=lambda x: x["code"],
    )
    return conditions


def save_to_json(conditions, filepath=OUTPUT_FILE):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(conditions, f, indent=2, ensure_ascii=False)
    print(f"\nSaved {len(conditions)} conditions to {filepath}")


if __name__ == "__main__":
    print("=" * 50)
    print("Fetching ICD-10-CM chronic conditions...")
    print("=" * 50)

    conditions = fetch_all_conditions()
    if not conditions:
        print("ERROR: No conditions found.")
        exit(1)

    save_to_json(conditions)
    print("Done!")
