from enum import Enum


class Bank(Enum):
    POSTE = "poste"
    BBVA = "bbva"
    OTHERS = "others"


class TransactionType(Enum):
    EXPENSE = "expense"
    INCOME = "income"
