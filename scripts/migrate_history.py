"""One-off migration of the historical Excel exports into the expenses DB.

Reuses the webapp ingestion pipeline (`ingest_file`) to import the three
historical bank exports, excluding the known TFR (Trattamento di Fine Rapporto)
transaction. The retired notebook dropped it by hard-coded row index (poste row
301); here it is identified by its stable business key (date/amount/description)
instead, so it stays excluded regardless of row order.

Run once, from the repo root:

    python scripts/migrate_history.py
"""

import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO_ROOT / "src"))

import db  # noqa: E402
from domain.enums import Bank  # noqa: E402
from service import ingest_file  # noqa: E402

DATA_DIR = _REPO_ROOT / "data"

HISTORICAL_FILES: list[tuple[Bank, str]] = [
    (Bank.POSTE, "movimenti_poste.xlsx"),
    (Bank.BBVA, "movimenti_bbva.xlsx"),
    (Bank.OTHERS, "movimenti_others.xlsx"),
]

# The TFR severance transfer, excluded by the notebook as poste row 301.
TFR_DATE = "2024-06-26"
TFR_VALUE = 4620.36
TFR_DESCRIPTION_MARKER = "trattamento di fine rapporto"


def is_tfr(row: dict) -> bool:
    """Identifies the known TFR transaction by date/amount/description."""
    return (
        row["date"] == TFR_DATE
        and round(row["value"], 2) == TFR_VALUE
        and TFR_DESCRIPTION_MARKER in row["description"].lower()
    )


def migrate(conn=None) -> None:
    owns_connection = conn is None
    conn = conn or db.get_connection()
    try:
        for bank, filename in HISTORICAL_FILES:
            path = DATA_DIR / filename
            # The TFR lives only in the Poste export; scope the exclusion to it.
            exclude = is_tfr if bank is Bank.POSTE else None
            with open(path, "rb") as f:
                result = ingest_file(bank, f, filename, conn=conn, exclude=exclude)
            print(
                f"{bank.value}: {result.inserted} inserite, "
                f"{result.duplicates} duplicate, {result.excluded} escluse (TFR)"
            )
    finally:
        if owns_connection:
            conn.close()


if __name__ == "__main__":
    migrate()
