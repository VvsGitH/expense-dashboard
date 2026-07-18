import pandas as pd

from ingestion._shared import type_from_sign

SHEET_NAME = "Informe BBVA"
HEADER_ROW = 4
USECOLS = "B:J"


def parse(file) -> pd.DataFrame:
    raw = pd.read_excel(
        file,
        sheet_name=SHEET_NAME,
        header=HEADER_ROW,
        usecols=USECOLS,
        decimal=",",
        thousands=".",
    )
    importo = raw["Importo"]

    return pd.DataFrame(
        {
            "date": pd.to_datetime(
                raw["Data valuta"], format="%d/%m/%Y", errors="coerce"
            ),
            "description": raw["Osservazioni"],
            "value": importo.abs(),
            "type": type_from_sign(importo),
        }
    )
