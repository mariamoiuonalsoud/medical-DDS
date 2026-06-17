import streamlit as st
from services.patient_service import get_all_patients, get_all_drugs
from services.validation_service import validate_prescription
from services.knowledge_service import search_knowledge
from services.llm_service import generate_clinical_brief
from models.schemas import Severity


def _reset_pipeline():
    st.session_state.validation_result = None
    st.session_state.knowledge_result = None
    st.session_state.brief_result = None
    st.session_state.pipeline_done = False


def render_validation():
    st.title("Prescription Validation")

    patients = get_all_patients()
    if not patients:
        st.info("No Patients Found — Add a patient first.")
        return

    all_drugs = get_all_drugs()
    if not all_drugs:
        st.warning("No drugs found in database. Run `seed_data.py` first.")
        st.stop()

    if "validation_result" not in st.session_state:
        _reset_pipeline()

    patient_options = {f"{p['name']} ({p.get('_id', '?')})": p for p in patients}

    with st.container():
        st.subheader("Select Patient & Drug")

        col1, col2 = st.columns(2)
        with col1:
            selected_label = st.selectbox(
                "Patient",
                options=list(patient_options.keys()),
                key="validation_patient",
                on_change=_reset_pipeline,
            )
            patient = patient_options[selected_label]

        with col2:
            proposed_drug = st.selectbox(
                "Medication",
                options=all_drugs,
                key="validation_drug",
                on_change=_reset_pipeline,
            )


    run_pipeline = st.button(
        "Check Prescription",
        type="primary",
        use_container_width=True,
        disabled=not proposed_drug,
    )

    if run_pipeline:
        _reset_pipeline()
        progress_bar = st.progress(0, text="Checking Interactions...")

        result = validate_prescription(patient, proposed_drug)
        st.session_state.validation_result = result
        progress_bar.progress(33, text="Searching Knowledge...")

        knowledge = search_knowledge(proposed_drug, top_k=3)
        st.session_state.knowledge_result = knowledge
        progress_bar.progress(66, text="Generating Clinical Summary...")

        brief = generate_clinical_brief(
            patient_name=patient["name"],
            proposed_drug=proposed_drug,
            alerts=result.alerts,
        )
        st.session_state.brief_result = brief
        progress_bar.progress(100, text="Prescription check complete")

        st.session_state.pipeline_done = True
        st.rerun()

    if st.session_state.pipeline_done and st.session_state.validation_result is not None:
        result = st.session_state.validation_result
        knowledge = st.session_state.knowledge_result
        brief = st.session_state.brief_result

        drug = proposed_drug
        pat = patient["name"]

        st.divider()
        st.subheader("Drug Interaction Results")

        if result.safe:
            st.success(f"**Safe to Prescribe** — {drug} appears safe for {pat}. No conflicts found.")
        else:
            for alert in result.alerts:
                sev = alert.severity
                conflict_type = alert.conflict_type.value.replace("_", " ").title()
                sev_label = alert.severity.value if hasattr(alert.severity, 'value') else str(alert.severity)
                msg = f"**{sev_label}: {conflict_type}** — {alert.drug} ↔ {alert.conflict_with}\n\n{alert.reason}\n\n{alert.source}"

                if sev in (Severity.contraindicated, Severity.high):
                    st.error(msg)
                elif sev == Severity.moderate:
                    st.warning(msg)
                else:
                    st.info(msg)

        if knowledge:
            st.divider()
            st.subheader("Related Medical Knowledge")
            for entry in knowledge:
                uses_str = ", ".join(entry.uses) if hasattr(entry, 'uses') and entry.uses else ""
                with st.expander(f"{entry.drug} — {entry.score:.2f}"):
                    st.write(entry.description)
                    if uses_str:
                        st.caption(f"Uses: {uses_str}")

        if brief:
            st.divider()
            st.subheader("Clinical Summary")
            is_live = not brief.model_used.startswith("Template")
            st.caption(f"Model: {brief.model_used}")

            st.write("**Summary**")
            st.write(brief.summary)

            st.write("**Recommendation**")
            st.write(brief.recommendation)

            if brief.alternatives:
                st.write("**Considered Alternatives**")
                for alt in brief.alternatives:
                    st.write(f"- {alt}")

            st.caption(brief.disclaimer)

        from config.database import validations_db
        validations_db.insert_one({
            "patient_id": patient.get("_id"),
            "patient_name": patient["name"],
            "proposed_drug": proposed_drug,
            "safe": result.safe,
            "alert_count": len(result.alerts),
            "timestamp": __import__("datetime").datetime.now(),
        })
