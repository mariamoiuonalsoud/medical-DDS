import streamlit as st
from config.database import patients_db, drugs_db, validations_db
from services.validation_service import get_interaction_stats
from services.knowledge_service import get_knowledge_stats


def render_dashboard():
    st.title("Clinical Decision Support System")
    st.markdown(
        "AI-Powered Drug Interaction Advisor — check prescriptions, "
        "validate drug interactions, and make informed clinical decisions."
    )
    ###? KRaw 1: Key Metrics
    total_patients = patients_db.count_documents({})
    total_validations = validations_db.count_documents({})
    flagged_count = validations_db.count_documents({"safe":False})
    safe_rate = (
        round((total_validations - flagged_count)/ total_validations * 100)
        if total_validations > 0 else 0
    )

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Patients", total_patients)
    with col2:
        st.metric("Flagged Prescriptions", flagged_count)
    with col3:
        st.metric("Total  Prescriptions Checked",total_validations)
    with col4:
        st.metric("Safe Rate", f"{safe_rate}%")

    st.divider()

    ###? Row 2: Patient Demo

    st.subheader("Patient Population Overview")
    all_patients = list(patients_db.find({}))

    col_left, col_right = st.columns(2)
    with col_left:
        age_groups = {"0-18":0, "19-35":0, "36-55":0, "56-70":0, "+71":0}
        for p in all_patients:
            age = p.get("age",0)
            if age <=18:
                age_groups['0-18'] += 1
            elif age <= 35:
                age_groups['19-35'] += 1
            elif age <= 55:
                age_groups['36-55'] += 1
            elif age <= 70:
                age_groups["56-70"] += 1
            else:
                age_groups["+71"] += 1
        st.markdown("**Age Distribution**")
        for label, count in age_groups.items():
            st.markdown(f"- {label}: {count}")
            if count > 0:
                st.progress(count / max(age_groups.values()))
    
    with col_right:
        condition_counter = {}
        for p in all_patients:
            for cnd in p.get("chronic_conditions",[]):
                condition_counter[cnd] = condition_counter.get(cnd, 0)+1
            if condition_counter:
                st.markdown("**Most Common Conditions")
                sorted_conditions = sorted(condition_counter.items(), key= lambda x: x[1], reverse= True)
                for cnd, cnt in sorted_conditions[:5]:
                    st.markdown(f'- {cnd}: {cnt}')
            else:
                st.info('No Chronic Conditions Recoreded.')
    st.divider()


    ###? Row 3: High-Risk Patients

    st.subheader("High-Risk Patients")
    from collections import Counter
    
    flagged_logs = validations_db.find({"safe": False})
    patient_counts = Counter(log["patient_name"] for log in flagged_logs)
    high_risk = patient_counts.most_common(5)
    if high_risk:
        for name, count in high_risk:
            st.warning(f"**{name}** — {count} flagged prescription(s)")
    else:
        st.success("No high-risk patients detected.")
    st.divider()

    ###? Row 4: Recent Activity
    st.subheader("Recent Validations")
    logs = list(validations_db.find().sort("timestamp", -1).limit(8))
    if logs:
        for log in logs:
            is_safe = log.get("safe", False)
            status = "Safe" if is_safe else f"{log.get('alert_count', 0)} alert(s)"
            if is_safe:
                st.success(f"**{log['patient_name']}** → {log['proposed_drug']} — {status}")
            else:
                st.error(f"**{log['patient_name']}** → {log['proposed_drug']} — {status}")
            st.caption(str(log.get("timestamp", "")))
    else:
        st.info("No validations performed yet.")
    st.divider()
    st.caption("Clinical Decision Support System")



'''
    col_left, col_right = st.columns(2)
    with col_left:
        st.subheader("Validations Performed")
        st.markdown(f"### {total_validations}")
        st.caption("Total prescription checks run in the system")

    with col_right:
        st.subheader("Recent Activity")
        logs = list(validations_db.find().sort("timestamp", -1).limit(8))
        if logs:
            for log in logs:
                is_safe = log.get("safe", False)
                status = "Safe" if is_safe else f"{log.get('alert_count', 0)} alert(s)"
                if is_safe:
                    st.success(f"**{log['patient_name']}** → {log['proposed_drug']} — {status}")
                else:
                    st.error(f"**{log['patient_name']}** → {log['proposed_drug']} — {status}")
                st.caption(str(log.get("timestamp", "")))
        else:
            st.info("No validations performed yet.")
'''
 
