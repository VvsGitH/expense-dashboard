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
    conn.execute(SCHEMA)
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
