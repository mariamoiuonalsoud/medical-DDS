from config.database import patients_db, medications_db, get_next_sequence, allergens_db, drugs_db, conditions_db, common_allergens_db

def add_patient(name, age, gender, chronic_conditions,
                current_medications = None, allergies = None, medical_history = ""):
    if name:
        new_patient = {
            "_id": f"P{get_next_sequence('patient_id')}",
            "name": name,
            "age": age,
            "gender": gender,
            "chronic_conditions": chronic_conditions or [],
            "current_medications": current_medications or [],
            "allergies" : allergies or [],
            "medical_history": medical_history
        }
        patients_db.insert_one(new_patient)
        return new_patient
    return None

def get_all_patients():
    return list(patients_db.find({}))

def get_patient_by_id(patient_id):
    return patients_db.find_one({"_id": patient_id})

def add_medication_to_patient(patient_id, medication_data):
    patients_db.update_one(
        {"_id": patient_id},
        {"$push": {"current_medications": medication_data}}
    )

def add_allergy_to_patient(patient_id, allergy_date):
    patients_db.update_one(
        {"_id": patient_id},
        {"$push": {"allergies": allergy_date}}
    )

def get_all_drugs():
    drugs = list(drugs_db.find({}, {"_id": 0, "name":1}))
    return [d["name"] for d in drugs]

def get_all_allergens():
    allergens = list(allergens_db.find({}, {'_id': 0, "allergen_class":1}))
    return [a["allergen_class"] for a in allergens]

def get_all_allergen_drugs():
    drugs = list(allergens_db.find({}, {'_id': 0, "drug": 1}))
    return sorted(set(d["drug"] for d in drugs))

def get_all_conditions():
    conditions = list(conditions_db.find({}, {"_id": 0, "code": 1, "name": 1}))
    return [c["name"] for c in conditions]

def get_all_common_allergens():
    items = list(common_allergens_db.find({}, {"_id": 0, "allergen": 1}))
    return sorted(set(a["allergen"] for a in items))
