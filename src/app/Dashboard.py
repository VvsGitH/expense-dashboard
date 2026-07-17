import sys
from pathlib import Path

_app_dir = next(p for p in Path(__file__).resolve().parents if p.name == "app")
sys.path.insert(0, str(_app_dir.parent))

import streamlit as st

st.set_page_config(page_title="Expenses Dashboard", layout="wide")

st.title("Dashboard")
st.info(
    "La dashboard di monitoraggio spese (tabella, grafico mensile, categorie) "
    "sarà disponibile qui nelle prossime iterazioni."
)
