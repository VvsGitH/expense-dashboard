import pandas as pd

import db
from db import TRANSACTION_COLUMNS
from domain import transfers
from service import get_monthly_totals


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


def _seed(conn):
    _insert(conn, date="2024-01-05", description="Farmacia", value=50.0, bank="poste", type_="expense")
    _insert(conn, date="2024-01-10", description="Stipendio", value=1500.0, bank="poste", type_="income")
    _insert(conn, date="2024-02-01", description="Spesa", value=30.0, bank="bbva", type_="expense")
    _insert(conn, date="2024-02-15", description="Rimborso", value=200.0, bank="poste", type_="income")
    # Cross-bank transfer pair (same amount, different bank, within 7 days) — must be excluded.
    _insert(conn, date="2024-03-05", description="Giroconto verso BBVA", value=100.0, bank="poste", type_="expense")
    _insert(conn, date="2024-03-08", description="Giroconto da Poste", value=100.0, bank="bbva", type_="income")
    # Genuine March movements, not part of the transfer.
    _insert(conn, date="2024-03-10", description="Bar", value=20.0, bank="poste", type_="expense")
    _insert(conn, date="2024-03-12", description="Regalo", value=300.0, bank="poste", type_="income")
    transfers.rebuild_cache(conn)


def test_returns_monthly_income_and_expense_totals(conn):
    _seed(conn)

    result = get_monthly_totals(conn=conn, today=pd.Timestamp("2024-06-15"))

    by_month = {row["month"]: row for row in result}
    assert by_month["2024-01"]["income"] == 1500.0
    assert by_month["2024-01"]["expense"] == 50.0
    assert by_month["2024-02"]["income"] == 200.0
    assert by_month["2024-02"]["expense"] == 30.0


def test_excludes_cross_bank_transfer_pairs_from_monthly_totals(conn):
    _seed(conn)

    result = get_monthly_totals(conn=conn, today=pd.Timestamp("2024-06-15"))

    by_month = {row["month"]: row for row in result}
    assert by_month["2024-03"]["income"] == 300.0
    assert by_month["2024-03"]["expense"] == 20.0


def test_respects_own_date_range(conn):
    _seed(conn)

    result = get_monthly_totals(
        conn=conn, date_from="2024-02-01", date_to="2024-02-29", today=pd.Timestamp("2024-06-15")
    )

    assert {row["month"] for row in result} == {"2024-02"}


def test_returns_empty_list_when_no_transactions_in_range(conn):
    _seed(conn)

    result = get_monthly_totals(
        conn=conn, date_from="2025-01-01", date_to="2025-01-31", today=pd.Timestamp("2024-06-15")
    )

    assert result == []


def test_excludes_current_month_from_monthly_totals(conn):
    _seed(conn)

    result = get_monthly_totals(conn=conn, today=pd.Timestamp("2024-03-15"))

    months = {row["month"] for row in result}
    assert months == {"2024-01", "2024-02"}
