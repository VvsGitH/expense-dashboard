import pandas as pd

from app.ingestion._shared import type_from_sign

SHEET_NAME = "Movimenti"
HEADER_ROW = 4


def parse(file) -> pd.DataFrame:
    raw = pd.read_excel(
        file, sheet_name=SHEET_NAME, header=HEADER_ROW, decimal=",", thousands="."
    )
    valore = raw["Valore"]

    return pd.DataFrame(
        {
            "date": pd.to_datetime(raw["Data"]),
            "description": raw["Descrizione"],
            "value": valore.abs(),
            "type": type_from_sign(valore),
        }
    )
