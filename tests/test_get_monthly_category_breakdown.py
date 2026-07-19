import pandas as pd

import db
from db import TRANSACTION_COLUMNS
from domain import transfers
from service import get_monthly_category_breakdown


def _insert(conn, *, date, description, value, bank, type_, upload_id="up-1"):
    row = pd.DataFrame(
        [
            {
                "date": date,
                "description": description,
                "value": value,
                "bank": bank,
                "type": type_,
                "upload_id": upload_id,
                "uploaded_at": "2024-01-01T00:00:00+00:00",
                "source_filename": "test.xlsx",
            }
        ],
        columns=TRANSACTION_COLUMNS,
    )
    db.insert_transactions(conn, row)


def test_groups_expenses_by_month_and_category(conn):
    _insert(conn, date="2024-01-05", description="Farmacia Rossi", value=50.0, bank="poste", type_="expense")
    _insert(conn, date="2024-01-06", description="Farmacia Bianchi", value=30.0, bank="poste", type_="expense")
    _insert(conn, date="2024-01-07", description="Supermercato Conad", value=20.0, bank="poste", type_="expense")
    _insert(conn, date="2024-02-05", description="Farmacia Rossi", value=10.0, bank="poste", type_="expense")

    result = get_monthly_category_breakdown(conn=conn, today=pd.Timestamp("2024-06-15"))

    by_month_category = {(row["month"], row["category"]): row["value"] for row in result}
    assert by_month_category[("2024-01", "salute")] == 80.0
    assert by_month_category[("2024-01", "spesa")] == 20.0
    assert by_month_category[("2024-02", "salute")] == 10.0


def test_excludes_income_transactions(conn):
    _insert(conn, date="2024-01-05", description="Farmacia Rossi", value=50.0, bank="poste", type_="expense")
    _insert(conn, date="2024-01-10", description="Stipendio", value=1500.0, bank="poste", type_="income")

    result = get_monthly_category_breakdown(conn=conn, today=pd.Timestamp("2024-06-15"))

    assert {(row["month"], row["category"]) for row in result} == {("2024-01", "salute")}


def test_excludes_cross_bank_transfer_pairs(conn):
    _insert(conn, date="2024-03-05", description="Giroconto verso BBVA", value=100.0, bank="poste", type_="expense")
    _insert(conn, date="2024-03-08", description="Giroconto da Poste", value=100.0, bank="bbva", type_="income")
    _insert(conn, date="2024-03-10", description="Farmacia Rossi", value=25.0, bank="poste", type_="expense")
    transfers.rebuild_cache(conn)

    result = get_monthly_category_breakdown(conn=conn, today=pd.Timestamp("2024-06-15"))

    by_month_category = {(row["month"], row["category"]): row["value"] for row in result}
    assert by_month_category == {("2024-03", "salute"): 25.0}


def test_excludes_current_month(conn):
    _insert(conn, date="2024-01-05", description="Farmacia Rossi", value=50.0, bank="poste", type_="expense")
    _insert(conn, date="2024-03-05", description="Farmacia Rossi", value=30.0, bank="poste", type_="expense")

    result = get_monthly_category_breakdown(conn=conn, today=pd.Timestamp("2024-03-15"))

    months = {row["month"] for row in result}
    assert months == {"2024-01"}


def test_respects_own_date_range(conn):
    _insert(conn, date="2024-01-05", description="Farmacia Rossi", value=50.0, bank="poste", type_="expense")
    _insert(conn, date="2024-02-05", description="Supermercato Conad", value=20.0, bank="poste", type_="expense")

    result = get_monthly_category_breakdown(
        conn=conn, date_from="2024-02-01", date_to="2024-02-29", today=pd.Timestamp("2024-06-15")
    )

    assert {row["month"] for row in result} == {"2024-02"}


def test_returns_empty_list_when_no_expenses_in_range(conn):
    _insert(conn, date="2024-01-05", description="Farmacia Rossi", value=50.0, bank="poste", type_="expense")

    result = get_monthly_category_breakdown(
        conn=conn, date_from="2025-01-01", date_to="2025-01-31", today=pd.Timestamp("2024-06-15")
    )

    assert result == []
