import streamlit as st


def render_sidebar():
    if "current_page" not in st.session_state:
        st.session_state.current_page = "dashboard"

    with st.sidebar:
        st.title("DDSS")
        st.caption("Doctor Decision Support System")
        pages = [
        ("Dashboard", "dashboard"),
        ("New Patient", "add patient"),
        ("Your Patients", "view patients"),
        ("Prescription Check", "validation"),]

        for label, target in pages:
            is_active = st.session_state.current_page == target
            if is_active:
                st.markdown(
                    f"<div style='background-color:#4b4bff; border:1px solid #1a73e8; "
                    f"border-radius:5px; padding:8px 12px; margin-bottom:7px;'>"
                    f"<b>{label}</b></div>",
                    unsafe_allow_html=True,
                )
            else:
                if st.button(label, key=f"nav_{target}", use_container_width=True):
                    st.session_state.current_page = target
                    st.rerun()



        st.sidebar.divider()
        st.caption("v1.0 — Developed by Abdelrhaman Yahia, Maryam Oyoun, Ahmed Sameh")

    return st.session_state.current_page
