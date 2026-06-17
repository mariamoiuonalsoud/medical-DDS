from services.patient_service import get_all_patients
import streamlit as st


def render_view_patients():
    st.title("Patient Records")

    patients = get_all_patients()

    if not patients:
        st.info("No Patients Found — Add a new patient to get started.")
        return

    if "selected_patient_id" not in st.session_state:
        st.session_state.selected_patient_id = patients[0].get("_id")

    search = st.text_input(
        "Search patients",
        placeholder="Type name or ID...",
    )

    filtered = patients
    if search:
        s = search.lower()
        filtered = [
            p for p in patients
            if s in p.get("name", "").lower() or s in str(p.get("_id", "")).lower()
        ]

    if filtered and st.session_state.selected_patient_id not in {p.get("_id") for p in filtered}:
        st.session_state.selected_patient_id = filtered[0].get("_id")

    col_list, col_detail = st.columns([1, 2])

    with col_list:
        st.markdown(f"**{len(filtered)} patient(s)**")
        for p in filtered:
            pid = p.get("_id", "?")
            pname = p.get("name", "?")
            selected = st.session_state.selected_patient_id == pid

            if selected:
                st.markdown(
                    f"<div style='background-color:#ff4b4b; border:1px solid #1a73e8; "
                    f"border-radius:5px; padding:8px 12px; margin-bottom:5px;'>"
                    f"<b>▸ {pname} — {pid}</b></div>",
                    unsafe_allow_html=True,
                )
            else:
                if st.button(f"  {pname} — {pid}", key=f"patient_{pid}", use_container_width=True):
                    st.session_state.selected_patient_id = pid
                    st.rerun()

    with col_detail:
        selected_patient = next(
            (p for p in filtered if p.get("_id") == st.session_state.selected_patient_id),
            None,
        )

        if selected_patient:
            st.subheader(selected_patient.get("name", "?"))
            st.caption(
                f"{selected_patient.get('_id', '?')}  ·  "
                f"{selected_patient.get('age', '?')} yrs  ·  "
                f"{selected_patient.get('gender', '?')}"
            )

            conds = selected_patient.get("chronic_conditions", [])
            meds = selected_patient.get("current_medications", [])
            allers = selected_patient.get("allergies", [])
            history = selected_patient.get("medical_history", "")

            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.write("**Conditions**")
                if conds:
                    for c in conds:
                        st.write(f"- {c}")
                else:
                    st.write("None recorded")
            with col_b:
                st.write("**Medications**")
                if meds:
                    for m in meds:
                        st.write(f"- {m}")
                else:
                    st.write("None recorded")
            with col_c:
                st.write("**Allergies**")
                if allers:
                    for a in allers:
                        st.write(f"- {a}")
                else:
                    st.write("None recorded")

            if history:
                st.divider()
                st.write("**Medical History**")
                st.write(history)

        elif not filtered:
            st.info(f'No patients match "{search}"')
