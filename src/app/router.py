import sys
from pathlib import Path

_app_dir = next(p for p in Path(__file__).resolve().parents if p.name == "app")
sys.path.insert(0, str(_app_dir.parent))

import streamlit as st

dashboard_page = st.Page("pages/dashboard.py", title="Dashboard")
carica_dati_page = st.Page("pages/carica_dati.py", title="Carica dati")

st.navigation([dashboard_page, carica_dati_page]).run()
