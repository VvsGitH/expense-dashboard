import pandas as pd

from app.domain.enums import Bank
from app.service import ingest_file
from conftest import make_poste_file


def test_ingest_poste_file_stores_parsed_transactions(conn, poste_file):
    with open(poste_file, "rb") as f:
        result = ingest_file(Bank.POSTE, f, "poste.xlsx", conn=conn)

    assert result.inserted == 2
    assert result.duplicates == 0

    by_description = {row["description"]: row for row in result.inserted_transactions}

    expense = by_description["Farmacia Rossi"]
    assert expense["date"] == "2024-01-05"
    assert expense["value"] == 50.00
    assert expense["bank"] == "poste"
    assert expense["type"] == "expense"

    income = by_description["Stipendio Gennaio"]
    assert income["date"] == "2024-01-10"
    assert income["value"] == 1500.00
    assert income["bank"] == "poste"
    assert income["type"] == "income"


def test_reingesting_same_file_finds_all_rows_duplicate(conn, poste_file):
    with open(poste_file, "rb") as f:
        ingest_file(Bank.POSTE, f, "poste.xlsx", conn=conn)

    with open(poste_file, "rb") as f:
        result = ingest_file(Bank.POSTE, f, "poste.xlsx", conn=conn)

    assert result.inserted == 0
    assert result.duplicates == 2
    assert result.inserted_transactions == []


def test_ingest_bbva_file_stores_parsed_transactions(conn, bbva_file):
    with open(bbva_file, "rb") as f:
        result = ingest_file(Bank.BBVA, f, "bbva.xlsx", conn=conn)

    assert result.inserted == 2
    assert result.duplicates == 0

    by_description = {row["description"]: row for row in result.inserted_transactions}

    expense = by_description["Supermercato Conad"]
    assert expense["date"] == "2024-01-05"
    assert expense["value"] == 30.00
    assert expense["bank"] == "bbva"
    assert expense["type"] == "expense"

    income = by_description["Bonifico ricevuto"]
    assert income["date"] == "2024-01-10"
    assert income["value"] == 200.00
    assert income["bank"] == "bbva"
    assert income["type"] == "income"


def test_ingest_others_file_stores_parsed_transactions(conn, others_file):
    with open(others_file, "rb") as f:
        result = ingest_file(Bank.OTHERS, f, "others.xlsx", conn=conn)

    assert result.inserted == 2
    assert result.duplicates == 0

    by_description = {row["description"]: row for row in result.inserted_transactions}

    expense = by_description["Farmacia"]
    assert expense["date"] == "2024-01-05"
    assert expense["value"] == 20.00
    assert expense["bank"] == "others"
    assert expense["type"] == "expense"

    income = by_description["Rimborso"]
    assert income["date"] == "2024-01-10"
    assert income["value"] == 100.00
    assert income["bank"] == "others"
    assert income["type"] == "income"


def test_overlapping_upload_inserts_only_the_new_row(conn, poste_file, tmp_path):
    with open(poste_file, "rb") as f:
        ingest_file(Bank.POSTE, f, "poste.xlsx", conn=conn)

    # Second export re-download: includes the previously-seen "Farmacia Rossi"
    # row plus one genuinely new transaction.
    overlapping_file = make_poste_file(
        tmp_path / "poste_2.xlsx",
        {
            "date": [pd.Timestamp(2024, 1, 5), pd.Timestamp(2024, 1, 20)],
            "description": ["Farmacia Rossi", "Supermercato Coop"],
            "addebiti": [50.00, 35.00],
            "accrediti": [None, None],
        },
    )

    with open(overlapping_file, "rb") as f:
        result = ingest_file(Bank.POSTE, f, "poste_2.xlsx", conn=conn)

    assert result.inserted == 1
    assert result.duplicates == 1
    assert result.inserted_transactions[0]["description"] == "Supermercato Coop"


def test_two_identical_rows_in_the_same_file_are_treated_as_one_duplicate(conn, tmp_path):
    # Deliberately accepted limitation of existence-only dedup (ADR-0002): two
    # genuinely identical transactions on the same day collapse into one.
    file_with_duplicate_rows = make_poste_file(
        tmp_path / "poste_dup.xlsx",
        {
            "date": [pd.Timestamp(2024, 1, 5), pd.Timestamp(2024, 1, 5)],
            "description": ["Bar Centrale", "Bar Centrale"],
            "addebiti": [1.20, 1.20],
            "accrediti": [None, None],
        },
    )

    with open(file_with_duplicate_rows, "rb") as f:
        result = ingest_file(Bank.POSTE, f, "poste_dup.xlsx", conn=conn)

    assert result.inserted == 1
    assert result.duplicates == 1
