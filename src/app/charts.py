import pandas as pd

MONTHLY_TOTALS_COLUMNS = {"income": "Entrate", "expense": "Uscite"}

CATEGORY_COLORS = {
    "salute": "#e41a1c",
    "casa": "#377eb8",
    "spesa": "#4daf4a",
    "shopping": "#984ea3",
    "hobby": "#ff7f00",
    "viaggi": "#ffff33",
    "fitness": "#a65628",
    "auto": "#f781bf",
    "tasse": "#4012bd",
    "contanti": "#7f66c2",
    "other": "#bdbdbd",
}


def monthly_totals_chart_data(monthly_totals: list[dict]) -> pd.DataFrame:
    """Shapes get_monthly_totals's output into a month-indexed DataFrame ready for a bar chart."""
    return (
        pd.DataFrame(monthly_totals, columns=["month", "income", "expense"])
        .rename(columns=MONTHLY_TOTALS_COLUMNS)
        .set_index("month")
    )


def category_breakdown_chart_data(breakdown: list[dict]) -> pd.Series:
    """Shapes get_category_breakdown's output into a category-indexed Series ready for a pie chart."""
    return pd.DataFrame(breakdown, columns=["category", "value"]).set_index("category")["value"]


def category_colors(categories) -> list[str]:
    """Maps an iterable of category names to their pie-chart colors, falling back to 'other'."""
    return [CATEGORY_COLORS.get(category, CATEGORY_COLORS["other"]) for category in categories]
