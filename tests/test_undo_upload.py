from app.domain import transfers
from app.domain.enums import Bank
from app.service import ingest_file, list_uploads, undo_upload


def test_undo_upload_removes_only_that_batch_transactions(conn, poste_file, others_file):
    with open(poste_file, "rb") as f:
        poste_result = ingest_file(Bank.POSTE, f, "poste.xlsx", conn=conn)
    with open(others_file, "rb") as f:
        ingest_file(Bank.OTHERS, f, "others.xlsx", conn=conn)

    poste_upload_id = poste_result.inserted_transactions[0]["upload_id"]

    removed = undo_upload(poste_upload_id, conn=conn)

    assert removed == 2
    remaining_banks = {
        row[0] for row in conn.execute("SELECT bank FROM transactions").fetchall()
    }
    assert remaining_banks == {"others"}


def test_undo_upload_forces_cross_bank_transfer_cache_rebuild(conn, tmp_path):
    from conftest import make_bbva_file, make_poste_file
    import pandas as pd

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
        poste_result = ingest_file(Bank.POSTE, f, "poste.xlsx", conn=conn)
    with open(bbva_file, "rb") as f:
        ingest_file(Bank.BBVA, f, "bbva.xlsx", conn=conn)

    assert len(transfers.get_transfers(conn)) == 1

    poste_upload_id = poste_result.inserted_transactions[0]["upload_id"]
    undo_upload(poste_upload_id, conn=conn)

    assert transfers.get_transfers(conn).empty


def test_list_uploads_returns_history_with_bank_filename_and_count(conn, poste_file, bbva_file):
    with open(poste_file, "rb") as f:
        ingest_file(Bank.POSTE, f, "poste.xlsx", conn=conn)
    with open(bbva_file, "rb") as f:
        ingest_file(Bank.BBVA, f, "bbva.xlsx", conn=conn)

    uploads = list_uploads(conn=conn)

    assert len(uploads) == 2
    by_bank = {upload.bank: upload for upload in uploads}
    assert by_bank["poste"].source_filename == "poste.xlsx"
    assert by_bank["poste"].transaction_count == 2
    assert by_bank["bbva"].source_filename == "bbva.xlsx"
    assert by_bank["bbva"].transaction_count == 2
