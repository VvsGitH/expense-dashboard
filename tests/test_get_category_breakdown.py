import pandas as pd

from app import categorization, db, transfers
from app.db import TRANSACTION_COLUMNS
from app.service import get_category_breakdown


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


def test_breaks_down_expenses_by_known_category(conn):
    _insert(conn, date="2024-01-05", description="Farmacia Rossi", value=50.0, bank="poste", type_="expense")
    _insert(conn, date="2024-01-06", description="Farmacia Bianchi", value=30.0, bank="poste", type_="expense")
    _insert(conn, date="2024-01-07", description="Supermercato Conad", value=20.0, bank="poste", type_="expense")

    result = get_category_breakdown(conn=conn)

    by_category = {row["category"]: row["value"] for row in result}
    assert by_category["salute"] == 80.0
    assert by_category["spesa"] == 20.0


def test_excludes_income_transactions(conn):
    _insert(conn, date="2024-01-05", description="Farmacia Rossi", value=50.0, bank="poste", type_="expense")
    _insert(conn, date="2024-01-10", description="Stipendio", value=1500.0, bank="poste", type_="income")

    result = get_category_breakdown(conn=conn)

    assert {row["category"] for row in result} == {"salute"}


def test_excludes_cross_bank_transfer_pairs(conn):
    _insert(conn, date="2024-03-05", description="Giroconto verso BBVA", value=100.0, bank="poste", type_="expense")
    _insert(conn, date="2024-03-08", description="Giroconto da Poste", value=100.0, bank="bbva", type_="income")
    _insert(conn, date="2024-03-10", description="Farmacia Rossi", value=25.0, bank="poste", type_="expense")
    transfers.rebuild_cache(conn)

    result = get_category_breakdown(conn=conn)

    by_category = {row["category"]: row["value"] for row in result}
    assert by_category == {"salute": 25.0}


def test_respects_own_date_range(conn):
    _insert(conn, date="2024-01-05", description="Farmacia Rossi", value=50.0, bank="poste", type_="expense")
    _insert(conn, date="2024-02-05", description="Supermercato Conad", value=20.0, bank="poste", type_="expense")

    result = get_category_breakdown(conn=conn, date_from="2024-02-01", date_to="2024-02-29")

    assert {row["category"] for row in result} == {"spesa"}


def test_returns_empty_list_when_no_expenses_in_range(conn):
    _insert(conn, date="2024-01-05", description="Farmacia Rossi", value=50.0, bank="poste", type_="expense")

    result = get_category_breakdown(conn=conn, date_from="2025-01-01", date_to="2025-01-31")

    assert result == []


def test_category_rule_changes_reflect_immediately_without_explicit_recompute(conn, monkeypatch):
    _insert(conn, date="2024-01-05", description="Negozio Misterioso XYZ", value=10.0, bank="poste", type_="expense")

    before = get_category_breakdown(conn=conn)
    assert {row["category"] for row in before} == {"other"}

    monkeypatch.setitem(categorization.EXP_CATEGORIES, "misteriosa", ["negozio misterioso"])

    after = get_category_breakdown(conn=conn)
    assert {row["category"] for row in after} == {"misteriosa"}
