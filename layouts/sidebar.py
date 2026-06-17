import streamlit as st


def render_sidebar():
    if "current_page" not in st.session_state:
        st.session_state.current_page = "dashboard"

    with st.sidebar:
        st.title("DDSS")
        st.caption("Doctor Decision Support System")

        '''page = st.radio(
            "Navigate",
            ["Dashboard", "New Patient", "Patient Records", "Prescription Check"],
            index=["Dashboard", "New Patient", "Patient Records", "Prescription Check"].index(
                st.session_state.current_page
            ) if st.session_state.current_page in ["Dashboard", "New Patient", "Patient Records", "Prescription Check"] else 0,
            label_visibility="collapsed",
        )

        page_map = {
            "Dashboard": "dashboard",
            "New Patient": "add patient",
            "Patient Records": "view patients",
            "Prescription Check": "validation",
        }
        '''
        if st.button("Dashboard", use_container_width=True):
            st.session_state.current_page = "dashboard"

        if st.button("New Patient", use_container_width= True):
            st.session_state.current_page = "add patient"

        if st.button("Your Patients", use_container_width= True):
            st.session_state.current_page= "view patients"

        if st.button("Presciption Check", use_container_width= True):
            st.session_state.current_page = "validation"



        st.sidebar.divider()
        st.caption("v1.0 — Developed by Abdelrhaman Yahia, Maryam Oyoun, Ahmed Sameh")

    return st.session_state.current_page
