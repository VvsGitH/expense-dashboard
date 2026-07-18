import pandas as pd

import db
from db import TRANSACTION_COLUMNS
from domain.enums import Bank, TransactionType
from service import get_transactions


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
    _insert(conn, date="2024-01-05", description="Farmacia Rossi", value=50.0, bank="poste", type_="expense")
    _insert(conn, date="2024-01-10", description="Stipendio Gennaio", value=1500.0, bank="poste", type_="income")
    _insert(conn, date="2024-02-01", description="Supermercato Conad", value=30.0, bank="bbva", type_="expense")
    _insert(conn, date="2024-02-15", description="Giroconto verso Poste", value=200.0, bank="bbva", type_="income")


def test_returns_all_transactions_including_cross_bank_transfers_by_default(conn):
    _seed(conn)

    result = get_transactions(conn=conn)

    assert len(result) == 4
    assert {row["description"] for row in result} == {
        "Farmacia Rossi",
        "Stipendio Gennaio",
        "Supermercato Conad",
        "Giroconto verso Poste",
    }


def test_filters_by_date_range(conn):
    _seed(conn)

    result = get_transactions(conn=conn, date_from="2024-01-06", date_to="2024-02-01")

    assert {row["description"] for row in result} == {"Stipendio Gennaio", "Supermercato Conad"}


def test_filters_by_type_expense_only(conn):
    _seed(conn)

    result = get_transactions(conn=conn, transaction_type=TransactionType.EXPENSE)

    assert {row["description"] for row in result} == {"Farmacia Rossi", "Supermercato Conad"}


def test_filters_by_type_income_only(conn):
    _seed(conn)

    result = get_transactions(conn=conn, transaction_type=TransactionType.INCOME)

    assert {row["description"] for row in result} == {"Stipendio Gennaio", "Giroconto verso Poste"}


def test_filters_by_bank(conn):
    _seed(conn)

    result = get_transactions(conn=conn, bank=Bank.BBVA)

    assert {row["description"] for row in result} == {"Supermercato Conad", "Giroconto verso Poste"}


def test_filters_by_description_text_case_insensitive(conn):
    _seed(conn)

    result = get_transactions(conn=conn, description_contains="giroconto")

    assert {row["description"] for row in result} == {"Giroconto verso Poste"}


def test_filters_by_description_text_treats_input_as_literal_not_regex(conn):
    _insert(conn, date="2024-03-01", description="POS (Conad)", value=10.0, bank="poste", type_="expense")
    _insert(conn, date="2024-03-02", description="POS Esselunga", value=10.0, bank="poste", type_="expense")

    result = get_transactions(conn=conn, description_contains="(Conad)")

    assert {row["description"] for row in result} == {"POS (Conad)"}


def test_combines_multiple_filters(conn):
    _seed(conn)

    result = get_transactions(
        conn=conn,
        date_from="2024-01-01",
        date_to="2024-12-31",
        transaction_type=TransactionType.EXPENSE,
        bank=Bank.POSTE,
        description_contains="farmacia",
    )

    assert [row["description"] for row in result] == ["Farmacia Rossi"]


def test_no_match_returns_empty_list(conn):
    _seed(conn)

    result = get_transactions(conn=conn, bank=Bank.OTHERS)

    assert result == []
