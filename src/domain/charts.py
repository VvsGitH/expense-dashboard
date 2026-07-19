import pandas as pd

MONTHLY_TOTALS_COLUMNS = {"income": "Entrate", "expense": "Uscite"}
CATEGORY_TOTAL_COLUMN = "Totale (€)"

CATEGORY_COLORS = {
    "salute": "#e41a1c",
    "casa": "#377eb8",
    "spesa": "#4daf4a",
    "shopping": "#984ea3",
    "hobby": "#ff7f00",
    "fitness": "#a65628",
    "auto": "#f781bf",
    "viaggi": "#a68f00",
    "tasse": "#00917f",
    "contanti": "#7f66c2",
    "other": "#c58e50",
}


def _monthly_totals_frame(monthly_totals: list[dict]) -> pd.DataFrame:
    """Shapes get_monthly_totals's output into a month-indexed DataFrame with raw income/expense."""
    return pd.DataFrame(monthly_totals, columns=["month", "income", "expense"]).set_index("month")


def monthly_totals_chart_data(monthly_totals: list[dict]) -> pd.DataFrame:
    """Shapes get_monthly_totals's output into a month-indexed DataFrame ready for a bar chart."""
    return _monthly_totals_frame(monthly_totals).rename(columns=MONTHLY_TOTALS_COLUMNS)


def savings_trend_chart_data(monthly_totals: list[dict]) -> pd.DataFrame:
    """Shapes get_monthly_totals's output into a month-indexed DataFrame ready for a line chart.

    "Differenza mensile" is income minus expense per month; "Risparmio teorico
    accumulato" is its running cumulative sum, restarting from zero at the
    first month present in the input (see docs/adr/0004).
    """
    monthly = _monthly_totals_frame(monthly_totals)
    difference = monthly["income"] - monthly["expense"]
    return pd.DataFrame(
        {
            "Differenza mensile": difference,
            "Risparmio teorico accumulato": difference.cumsum(),
        }
    )


def category_breakdown_chart_data(breakdown: list[dict]) -> pd.Series:
    """Shapes get_category_breakdown's output into a category-indexed Series ready for a bar chart."""
    return pd.DataFrame(breakdown, columns=["category", "value"]).set_index("category")["value"]


def category_breakdown_table_data(breakdown: list[dict]) -> pd.DataFrame:
    """Shapes get_category_breakdown's output into a category-indexed table with totals and share of total."""
    totals = category_breakdown_chart_data(breakdown)
    if totals.empty:
        return pd.DataFrame()
    return pd.DataFrame(
        {
            CATEGORY_TOTAL_COLUMN: totals,
            "Percentuale": totals / totals.sum() * 100,
        }
    ).sort_values(CATEGORY_TOTAL_COLUMN, ascending=False)


def category_names() -> list[str]:
    """Returns the known category names, in their canonical (validated-palette) order."""
    return list(CATEGORY_COLORS)


def category_colors(categories) -> list[str]:
    """Maps an iterable of category names to their bar-chart colors, falling back to 'other'."""
    return [CATEGORY_COLORS.get(category, CATEGORY_COLORS["other"]) for category in categories]
