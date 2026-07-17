import pandas as pd
import pytest

from app import db


@pytest.fixture
def conn(tmp_path):
    connection = db.get_connection(tmp_path / "test.db")
    yield connection
    connection.close()


def _write_excel(path, sheet_name, header_row, rows: pd.DataFrame, startcol=0):
    with pd.ExcelWriter(path) as writer:
        rows.to_excel(
            writer, sheet_name=sheet_name, startrow=header_row, startcol=startcol, index=False
        )
    return path


def make_poste_file(path, rows: dict):
    """rows: {'date': [...], 'description': [...], 'addebiti': [...], 'accrediti': [...]}"""
    df = pd.DataFrame(
        {
            "Data Contabile": rows["date"],
            "Data Valuta": rows["date"],
            "Addebiti (euro)": rows["addebiti"],
            "Accrediti (euro)": rows["accrediti"],
            "Descrizione operazioni": rows["description"],
        }
    )
    return _write_excel(path, "ListaMovimenti", header_row=2, rows=df)


def make_bbva_file(path, rows: dict):
    """rows: {'date': [dd/mm/yyyy strings], 'description': [...], 'importo': [...]}"""
    n = len(rows["date"])
    df = pd.DataFrame(
        {
            "Data valuta": rows["date"],
            "Data": rows["date"],
            "Concetto": [""] * n,
            "Movimento": [""] * n,
            "Importo": rows["importo"],
            "Valuta": ["EUR"] * n,
            "Disponibile": [0] * n,
            "Valuta.1": ["EUR"] * n,
            "Osservazioni": rows["description"],
        }
    )
    return _write_excel(path, "Informe BBVA", header_row=4, rows=df, startcol=1)


def make_others_file(path, rows: dict):
    """rows: {'date': [...], 'description': [...], 'valore': [...]}"""
    df = pd.DataFrame(
        {
            "Data": rows["date"],
            "Valore": rows["valore"],
            "Descrizione": rows["description"],
        }
    )
    return _write_excel(path, "Movimenti", header_row=4, rows=df)


@pytest.fixture
def poste_file(tmp_path):
    return make_poste_file(
        tmp_path / "poste.xlsx",
        {
            "date": [pd.Timestamp(2024, 1, 5), pd.Timestamp(2024, 1, 10)],
            "description": ["Farmacia Rossi", "Stipendio Gennaio"],
            "addebiti": [50.00, None],
            "accrediti": [None, 1500.00],
        },
    )


@pytest.fixture
def bbva_file(tmp_path):
    return make_bbva_file(
        tmp_path / "bbva.xlsx",
        {
            "date": ["05/01/2024", "10/01/2024"],
            "description": ["Supermercato Conad", "Bonifico ricevuto"],
            "importo": [-30.00, 200.00],
        },
    )


@pytest.fixture
def others_file(tmp_path):
    return make_others_file(
        tmp_path / "others.xlsx",
        {
            "date": [pd.Timestamp(2024, 1, 5), pd.Timestamp(2024, 1, 10)],
            "description": ["Farmacia", "Rimborso"],
            "valore": [-20.00, 100.00],
        },
    )
