import sys
from pathlib import Path

_app_dir = next(p for p in Path(__file__).resolve().parents if p.name == "app")
sys.path.insert(0, str(_app_dir.parent))

import streamlit as st

from app import db, transfers
from app.charts import monthly_totals_chart_data
from app.enums import Bank, TransactionType
from app.service import get_monthly_totals, get_transactions

st.set_page_config(page_title="Expenses Dashboard", layout="wide")

conn = db.get_connection()
try:
    transfers.rebuild_cache(conn)
finally:
    conn.close()

st.title("Dashboard")

st.header("Tabella transazioni")

TYPE_LABELS = {
    None: "Entrambe",
    TransactionType.INCOME: "Entrate",
    TransactionType.EXPENSE: "Uscite",
}
BANK_LABELS = {
    None: "Tutte",
    Bank.POSTE: "Poste",
    Bank.BBVA: "BBVA",
    Bank.OTHERS: "Others",
}

col_date_from, col_date_to, col_type, col_bank, col_description = st.columns(5)
table_date_from = col_date_from.date_input("Da", value=None, key="table_date_from")
table_date_to = col_date_to.date_input("A", value=None, key="table_date_to")
table_type_label = col_type.selectbox(
    "Tipologia", list(TYPE_LABELS.values()), key="table_type"
)
table_bank_label = col_bank.selectbox("Banca", list(BANK_LABELS.values()), key="table_bank")
table_description = col_description.text_input("Descrizione contiene", key="table_description")

table_type = next(value for value, label in TYPE_LABELS.items() if label == table_type_label)
table_bank = next(value for value, label in BANK_LABELS.items() if label == table_bank_label)

transactions = get_transactions(
    date_from=table_date_from.isoformat() if table_date_from else None,
    date_to=table_date_to.isoformat() if table_date_to else None,
    transaction_type=table_type,
    bank=table_bank,
    description_contains=table_description or None,
)
st.dataframe(transactions, use_container_width=True)

st.header("Entrate e Uscite mensili")

col_bar_date_from, col_bar_date_to = st.columns(2)
bar_date_from = col_bar_date_from.date_input("Da", value=None, key="bar_date_from")
bar_date_to = col_bar_date_to.date_input("A", value=None, key="bar_date_to")

monthly_totals = get_monthly_totals(
    date_from=bar_date_from.isoformat() if bar_date_from else None,
    date_to=bar_date_to.isoformat() if bar_date_to else None,
)
monthly_totals_df = monthly_totals_chart_data(monthly_totals)
if monthly_totals_df.empty:
    st.info("Nessuna Transazione nel periodo selezionato.")
else:
    st.bar_chart(
        monthly_totals_df,
        stack=False,
        use_container_width=True,
    )
