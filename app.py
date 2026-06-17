from ui.add_patient import render_add_patient
from layouts.sidebar import render_sidebar
from ui.view_patient import render_view_patients
from ui.validation import render_validation
from ui.dashboard import render_dashboard
import streamlit as st

st.set_page_config(
    page_title="CDSS - Clinical Decision Support System",
    page_icon="🏥",
    layout="wide",
)

selected_page = render_sidebar()

if selected_page == "home" or selected_page == "dashboard":
    render_dashboard()

elif selected_page == "add patient":
    render_add_patient()

elif selected_page == "view patients":
    render_view_patients()

elif selected_page == "validation":
    render_validation()
