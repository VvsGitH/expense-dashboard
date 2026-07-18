import streamlit as st

dashboard_page = st.Page("pages/dashboard.py", title="Dashboard")
carica_dati_page = st.Page("pages/carica_dati.py", title="Carica dati")

st.navigation([dashboard_page, carica_dati_page]).run()
