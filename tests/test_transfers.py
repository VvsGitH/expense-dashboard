import pandas as pd

from app.domain import transfers
from app.repository import db
from app.repository.db import TRANSACTION_COLUMNS


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


def test_pair_same_amount_different_bank_within_7_days_is_detected(conn):
    _insert(conn, date="2024-01-05", description="Uscita", value=50.0, bank="poste", type_="expense")
    _insert(conn, date="2024-01-10", description="Entrata", value=50.0, bank="bbva", type_="income")

    count = transfers.rebuild_cache(conn)

    assert count == 1
    detected = transfers.get_transfers(conn)
    assert len(detected) == 1
    assert detected.iloc[0]["expense_bank"] == "poste"
    assert detected.iloc[0]["income_bank"] == "bbva"


def test_pair_same_bank_is_not_detected(conn):
    _insert(conn, date="2024-01-05", description="Uscita", value=50.0, bank="poste", type_="expense")
    _insert(conn, date="2024-01-10", description="Entrata", value=50.0, bank="poste", type_="income")

    count = transfers.rebuild_cache(conn)

    assert count == 0
    assert transfers.get_transfers(conn).empty


def test_pair_more_than_7_days_apart_is_not_detected(conn):
    _insert(conn, date="2024-01-01", description="Uscita", value=50.0, bank="poste", type_="expense")
    _insert(conn, date="2024-01-10", description="Entrata", value=50.0, bank="bbva", type_="income")

    count = transfers.rebuild_cache(conn)

    assert count == 0
    assert transfers.get_transfers(conn).empty


def test_pair_with_different_amount_is_not_detected(conn):
    _insert(conn, date="2024-01-05", description="Uscita", value=50.0, bank="poste", type_="expense")
    _insert(conn, date="2024-01-10", description="Entrata", value=60.0, bank="bbva", type_="income")

    count = transfers.rebuild_cache(conn)

    assert count == 0
    assert transfers.get_transfers(conn).empty


def test_rebuild_replaces_cache_instead_of_accumulating(conn):
    _insert(conn, date="2024-01-05", description="Uscita", value=50.0, bank="poste", type_="expense")
    _insert(conn, date="2024-01-10", description="Entrata", value=50.0, bank="bbva", type_="income")

    transfers.rebuild_cache(conn)
    transfers.rebuild_cache(conn)

    assert len(transfers.get_transfers(conn)) == 1


def test_ingest_file_triggers_cache_rebuild(conn, tmp_path):
    from app.domain.enums import Bank
    from app.service import ingest_file
    from conftest import make_bbva_file, make_poste_file

    poste_file = make_poste_file(
        tmp_path / "poste.xlsx",
        {
            "date": [pd.Timestamp(2024, 1, 5)],
            "description": ["Giroconto verso BBVA"],
            "addebiti": [50.00],
            "accrediti": [None],
        },
    )
    bbva_file = make_bbva_file(
        tmp_path / "bbva.xlsx",
        {
            "date": ["10/01/2024"],
            "description": ["Giroconto da Poste"],
            "importo": [50.00],
        },
    )

    with open(poste_file, "rb") as f:
        ingest_file(Bank.POSTE, f, "poste.xlsx", conn=conn)
    with open(bbva_file, "rb") as f:
        ingest_file(Bank.BBVA, f, "bbva.xlsx", conn=conn)

    detected = transfers.get_transfers(conn)
    assert len(detected) == 1
    assert detected.iloc[0]["value"] == 50.0
