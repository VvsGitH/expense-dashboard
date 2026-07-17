import sqlite3
from pathlib import Path

import pandas as pd

DEFAULT_DB_PATH = Path(__file__).resolve().parents[2] / "data" / "expenses.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    description TEXT NOT NULL,
    value REAL NOT NULL,
    bank TEXT NOT NULL,
    type TEXT NOT NULL,
    upload_id TEXT NOT NULL,
    uploaded_at TEXT NOT NULL,
    source_filename TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS cross_bank_transfers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    expense_transaction_id INTEGER NOT NULL REFERENCES transactions(id),
    income_transaction_id INTEGER NOT NULL REFERENCES transactions(id)
);
"""

TRANSACTION_COLUMNS = [
    "date",
    "description",
    "value",
    "bank",
    "type",
    "upload_id",
    "uploaded_at",
    "source_filename",
]


def get_connection(db_path: Path | None = None) -> sqlite3.Connection:
    db_path = Path(db_path) if db_path is not None else DEFAULT_DB_PATH
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.executescript(SCHEMA)
    conn.commit()
    return conn


def existing_keys(conn: sqlite3.Connection, bank: str) -> set[tuple[str, float, str]]:
    rows = conn.execute(
        "SELECT date, value, description FROM transactions WHERE bank = ?", (bank,)
    ).fetchall()
    return {(date, value, description) for date, value, description in rows}


def insert_transactions(conn: sqlite3.Connection, rows: pd.DataFrame) -> None:
    if rows.empty:
        return
    rows.loc[:, TRANSACTION_COLUMNS].to_sql(
        "transactions", conn, if_exists="append", index=False
    )
    conn.commit()


def read_transactions(conn: sqlite3.Connection) -> pd.DataFrame:
    return pd.read_sql(
        "SELECT id, date, description, value, bank, type FROM transactions",
        conn,
        parse_dates=["date"],
    )


def replace_cross_bank_transfers(conn: sqlite3.Connection, pairs: pd.DataFrame) -> None:
    conn.execute("DELETE FROM cross_bank_transfers")
    if not pairs.empty:
        pairs.loc[:, ["expense_transaction_id", "income_transaction_id"]].to_sql(
            "cross_bank_transfers", conn, if_exists="append", index=False
        )
    conn.commit()


def read_cross_bank_transfers(conn: sqlite3.Connection) -> pd.DataFrame:
    return pd.read_sql(
        """
        SELECT
            c.id AS transfer_id,
            e.value AS value,
            e.id AS expense_id,
            e.date AS expense_date,
            e.description AS expense_description,
            e.bank AS expense_bank,
            i.id AS income_id,
            i.date AS income_date,
            i.description AS income_description,
            i.bank AS income_bank
        FROM cross_bank_transfers c
        JOIN transactions e ON e.id = c.expense_transaction_id
        JOIN transactions i ON i.id = c.income_transaction_id
        """,
        conn,
        parse_dates=["expense_date", "income_date"],
    )
