# Extract Expenses

Traccia e categorizza i movimenti bancari personali (Poste, BBVA, altri conti) e li presenta in una dashboard Streamlit di monitoraggio spese/entrate.

Vedi [`CONTEXT.md`](CONTEXT.md) per il linguaggio di dominio e `docs/adr/` per le decisioni architetturali.

## Setup

In un terminale, dalla root del progetto:

```
python -m venv ./venv
./venv/Scripts/activate
pip install -r requirements.txt
```

## Avviare la web application

```
streamlit run src/router.py
```

`router.py` è l'entrypoint: registra le pagine (`Dashboard`, `Carica dati`) tramite `st.Page`/`st.navigation`.

## Eseguire i test

```
pytest
```

## Migrazione dello storico (una tantum)

Per importare i tre file Excel storici (`data/movimenti_*.xlsx`) nel DB riusando la
stessa pipeline di ingestion della webapp — escludendo la nota transazione TFR:

```
python scripts/migrate_history.py
```

## Struttura del progetto

```
src/
  domain/       # enums, categorizzazione, trasferimenti cross-bank, dati per i grafici
  ingestion/    # parser per i formati Excel di ciascuna banca
  pages/        # pagine Streamlit (dashboard.py, carica_dati.py)
  db.py         # accesso a SQLite
  service.py    # seam applicativo testato, orchestration tra db/domain/ingestion
  router.py     # entrypoint Streamlit
scripts/        # utility one-off (migrate_history.py)
tests/          # suite di test, piatta
```
