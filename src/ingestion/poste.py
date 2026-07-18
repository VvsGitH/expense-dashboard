import pandas as pd

from ingestion._shared import type_from_sign

SHEET_NAME = "ListaMovimenti"
HEADER_ROW = 2


def parse(file) -> pd.DataFrame:
    raw = pd.read_excel(
        file, sheet_name=SHEET_NAME, header=HEADER_ROW, decimal=",", thousands="."
    )
    values = raw["Accrediti (euro)"].fillna(0) - raw["Addebiti (euro)"].fillna(0)

    return pd.DataFrame(
        {
            "date": pd.to_datetime(raw["Data Valuta"]),
            "description": raw["Descrizione operazioni"],
            "value": values.abs(),
            "type": type_from_sign(values),
        }
    )
