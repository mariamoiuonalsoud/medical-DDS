from services.patient_service import add_patient, get_all_allergens, get_all_allergen_drugs, get_all_drugs, get_all_conditions, get_all_common_allergens
import streamlit as st
import datetime

FALLBACK_CONDITIONS = [
    "Diabetes", "Hypertension", "Asthma", "COPD",
    "Chronic Kidney Disease", "Heart Failure",
    "Hypothyroidism", "Hyperthyroidism", "Arthritis", "Cancer"
]

def get_conditions():
    db_conditions = get_all_conditions()
    return db_conditions if db_conditions else FALLBACK_CONDITIONS

def get_common_allergens():
    db_allergens = get_all_common_allergens()
    return db_allergens if db_allergens else COMMON_ALLERGENS

ALLERGENS_MAP = {
    "Penicillin": ["Amoxicillin", "Ampicillin", "Penicillin V"],
    "Sulfa": ["Sulfamethoxazole", "Furosemide", "Glipizide"],
    "Aspirin/NSAIDs": ["Aspirin", "Ibuprofen", "Naproxen", "Celecoxib"],
    "Codeine": ["Codeine", "Morphine", "Hydrocodone"],
    "ACE Inhibitors": ["Lisinopril", "Enalapril", "Ramipril"],
    "Statins": ["Atorvastatin", "Simvastatin", "Rosuvastatin"],
}

COMMON_ALLERGENS = [
    "Peanuts", "Tree Nuts", "Milk", "Eggs", "Soy", "Wheat",
    "Fish", "Shellfish", "Sesame", "Latex", "Bee Stings",
    "Pollen", "Dust Mites", "Mold", "Pet Dander",
    "Sulfites", "MSG", "Food Dye", "Cockroach",
    "Insect Stings", "Nickel", "Fragrance", "Poison Ivy",
]


def render_add_patient():
    st.title("Add New Patient")

    all_drugs = get_all_drugs()

    with st.form("add_patient_form", clear_on_submit=True):
        st.subheader("Patient Information")

        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            name = st.text_input(
                "Patient Name",
                placeholder="e.g. John Smith",
            )
        with col2:
            dob = st.date_input(
                "Date of Birth",
                min_value=datetime.date(1900, 1, 1),
                max_value=datetime.date.today(),
                value=datetime.date(2000, 1, 1),
            )
        with col3:
            gender = st.selectbox(
                "Gender",
                options=["Male", "Female"],
            )

        today = datetime.date.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

        st.subheader("Chronic Conditions")
        conditions_opts = get_conditions()
        chronic_conditions = st.multiselect(
            "Chronic Conditions",
            options=conditions_opts,
            placeholder="Select conditions...",
        )

        st.subheader("Current Medications")
        current_medications = st.multiselect(
            "Select Active Medications",
            options= all_drugs,
            placeholder="Select medications...",
        )

        st.subheader("Allergies")
        allergen_options = (
            list(ALLERGENS_MAP.keys())
            + get_all_allergens()
            + get_all_allergen_drugs()
            + get_common_allergens()
        )
        allergen_options = sorted(set(allergen_options))
        allergies = st.multiselect(
            "Select Allergies",
            options=allergen_options,
            placeholder="Select allergies...",
        )

        st.subheader("Medical History")
        medical_history = st.text_area(
            "Notes / Past Medical History",
            placeholder="Enter any relevant medical history, notes, or observations...",
        )

        submitted = st.form_submit_button("Add Patient", type="primary", use_container_width=True)

        if submitted:
            if name:
                add_patient(
                    name, age, gender, chronic_conditions,
                    current_medications, allergies, medical_history,
                )
                st.success(f"Patient Added Successfully — {name} has been registered in the system.")
            else:
                st.error("Required Field — Patient name is required.")
