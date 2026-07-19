import altair as alt
import streamlit as st

import db
from domain import transfers
from domain.charts import (
    CATEGORY_TOTAL_COLUMN,
    category_breakdown_chart_data,
    category_breakdown_percentages,
    category_colors,
    category_names,
    monthly_category_breakdown_chart_data,
    monthly_totals_chart_data,
    savings_trend_chart_data,
)
from domain.enums import Bank, TransactionType
from service import (
    get_category_breakdown,
    get_monthly_cashflow_summary,
    get_monthly_category_breakdown,
    get_monthly_totals,
    get_transactions,
)

st.set_page_config(page_title="Expenses Dashboard", layout="centered")
st.markdown(
    """
    <style>
    section[data-testid="stMain"] > div[data-testid="stMainBlockContainer"] {
        max-width: 1024px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

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
st.dataframe(transactions, width="stretch")

st.header("Entrate e Uscite mensili")

st.subheader("Andamento mese per mese")

col_bar_date_from, col_bar_date_to = st.columns(2)
bar_date_from = col_bar_date_from.date_input("Da", value=None, key="bar_date_from")
bar_date_to = col_bar_date_to.date_input("A", value=None, key="bar_date_to")
bar_date_from_iso = bar_date_from.isoformat() if bar_date_from else None
bar_date_to_iso = bar_date_to.isoformat() if bar_date_to else None

monthly_totals = get_monthly_totals(date_from=bar_date_from_iso, date_to=bar_date_to_iso)
monthly_totals_df = monthly_totals_chart_data(monthly_totals)
if monthly_totals_df.empty:
    st.info("Nessuna Transazione nel periodo selezionato.")
else:
    st.bar_chart(
        monthly_totals_df,
        stack=False,
        width="stretch",
    )

st.subheader("Andamento risparmi")

if monthly_totals_df.empty:
    st.info("Nessuna Transazione nel periodo selezionato.")
else:
    st.line_chart(
        savings_trend_chart_data(monthly_totals),
        width="stretch",
    )

st.subheader("Flusso di cassa mensile")

cashflow_summary = get_monthly_cashflow_summary(date_from=bar_date_from_iso, date_to=bar_date_to_iso)
if cashflow_summary is None:
    st.info("Intervallo troppo piccolo per calcolare il flusso di cassa mensile")
else:
    col_income, col_expense, col_difference = st.columns(3)
    col_income.metric("Entrate mensili (media)", f"€ {cashflow_summary.income.mean:.2f}")
    col_income.metric("Entrate mensili (mediana)", f"€ {cashflow_summary.income.median:.2f}")
    col_expense.metric("Uscite mensili (media)", f"€ {cashflow_summary.expense.mean:.2f}")
    col_expense.metric("Uscite mensili (mediana)", f"€ {cashflow_summary.expense.median:.2f}")
    col_difference.metric("Differenza mensile (media)", f"€ {cashflow_summary.difference.mean:.2f}")
    col_difference.metric("Differenza mensile (mediana)", f"€ {cashflow_summary.difference.median:.2f}")

st.header("Uscite per Categoria")

col_category_date_from, col_category_date_to = st.columns(2)
category_date_from = col_category_date_from.date_input("Da", value=None, key="category_date_from")
category_date_to = col_category_date_to.date_input("A", value=None, key="category_date_to")
category_date_from_iso = category_date_from.isoformat() if category_date_from else None
category_date_to_iso = category_date_to.isoformat() if category_date_to else None

category_breakdown = get_category_breakdown(date_from=category_date_from_iso, date_to=category_date_to_iso)
category_totals = category_breakdown_chart_data(category_breakdown)
if category_totals.empty:
    st.info("Nessuna Uscita nel periodo selezionato.")
else:
    known_categories = category_names()
    category_color_scale = alt.Scale(domain=known_categories, range=category_colors(known_categories))
    category_percentages = category_breakdown_percentages(category_totals)
    category_chart_data = category_totals.rename_axis("Categoria").reset_index(name=CATEGORY_TOTAL_COLUMN)
    category_chart_data["Percentuale"] = category_chart_data["Categoria"].map(category_percentages)
    category_chart = (
        alt.Chart(category_chart_data)
        .mark_bar()
        .encode(
            x=alt.X(f"{CATEGORY_TOTAL_COLUMN}:Q"),
            y=alt.Y("Categoria:N", sort="-x"),
            color=alt.Color("Categoria:N", scale=category_color_scale, legend=None),
            tooltip=[
                "Categoria",
                CATEGORY_TOTAL_COLUMN,
                alt.Tooltip("Percentuale:Q", title="Percentuale (%)", format=".1f"),
            ],
        )
    )
    st.altair_chart(category_chart, width="stretch")

    st.subheader("Spese mensili per Categoria")

    monthly_category_breakdown = get_monthly_category_breakdown(
        date_from=category_date_from_iso, date_to=category_date_to_iso
    )
    monthly_category_chart_data = monthly_category_breakdown_chart_data(monthly_category_breakdown)
    if monthly_category_chart_data.empty:
        st.info("Nessuna Uscita nel periodo selezionato.")
    else:
        monthly_category_chart = (
            alt.Chart(monthly_category_chart_data)
            .mark_bar()
            .encode(
                x=alt.X("Mese:O"),
                y=alt.Y(
                    f"{CATEGORY_TOTAL_COLUMN}:Q",
                    stack="normalize",
                    title="Quota (%)",
                    axis=alt.Axis(format="%"),
                ),
                color=alt.Color("Categoria:N", scale=category_color_scale, legend=alt.Legend(title="Categoria")),
                tooltip=[
                    "Mese",
                    "Categoria",
                    CATEGORY_TOTAL_COLUMN,
                    alt.Tooltip("Percentuale:Q", title="Percentuale (%)", format=".1f"),
                ],
            )
        )
        st.altair_chart(monthly_category_chart, width="stretch")
