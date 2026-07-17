import streamlit as st

from app.domain.enums import Bank
from app.service import ingest_file, list_uploads, undo_upload

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

st.header("Storico caricamenti")

if "undo_message" in st.session_state:
    st.success(st.session_state.pop("undo_message"))

uploads = list_uploads()
if not uploads:
    st.info("Nessun caricamento effettuato finora.")
else:
    for upload in uploads:
        col_info, col_action = st.columns([4, 1])
        col_info.write(
            f"{upload.uploaded_at} — **{BANK_LABELS.get(Bank(upload.bank), upload.bank)}** — "
            f"{upload.source_filename} — {upload.transaction_count} transazioni"
        )
        if col_action.button("Annulla", key=f"undo-{upload.upload_id}"):
            removed = undo_upload(upload.upload_id)
            st.session_state["undo_message"] = f"Rimosse {removed} transazioni."
            st.rerun()
