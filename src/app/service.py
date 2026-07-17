import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone

import pandas as pd

from app.domain import transfers
from app.domain.categorization import categorize_description
from app.domain.enums import Bank, TransactionType
from app.ingestion import bbva, others, poste
from app.repository import db

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


def _filter_date_range(
    transactions: pd.DataFrame, date_from: str | None, date_to: str | None
) -> pd.DataFrame:
    if date_from is not None:
        transactions = transactions[transactions["date"] >= pd.Timestamp(date_from)]
    if date_to is not None:
        transactions = transactions[transactions["date"] <= pd.Timestamp(date_to)]
    return transactions


def _read_non_transfer_transactions(
    conn, date_from: str | None, date_to: str | None
) -> pd.DataFrame:
    transactions = db.read_transactions(conn)
    transfer_ids = transfers.get_transfer_leg_ids(conn)
    transactions = transactions[~transactions["id"].isin(transfer_ids)]
    return _filter_date_range(transactions, date_from, date_to)


def get_transactions(
    conn=None,
    date_from: str | None = None,
    date_to: str | None = None,
    transaction_type: TransactionType | None = None,
    bank: Bank | None = None,
    description_contains: str | None = None,
) -> list[dict]:
    owns_connection = conn is None
    conn = conn or db.get_connection()
    try:
        transactions = db.read_transactions(conn)
        transactions = _filter_date_range(transactions, date_from, date_to)

        if transaction_type is not None:
            transactions = transactions[transactions["type"] == transaction_type.value]
        if bank is not None:
            transactions = transactions[transactions["bank"] == bank.value]
        if description_contains:
            transactions = transactions[
                transactions["description"].str.contains(
                    description_contains, case=False, na=False, regex=False
                )
            ]

        transactions = transactions.sort_values("date")
        records = transactions.to_dict("records")
        for record in records:
            record["date"] = record["date"].strftime("%Y-%m-%d")
        return records
    finally:
        if owns_connection:
            conn.close()


def get_monthly_totals(
    conn=None, date_from: str | None = None, date_to: str | None = None
) -> list[dict]:
    owns_connection = conn is None
    conn = conn or db.get_connection()
    try:
        transactions = _read_non_transfer_transactions(conn, date_from, date_to)

        if transactions.empty:
            return []

        transactions = transactions.assign(month=transactions["date"].dt.strftime("%Y-%m"))
        totals = (
            transactions.groupby(["month", "type"])["value"]
            .sum()
            .unstack(fill_value=0.0)
            .reindex(columns=[TransactionType.INCOME.value, TransactionType.EXPENSE.value], fill_value=0.0)
            .rename(
                columns={
                    TransactionType.INCOME.value: "income",
                    TransactionType.EXPENSE.value: "expense",
                }
            )
            .reset_index()
            .sort_values("month")
        )
        return totals.to_dict("records")
    finally:
        if owns_connection:
            conn.close()


def get_category_breakdown(
    conn=None, date_from: str | None = None, date_to: str | None = None
) -> list[dict]:
    owns_connection = conn is None
    conn = conn or db.get_connection()
    try:
        transactions = _read_non_transfer_transactions(conn, date_from, date_to)

        expenses = transactions[transactions["type"] == TransactionType.EXPENSE.value]
        if expenses.empty:
            return []

        expenses = expenses.assign(
            category=expenses["description"].apply(categorize_description)
        )
        breakdown = (
            expenses.groupby("category")["value"]
            .sum()
            .sort_values(ascending=False)
            .reset_index()
        )
        return breakdown.to_dict("records")
    finally:
        if owns_connection:
            conn.close()
