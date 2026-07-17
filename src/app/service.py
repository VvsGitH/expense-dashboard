import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone

import pandas as pd

from app import db, transfers
from app.enums import Bank
from app.ingestion import bbva, others, poste

_PARSERS = {
    Bank.POSTE: poste.parse,
    Bank.BBVA: bbva.parse,
    Bank.OTHERS: others.parse,
}


@dataclass
class IngestResult:
    inserted: int
    duplicates: int
    inserted_transactions: list[dict] = field(default_factory=list)


@dataclass
class Upload:
    upload_id: str
    bank: str
    uploaded_at: str
    source_filename: str
    transaction_count: int


def ingest_file(bank: Bank, file, filename: str, conn=None) -> IngestResult:
    owns_connection = conn is None
    conn = conn or db.get_connection()
    try:
        parsed = _PARSERS[bank](file)
        parsed["date"] = parsed["date"].dt.strftime("%Y-%m-%d")
        parsed["bank"] = bank.value

        seen = db.existing_keys(conn, bank.value)
        inserted_rows = []
        duplicate_count = 0
        for row in parsed.to_dict("records"):
            key = (row["date"], row["value"], row["description"])
            if key in seen:
                duplicate_count += 1
                continue
            seen.add(key)
            inserted_rows.append(row)

        to_insert = pd.DataFrame(inserted_rows, columns=parsed.columns)
        upload_id = str(uuid.uuid4())
        uploaded_at = datetime.now(timezone.utc).isoformat()
        to_insert["upload_id"] = upload_id
        to_insert["uploaded_at"] = uploaded_at
        to_insert["source_filename"] = filename

        db.insert_transactions(conn, to_insert)
        transfers.rebuild_cache(conn)

        return IngestResult(
            inserted=len(to_insert),
            duplicates=duplicate_count,
            inserted_transactions=to_insert.to_dict("records"),
        )
    finally:
        if owns_connection:
            conn.close()


def list_uploads(conn=None) -> list[Upload]:
    owns_connection = conn is None
    conn = conn or db.get_connection()
    try:
        return [
            Upload(
                upload_id=row["upload_id"],
                bank=row["bank"],
                uploaded_at=row["uploaded_at"],
                source_filename=row["source_filename"],
                transaction_count=int(row["transaction_count"]),
            )
            for row in db.list_uploads(conn).to_dict("records")
        ]
    finally:
        if owns_connection:
            conn.close()


def undo_upload(upload_id: str, conn=None) -> int:
    owns_connection = conn is None
    conn = conn or db.get_connection()
    try:
        removed = db.delete_transactions_by_upload(conn, upload_id)
        transfers.rebuild_cache(conn)
        return removed
    finally:
        if owns_connection:
            conn.close()
