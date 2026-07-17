import pandas as pd

MONTHLY_TOTALS_COLUMNS = {"income": "Entrate", "expense": "Uscite"}


def monthly_totals_chart_data(monthly_totals: list[dict]) -> pd.DataFrame:
    """Shapes get_monthly_totals's output into a month-indexed DataFrame ready for a bar chart."""
    return (
        pd.DataFrame(monthly_totals, columns=["month", "income", "expense"])
        .rename(columns=MONTHLY_TOTALS_COLUMNS)
        .set_index("month")
    )
