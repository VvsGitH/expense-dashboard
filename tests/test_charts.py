from app.domain.charts import CATEGORY_COLORS, category_breakdown_chart_data, category_colors, monthly_totals_chart_data


def test_monthly_totals_chart_data_shapes_data_for_bar_chart():
    monthly_totals = [
        {"month": "2024-01", "income": 1500.0, "expense": 50.0},
        {"month": "2024-02", "income": 200.0, "expense": 30.0},
    ]

    result = monthly_totals_chart_data(monthly_totals)

    assert list(result.index) == ["2024-01", "2024-02"]
    assert list(result.columns) == ["Entrate", "Uscite"]
    assert result.loc["2024-01", "Entrate"] == 1500.0
    assert result.loc["2024-01", "Uscite"] == 50.0


def test_monthly_totals_chart_data_handles_empty_input():
    result = monthly_totals_chart_data([])

    assert result.empty


def test_category_breakdown_chart_data_shapes_data_for_pie_chart():
    breakdown = [
        {"category": "spesa", "value": 80.0},
        {"category": "salute", "value": 50.0},
    ]

    result = category_breakdown_chart_data(breakdown)

    assert list(result.index) == ["spesa", "salute"]
    assert result.loc["spesa"] == 80.0
    assert result.loc["salute"] == 50.0


def test_category_breakdown_chart_data_handles_empty_input():
    result = category_breakdown_chart_data([])

    assert result.empty


def test_category_colors_maps_known_categories():
    result = category_colors(["spesa", "salute"])

    assert result == [CATEGORY_COLORS["spesa"], CATEGORY_COLORS["salute"]]


def test_category_colors_falls_back_to_other_for_unknown_category():
    result = category_colors(["not-a-real-category"])

    assert result == [CATEGORY_COLORS["other"]]
