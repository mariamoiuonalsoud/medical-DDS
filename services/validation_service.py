from config.database import interactions_db, condition_rules_db, allergens_db
from models.schemas import ValidationResult, InteractionAlert, ConflictType, Severity

def validate_prescription(patient, proposed_drug):
    """
    Check a proposed drug against a patient's current medications,
    allergies, and chronic conditions.
    patient: dict from patients_db
    proposed_drug: str
    Returns ValidationResult
    """
    
    if not proposed_drug:
        return ValidationResult(
            patient_id=patient.get("_id", ""),
            proposed_drug="",
            safe=True,
            alerts=[]
        )
    alerts=[]
    proposed_lower = proposed_drug.strip().lower()

    # ─── 1. Drug-Drug Conflicts ──────────────────────────────────
    patient_meds = [m.lower() for m in patient.get("current_medications", [])]
    for rule in interactions_db.find({}):
        drug_a = rule["drug_a"].lower()
        drug_b = rule["drug_b"].lower()
        if drug_a == proposed_lower and drug_b in patient_meds:
            alerts.append(InteractionAlert(
                conflict_type=ConflictType.drug_drug,
                severity=_parse_severity(rule["severity"]),
                reason=rule.get("mechanism", ""),
                source="Interaction rule",
                drug=proposed_drug,
                conflict_with=rule["drug_b"]
            ))
        elif drug_b == proposed_lower and drug_a in patient_meds:
            alerts.append(InteractionAlert(
                conflict_type=ConflictType.drug_drug,
                severity=_parse_severity(rule["severity"]),
                reason=rule.get("mechanism", ""),
                source="Interaction rule",
                drug=proposed_drug,
                conflict_with=rule["drug_a"]
            ))

    # ─── 2. Drug-Allergy Conflicts ───────────────────────────────
    patient_allergies = [a.lower() for a in patient.get("allergies", [])]

    # 2a. Direct allergy check
    if proposed_lower in patient_allergies:
        alerts.append(InteractionAlert(
            conflict_type=ConflictType.drug_allergy,
            severity=Severity.contraindicated,
            reason=f"Patient has a documented allergy to {proposed_drug}",
            source="Allergy record",
            drug=proposed_drug,
            conflict_with=proposed_drug
        ))

    # 2b. Cross-reactivity check
    for allergen in allergens_db.find({}):
        if allergen["drug"].lower() == proposed_lower:
            allergen_class = allergen["allergen_class"].lower()
            for pa in patient_allergies:
                # Check if patient's allergy matches the allergen class
                if pa == allergen_class:
                    alerts.append(InteractionAlert(
                        conflict_type=ConflictType.drug_allergy,
                        severity=Severity.contraindicated,
                        reason=f"{proposed_drug} belongs to {allergen['allergen_class']} class — patient has documented {pa} allergy",
                        source="Allergen cross-reactivity",
                        drug=proposed_drug,
                        conflict_with=pa
                    ))
            # Check cross-reactives
            for cr in allergen.get("cross_reactives", []):
                if cr.lower() in patient_allergies:
                    alerts.append(InteractionAlert(
                        conflict_type=ConflictType.drug_allergy,
                        severity=Severity.moderate,
                        reason=f"{proposed_drug} ({allergen['allergen_class']}) may cross-react with {cr}",
                        source="Allergen cross-reactivity",
                        drug=proposed_drug,
                        conflict_with=cr
                    ))

    # ─── 3. Condition Warnings ───────────────────────────────────
    patient_conditions = [c.lower() for c in patient.get("chronic_conditions", [])]
    for rule in condition_rules_db.find({}):
        if rule["drug"].lower() == proposed_lower:
            condition = rule["interacts_with"].lower()
            for pc in patient_conditions:
                if condition in pc or pc in condition:
                    alerts.append(InteractionAlert(
                        conflict_type=ConflictType.condition_warning,
                        severity=_parse_severity(rule["severity"]),
                        reason=rule["reason"],
                        source="Condition warning rule",
                        drug=proposed_drug,
                        conflict_with=rule["interacts_with"]
                    ))

    return ValidationResult(
        patient_id=patient.get("_id", ""),
        proposed_drug=proposed_drug,
        safe=len(alerts) == 0,
        alerts=alerts
    )


def _parse_severity(s):
    s = s.strip()
    mapping = {
        "High": Severity.high,
        "High Risk": Severity.high,
        "Moderate": Severity.moderate,
        "Moderate Risk": Severity.moderate,
        "Low": Severity.low,
        "Low Risk": Severity.low,
        "Contraindicated": Severity.contraindicated,
    }
    return mapping.get(s, Severity.moderate)


def get_interaction_stats():
    total_drug_drug = interactions_db.count_documents({})
    total_condition = condition_rules_db.count_documents({})
    total_allergen = allergens_db.count_documents({})
    return {
        "total_interaction_rules": total_drug_drug + total_condition + total_allergen,
        "total_drug_drug": total_drug_drug,
        "total_condition_rules": total_condition,
        "total_allergen_rules": total_allergen,
    }