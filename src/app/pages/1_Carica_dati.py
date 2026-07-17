import sys
from pathlib import Path

_app_dir = next(p for p in Path(__file__).resolve().parents if p.name == "app")
sys.path.insert(0, str(_app_dir.parent))

import streamlit as st

from app.enums import Bank
from app.service import ingest_file

st.set_page_config(page_title="Carica dati", layout="wide")
st.title("Carica dati")

BANK_LABELS = {
    Bank.POSTE: "Poste",
    Bank.BBVA: "BBVA",
    Bank.OTHERS: "Others",
}

selected_label = st.selectbox("Banca", list(BANK_LABELS.values()))
selected_bank = next(bank for bank, label in BANK_LABELS.items() if label == selected_label)

uploaded_file = st.file_uploader("Estratto conto (Excel)", type=["xlsx"])

if uploaded_file is not None and st.button("Carica"):
    result = ingest_file(selected_bank, uploaded_file, uploaded_file.name)
    st.success(
        f"Inserite {result.inserted} transazioni, "
        f"{result.duplicates} scartate come duplicate."
    )
