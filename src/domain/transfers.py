import sqlite3

import pandas as pd

import db
from domain.enums import TransactionType

TRANSFER_WINDOW_DAYS = 7


def rebuild_cache(conn: sqlite3.Connection) -> int:
    """Truncates and rebuilds the cross_bank_transfers cache from the raw transactions."""
    transactions = db.read_transactions(conn)
    expenses = transactions[transactions["type"] == TransactionType.EXPENSE.value]
    income = transactions[transactions["type"] == TransactionType.INCOME.value]

    pairs = pd.merge(expenses, income, on="value", suffixes=("_exp", "_inc"), how="inner")
    pairs = pairs[
        (pairs["bank_exp"] != pairs["bank_inc"])
        & ((pairs["date_inc"] - pairs["date_exp"]).abs().dt.days <= TRANSFER_WINDOW_DAYS)
    ]
    pairs = pairs.rename(
        columns={"id_exp": "expense_transaction_id", "id_inc": "income_transaction_id"}
    )

    db.replace_cross_bank_transfers(conn, pairs)
    return len(pairs)


def get_transfers(conn: sqlite3.Connection) -> pd.DataFrame:
    """Returns the materialized cross-bank transfer pairs, for debug inspection."""
    return db.read_cross_bank_transfers(conn)


def get_transfer_leg_ids(conn: sqlite3.Connection) -> set[int]:
    """Returns the ids of all transactions that are one leg of a detected cross-bank transfer."""
    detected = db.read_cross_bank_transfers(conn)
    if detected.empty:
        return set()
    return set(detected["expense_id"]) | set(detected["income_id"])
