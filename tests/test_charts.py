from app.charts import monthly_totals_chart_data


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
