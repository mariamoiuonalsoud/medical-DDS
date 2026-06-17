from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from enum import Enum

class ConflictType(str, Enum):
    drug_drug = "drug_drug"
    drug_allergy = "drug_allergy"
    condition_warning = "condition_warning"

class Severity(str, Enum):
    contraindicated = "Contraindicated"
    high = "High Risk"
    moderate = "Moderate Risk"
    low = "Low Risk"

class Medication(BaseModel):
    drug_name: str
    dosage: str = ""
    frequency: str = "" 
    start_date: Optional[date] = None
    status: str = "active"

class Allergy(BaseModel):
    substance: str
    reaction: str = ""
    severity: str = "Moderate"

class Patient(BaseModel):
    patient_id: str
    name: str
    age: int
    gender: str
    chronic_conditions: list[str] = []
    allergies: list[Allergy] = []
    current_medications: list[str] = []
    medical_history: str = ''

class DrugInfo(BaseModel):
    name: str
    generic_name: str = ''
    therapeutic_class: str
    mechaism: str = ""
    contraindications: list[str] = []
    common_dosage: str = ''
    side_effects: list[str] = []

class DrugAllergen(BaseModel):
    drug: str
    allergen_class: str
    cross_reactives: list[str] = []

class InteractionAlert(BaseModel):
    conflict_type: ConflictType
    severity: Severity
    reason: str
    source: str
    drug: str
    conflict_with: str

class ValidationResult(BaseModel):
    patient_id: str
    proposed_drug: str
    safe: bool
    alerts: list[InteractionAlert] = []

class InteractionRule(BaseModel):
    drug:str
    interacts_with: str
    type: ConflictType
    severity: Severity
    reason: str

class KnowledgeEntry(BaseModel):
    drug: str
    description: str
    uses: list[str]= [] 
    score: float = 0.0

class ClinicalBrief(BaseModel):
    summary: str
    recommendation: str
    alternatives: list[str] = []
    disclaimer: str = ""
    generated_at: str = ''
    model_used: str = ''

class DashboardStats(BaseModel):
    total_patients: int = 0
    total_drugs: int = 0
    total_interaction_rules: int = 0
    total_knowledge_entries: int = 0
    recent_validations: int = 0

