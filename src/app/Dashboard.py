import sys
from pathlib import Path

_app_dir = next(p for p in Path(__file__).resolve().parents if p.name == "app")
sys.path.insert(0, str(_app_dir.parent))

import streamlit as st

from app import db, transfers

st.set_page_config(page_title="Expenses Dashboard", layout="wide")

conn = db.get_connection()
try:
    transfers.rebuild_cache(conn)
finally:
    conn.close()

st.title("Dashboard")
st.info(
    "La dashboard di monitoraggio spese (tabella, grafico mensile, categorie) "
    "sarà disponibile qui nelle prossime iterazioni."
)
