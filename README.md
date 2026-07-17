# Extract Expenses

Traccia e categorizza i movimenti bancari personali (Poste, BBVA, altri conti) e li presenta in una dashboard Streamlit di monitoraggio spese/entrate.

Vedi [`CONTEXT.md`](CONTEXT.md) per il linguaggio di dominio e `docs/adr/` per le decisioni architetturali.

## Setup

In un terminale, dalla root del progetto:

```
python -m venv ./venv
./venv/Scripts/activate
pip install streamlit pandas matplotlib rapidfuzz openpyxl pytest
```

## Avviare la web application

```
streamlit run src/app/router.py
```

`router.py` è l'entrypoint: registra le pagine (`Dashboard`, `Carica dati`) tramite `st.Page`/`st.navigation` e si occupa del fixup di `sys.path` necessario per gli import interni (`from app...`).

## Eseguire i test

```
pytest
```

## Struttura del progetto

```
src/app/
  domain/       # enums, categorizzazione, trasferimenti cross-bank, dati per i grafici
  repository/   # accesso a SQLite (db.py)
  ingestion/    # parser per i formati Excel di ciascuna banca
  pages/        # pagine Streamlit (dashboard.py, carica_dati.py)
  service.py    # seam applicativo testato, orchestration tra repository/domain/ingestion
  router.py     # entrypoint Streamlit
tests/          # suite di test, piatta
```
