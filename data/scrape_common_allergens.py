import json
import os
import requests
import re

WIKI_URL = "https://en.wikipedia.org/w/api.php"
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "common_allergens.json")


HEADERS = {"User-Agent": "CDSS-MedicalApp/1.0 (educational project; contact@example.com)"}


def fetch_wikipedia_sections():
    params = {
        "action": "parse",
        "page": "List_of_allergens",
        "prop": "sections|text",
        "format": "json",
        "section": 0,
    }
    resp = requests.get(WIKI_URL, params=params, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    # Get the text of each section by fetching section by section
    sections_data = data.get("parse", {}).get("sections", [])
    # We'll fetch relevant sections
    relevant_titles = [
        "Plant", "Animal", "Small_organic_molecules", "Small_inorganic_molecules"
    ]

    allergens = []
    seen = set()

    for section in sections_data:
        title = section.get("line", "")
        if title not in relevant_titles:
            continue

        sec_index = section.get("index")
        sec_params = {
            "action": "parse",
            "page": "List_of_allergens",
            "prop": "text",
            "format": "json",
            "section": sec_index,
        }
        sec_resp = requests.get(WIKI_URL, params=sec_params, headers=HEADERS, timeout=30)
        sec_resp.raise_for_status()
        sec_data = sec_resp.json()
        text = sec_data.get("parse", {}).get("text", {}).get("*", "")

        # Extract <li> items and <h3>/<h4> headings which indicate allergen names
        # Look for headings as they indicate main allergen categories
        headings = re.findall(r'<h[34][^>]*><span[^>]*id="([^"]+)"', text)
        for h in headings:
            name = h.replace("_", " ").replace(".28", "(").replace(".29", ")").replace(".2C", ",")
            name = re.sub(r'\([^)]*\)', '', name).strip()
            if name and name not in seen and len(name) > 1:
                # Filter out generic/technical names
                if name.lower() not in ["edit", "see also", "references", "further reading", "notes"]:
                    from_category = title.replace("_", " ")
                    allergens.append({
                        "allergen": name,
                        "category": from_category,
                        "source": "Wikipedia",
                    })
                    seen.add(name)

        # Also extract list items with strong/bold tags (often contain allergen names)
        lis = re.findall(r'<li>(.*?)</li>', text, re.DOTALL)
        for li in lis:
            # Look for main link text
            links = re.findall(r'<a[^>]*>([^<]+)</a>', li)
            for link in links:
                link = link.strip()
                if link and len(link) > 2 and link not in seen:
                    # Skip non-allergen entries
                    skip_words = ["edit", "main article", "see also", "routes",
                                   "symptoms", "chemical nature", "this section"]
                    if not any(s in link.lower() for s in skip_words) and not link.startswith("["):
                        from_category = title.replace("_", " ")
                        allergens.append({
                            "allergen": link,
                            "category": from_category,
                            "source": "Wikipedia",
                        })
                        seen.add(link)

    return allergens


def compile_allergens():
    print("Fetching allergen data from Wikipedia...")

    try:
        wiki_allergens = fetch_wikipedia_sections()
        print(f"Found {len(wiki_allergens)} allergens from Wikipedia")
    except Exception as e:
        print(f"Wikipedia fetch failed: {e}")
        wiki_allergens = []

    # Hardcoded base list of common allergens (as fallback/ supplement)
    base_allergens = [
        # Food
        {"allergen": "Peanuts", "category": "Food", "source": "Clinical"},
        {"allergen": "Tree Nuts", "category": "Food", "source": "Clinical"},
        {"allergen": "Almonds", "category": "Food", "source": "Clinical"},
        {"allergen": "Walnuts", "category": "Food", "source": "Clinical"},
        {"allergen": "Cashews", "category": "Food", "source": "Clinical"},
        {"allergen": "Pecans", "category": "Food", "source": "Clinical"},
        {"allergen": "Brazil Nuts", "category": "Food", "source": "Clinical"},
        {"allergen": "Pistachios", "category": "Food", "source": "Clinical"},
        {"allergen": "Macadamia Nuts", "category": "Food", "source": "Clinical"},
        {"allergen": "Milk", "category": "Food", "source": "Clinical"},
        {"allergen": "Eggs", "category": "Food", "source": "Clinical"},
        {"allergen": "Soy", "category": "Food", "source": "Clinical"},
        {"allergen": "Wheat", "category": "Food", "source": "Clinical"},
        {"allergen": "Fish", "category": "Food", "source": "Clinical"},
        {"allergen": "Shellfish", "category": "Food", "source": "Clinical"},
        {"allergen": "Crustaceans", "category": "Food", "source": "Clinical"},
        {"allergen": "Mollusks", "category": "Food", "source": "Clinical"},
        {"allergen": "Sesame", "category": "Food", "source": "Clinical"},
        {"allergen": "Mustard", "category": "Food", "source": "Clinical"},
        {"allergen": "Celery", "category": "Food", "source": "Clinical"},
        {"allergen": "Lupin", "category": "Food", "source": "Clinical"},
        {"allergen": "Sulfites", "category": "Food", "source": "Clinical"},
        {"allergen": "Buckwheat", "category": "Food", "source": "Clinical"},
        {"allergen": "Corn", "category": "Food", "source": "Clinical"},
        {"allergen": "Garlic", "category": "Food", "source": "Clinical"},
        {"allergen": "Rice", "category": "Food", "source": "Clinical"},
        {"allergen": "Oats", "category": "Food", "source": "Clinical"},
        {"allergen": "Strawberries", "category": "Food", "source": "Clinical"},
        {"allergen": "Banana", "category": "Food", "source": "Clinical"},
        {"allergen": "Kiwi", "category": "Food", "source": "Clinical"},
        {"allergen": "Avocado", "category": "Food", "source": "Clinical"},
        {"allergen": "Mango", "category": "Food", "source": "Clinical"},
        {"allergen": "Tomato", "category": "Food", "source": "Clinical"},
        {"allergen": "Red Meat", "category": "Food", "source": "Clinical"},
        {"allergen": "Poultry", "category": "Food", "source": "Clinical"},
        {"allergen": "Pork", "category": "Food", "source": "Clinical"},
        {"allergen": "Egg White", "category": "Food", "source": "Clinical"},
        {"allergen": "Egg Yolk", "category": "Food", "source": "Clinical"},

        # Environmental
        {"allergen": "Pollen", "category": "Environmental", "source": "Clinical"},
        {"allergen": "Grass Pollen", "category": "Environmental", "source": "Clinical"},
        {"allergen": "Tree Pollen", "category": "Environmental", "source": "Clinical"},
        {"allergen": "Ragweed Pollen", "category": "Environmental", "source": "Clinical"},
        {"allergen": "Dust Mites", "category": "Environmental", "source": "Clinical"},
        {"allergen": "Mold", "category": "Environmental", "source": "Clinical"},
        {"allergen": "Pet Dander", "category": "Environmental", "source": "Clinical"},
        {"allergen": "Cat Dander", "category": "Environmental", "source": "Clinical"},
        {"allergen": "Dog Dander", "category": "Environmental", "source": "Clinical"},
        {"allergen": "Cockroach", "category": "Environmental", "source": "Clinical"},
        {"allergen": "Latex", "category": "Environmental", "source": "Clinical"},

        # Insect
        {"allergen": "Bee Stings", "category": "Insect", "source": "Clinical"},
        {"allergen": "Wasp Stings", "category": "Insect", "source": "Clinical"},
        {"allergen": "Mosquito Bites", "category": "Insect", "source": "Clinical"},
        {"allergen": "Fire Ants", "category": "Insect", "source": "Clinical"},

        # Chemical
        {"allergen": "Nickel", "category": "Chemical", "source": "Clinical"},
        {"allergen": "Gold", "category": "Chemical", "source": "Clinical"},
        {"allergen": "Fragrance", "category": "Chemical", "source": "Clinical"},
        {"allergen": "Formaldehyde", "category": "Chemical", "source": "Clinical"},
        {"allergen": "Tartrazine", "category": "Chemical", "source": "Clinical"},
        {"allergen": "Paraphenylenediamine", "category": "Chemical", "source": "Clinical"},
        {"allergen": "Sulfates", "category": "Chemical", "source": "Clinical"},
        {"allergen": "Dimethylaminopropylamine", "category": "Chemical", "source": "Clinical"},

        # Drug classes (overlap with drug_allergens, added here for UI completeness)
        {"allergen": "Penicillin", "category": "Drug Class", "source": "Clinical"},
        {"allergen": "Cephalosporins", "category": "Drug Class", "source": "Clinical"},
        {"allergen": "Sulfonamides", "category": "Drug Class", "source": "Clinical"},
        {"allergen": "NSAIDs", "category": "Drug Class", "source": "Clinical"},
        {"allergen": "Opioids", "category": "Drug Class", "source": "Clinical"},
        {"allergen": "Statins", "category": "Drug Class", "source": "Clinical"},
        {"allergen": "ACE Inhibitors", "category": "Drug Class", "source": "Clinical"},
        {"allergen": "Local Anesthetics", "category": "Drug Class", "source": "Clinical"},
        {"allergen": "Radiocontrast Media", "category": "Drug Class", "source": "Clinical"},
    ]

    seen_names = set()
    combined = []

    # Wikipedia first
    for a in wiki_allergens:
        name = a["allergen"].strip()
        if name and name.lower() not in seen_names:
            combined.append(a)
            seen_names.add(name.lower())

    # Then base list (skip duplicates)
    for a in base_allergens:
        name = a["allergen"].strip()
        if name.lower() not in seen_names:
            combined.append(a)
            seen_names.add(name.lower())

    combined.sort(key=lambda x: (x["category"], x["allergen"]))
    return combined


def save_to_json(allergens, filepath=OUTPUT_FILE):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(allergens, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(allergens)} common allergens to {filepath}")


if __name__ == "__main__":
    print("=" * 50)
    print("Fetching common allergens from Wikipedia...")
    print("=" * 50)

    allergens = compile_allergens()
    save_to_json(allergens)
    print("Done!")
