import pandas as pd

from app.domain.enums import TransactionType


def type_from_sign(values: pd.Series) -> pd.Series:
    """Maps a signed amount Series to TransactionType.INCOME/EXPENSE values."""
    return values.apply(
        lambda x: TransactionType.INCOME.value if x > 0 else TransactionType.EXPENSE.value
    )
