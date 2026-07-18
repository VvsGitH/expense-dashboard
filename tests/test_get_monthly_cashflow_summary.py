import pandas as pd
import pytest

import db
from db import TRANSACTION_COLUMNS
from domain import transfers
from service import get_monthly_cashflow_summary


def _insert(conn, *, date, description, value, bank, type_, upload_id="up-1"):
    row = pd.DataFrame(
        [
            {
                "date": date,
                "description": description,
                "value": value,
                "bank": bank,
                "type": type_,
                "upload_id": upload_id,
                "uploaded_at": "2024-01-01T00:00:00+00:00",
                "source_filename": "test.xlsx",
            }
        ],
        columns=TRANSACTION_COLUMNS,
    )
    db.insert_transactions(conn, row)


def _seed_three_months(conn):
    """Jan/Feb/Mar 2024: income [1000, 1000, 1000], expense [100, 200, 300]."""
    _insert(conn, date="2024-01-05", description="Stipendio", value=1000.0, bank="poste", type_="income")
    _insert(conn, date="2024-01-10", description="Farmacia", value=100.0, bank="poste", type_="expense")
    _insert(conn, date="2024-02-05", description="Stipendio", value=1000.0, bank="poste", type_="income")
    _insert(conn, date="2024-02-10", description="Spesa", value=200.0, bank="poste", type_="expense")
    _insert(conn, date="2024-03-05", description="Stipendio", value=1000.0, bank="poste", type_="income")
    _insert(conn, date="2024-03-10", description="Bar", value=300.0, bank="poste", type_="expense")


def _seed_four_months(conn):
    """Jan/Feb/Mar/Apr 2024: income [1000, 1000, 1000, 9000], expense [100, 200, 300, 1000]."""
    _seed_three_months(conn)
    _insert(conn, date="2024-04-05", description="Bonus", value=9000.0, bank="poste", type_="income")
    _insert(conn, date="2024-04-10", description="Regalo costoso", value=1000.0, bank="poste", type_="expense")


def test_computes_mean_and_median_of_monthly_income_and_expense(conn):
    _seed_four_months(conn)

    summary = get_monthly_cashflow_summary(conn=conn, today=pd.Timestamp("2024-06-15"))

    assert summary.income.mean == pytest.approx(3000.0)
    assert summary.income.median == pytest.approx(1000.0)
    assert summary.expense.mean == pytest.approx(400.0)
    assert summary.expense.median == pytest.approx(250.0)


def test_difference_is_computed_as_its_own_monthly_series(conn):
    _seed_four_months(conn)

    summary = get_monthly_cashflow_summary(conn=conn, today=pd.Timestamp("2024-06-15"))

    # Monthly differences: 900, 800, 700, 8000 -> median 850.
    naive_median = summary.income.median - summary.expense.median  # 1000 - 250 = 750
    assert summary.difference.median == pytest.approx(850.0)
    assert summary.difference.median != pytest.approx(naive_median)
    # Mean is linear, so it does coincide with mean(income) - mean(expense) either way.
    assert summary.difference.mean == pytest.approx(summary.income.mean - summary.expense.mean)


def test_excludes_cross_bank_transfer_pairs(conn):
    _insert(conn, date="2024-01-05", description="Farmacia", value=50.0, bank="poste", type_="expense")
    _insert(conn, date="2024-01-10", description="Stipendio", value=1500.0, bank="poste", type_="income")
    _insert(conn, date="2024-02-01", description="Spesa", value=30.0, bank="bbva", type_="expense")
    _insert(conn, date="2024-02-15", description="Rimborso", value=200.0, bank="poste", type_="income")
    # Cross-bank transfer pair (same amount, different bank, within 7 days) — must be excluded.
    _insert(conn, date="2024-03-05", description="Giroconto verso BBVA", value=100.0, bank="poste", type_="expense")
    _insert(conn, date="2024-03-08", description="Giroconto da Poste", value=100.0, bank="bbva", type_="income")
    # Genuine March movements, not part of the transfer.
    _insert(conn, date="2024-03-10", description="Bar", value=20.0, bank="poste", type_="expense")
    _insert(conn, date="2024-03-12", description="Regalo", value=300.0, bank="poste", type_="income")
    transfers.rebuild_cache(conn)

    summary = get_monthly_cashflow_summary(conn=conn, today=pd.Timestamp("2024-06-15"))

    # Monthly income (transfer excluded): 1500, 200, 300 -> mean 666.67, median 300.
    assert summary.income.mean == pytest.approx(2000.0 / 3.0)
    assert summary.income.median == pytest.approx(300.0)
    # Monthly expense (transfer excluded): 50, 30, 20 -> mean 33.33, median 30.
    assert summary.expense.mean == pytest.approx(100.0 / 3.0)
    assert summary.expense.median == pytest.approx(30.0)


def test_excludes_current_month_from_the_calculation(conn):
    _seed_three_months(conn)
    _insert(conn, date="2024-04-05", description="Bonus enorme", value=999999.0, bank="poste", type_="income")
    _insert(conn, date="2024-04-10", description="Spesa enorme", value=999999.0, bank="poste", type_="expense")

    summary = get_monthly_cashflow_summary(conn=conn, today=pd.Timestamp("2024-04-15"))

    assert summary.income.mean == pytest.approx(1000.0)
    assert summary.income.median == pytest.approx(1000.0)
    assert summary.expense.mean == pytest.approx(200.0)
    assert summary.expense.median == pytest.approx(200.0)
    assert summary.difference.mean == pytest.approx(800.0)
    assert summary.difference.median == pytest.approx(800.0)


def test_returns_none_when_date_range_covers_less_than_a_calendar_month(conn):
    _seed_three_months(conn)

    summary = get_monthly_cashflow_summary(
        conn=conn, date_from="2024-01-01", date_to="2024-01-20", today=pd.Timestamp("2024-06-15")
    )

    assert summary is None


def test_duration_check_is_skipped_when_only_one_side_of_the_range_is_set(conn):
    _seed_three_months(conn)

    summary = get_monthly_cashflow_summary(
        conn=conn, date_from="2024-01-01", date_to=None, today=pd.Timestamp("2024-06-15")
    )

    assert summary is not None


def test_returns_none_when_there_are_no_transactions(conn):
    summary = get_monthly_cashflow_summary(conn=conn, today=pd.Timestamp("2024-06-15"))

    assert summary is None


def test_returns_none_when_only_current_month_has_data(conn):
    _insert(conn, date="2024-04-05", description="Stipendio", value=1000.0, bank="poste", type_="income")
    _insert(conn, date="2024-04-10", description="Spesa", value=100.0, bank="poste", type_="expense")

    summary = get_monthly_cashflow_summary(conn=conn, today=pd.Timestamp("2024-04-15"))

    assert summary is None
