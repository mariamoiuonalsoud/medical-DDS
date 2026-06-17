import streamlit as st
import pandas as pd
import os
from models.schemas import ClinicalBrief

CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "medical_knowledge.csv")

@st.cache_resource
def load_fallback_data():
    """Load the CSV for safe alternative lookups (no LLM required)."""
    if os.path.exists(CSV_PATH):
        return pd.read_csv(CSV_PATH)
    return None

def _lookup_alternative(wrong_drug):
    df = load_fallback_data()
    if df is not None:
        match = df[df["Drug_Name"].str.lower() == wrong_drug.lower()]
        if not match.empty:
            return match.iloc[0]["Safe_Alternatives"], match.iloc[0]["Dosage_Guidance"]
    return "Acetaminophen (Paracetamol)", "Take 500mg to 1000mg every 4 to 6 hours as needed. Maximum 4g per day."


def _generate_template_brief(patient_name, proposed_drug, alerts, alternative, dosage):
    """Deterministic fallback when LLM is unavailable."""
    severity_text = ", ".join(f"{a.severity.value}" for a in alerts)
    reasons = "\n".join(f"- {a.reason}" for a in alerts)
    return ClinicalBrief(
        summary=f"Proposed drug '{proposed_drug}' triggered {len(alerts)} alert(s) "
                f"({severity_text}) for patient {patient_name}.\n\nReasons:\n{reasons}",
        recommendation=f"Consider switching to {alternative} as a safer alternative. {dosage}",
        alternatives=[alternative],
        disclaimer="This is a deterministic clinical brief. No AI model was used.",
        generated_at="",
        model_used="template-fallback"
    )


def generate_clinical_brief(patient_name, proposed_drug, alerts, knowledge_entries=None):
    """
    Generate a clinical brief for a proposed prescription.
    Falls back to deterministic template if LLM is not available.
    """
    alternative, dosage = _lookup_alternative(proposed_drug)
    return _generate_template_brief(patient_name, proposed_drug, alerts, alternative, dosage)


# ─── LLM Mode (requires BioMistral-7B) ──────────────────────────────

@st.cache_resource
def _load_llm():
    """Lazy-load BioMistral-7B (requires GPU). Returns None if unavailable."""
    try:
        import torch
        from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
        model_id = "BioMistral/BioMistral-7B"
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16
        )
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        model = AutoModelForCausalLM.from_pretrained(
            model_id, quantization_config=bnb_config, device_map="auto"
        )
        return tokenizer, model, torch.device("cuda" if torch.cuda.is_available() else "cpu")
    except Exception as e:
        st.warning(f"Could not load LLM: {e}. Using template fallback.")
        return None


def generate_llm_brief(patient_name, patient_data, proposed_drug, alerts):
    llm = _load_llm()
    if llm is None:
        return generate_clinical_brief(patient_name, proposed_drug, alerts)

    tokenizer, model, device = llm
    alternative, dosage = _lookup_alternative(proposed_drug)
    conflict_details = "; ".join(f"{a.conflict_type.value}: {a.reason}" for a in alerts)

    prompt = f"""You are an expert Clinical AI Advisor. Analyze this hospital safety case.

[PATIENT]: {patient_data}
[CONTRAINDICATION]: The physician tried to prescribe '{proposed_drug}'.
Conflicts: {conflict_details}
[ALTERNATIVE]: {alternative}
[DOSAGE]: {dosage}

Task: Write a structured Clinical Brief:
Section 1: Biomolecular reason why {proposed_drug} is contraindicated.
Section 2: Recommended alternative: {alternative}.
Section 3: Dosage guidance: {dosage}.

Clinical Brief:"""

    import torch
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    with torch.no_grad():
        outputs = model.generate(
            **inputs, max_new_tokens=250, temperature=0.1, do_sample=True
        )

    result = tokenizer.decode(outputs[0], skip_special_tokens=True)
    report = result.split("Clinical Brief:")[-1].strip()

    return ClinicalBrief(
        summary=report,
        recommendation=f"Switch to {alternative}. {dosage}",
        alternatives=[alternative],
        disclaimer="AI-generated. Verify with clinical guidelines.",
        generated_at="",
        model_used="BioMistral-7B"
    )