from pymongo import MongoClient
import pymongo
import streamlit as st



@st.cache_resource  # Cache the database connection to avoid reconnecting on every run
def get_db_connection(): ## MongoDB connection setup
    client = MongoClient("mongodb://localhost:27017/")
    db = client["medical_DDS"]
    return db

#! database connection and collection setup

db = get_db_connection()
patients_db = db["patients"]  # for patients data
medications_db = db["medications"] # for medications data
drugs_db = db["drugs"] # for drugs data
interactions_db = db["drug_interactions"] # for drugs interactions data
allergens_db = db["drug_allergens"] # for drug allergens data
condition_rules_db = db["condition_rules"] 
conditions_db = db["chronic_conditions"]
common_allergens_db = db["common_allergens"]
knowledge_db = db['knowledge_base']
validations_db = db['validations']
counters_db = db["counters"] # for maintaining auto-incrementing IDs



#! for patient's ID sequance

def get_next_sequence(seq_name): 
    counter = counters_db.find_one_and_update(
        {"_id": seq_name},
        {"$inc": {"seq": 1}},
        upsert=True,
        return_document = pymongo.ReturnDocument.AFTER
    )
    return counter["seq"]