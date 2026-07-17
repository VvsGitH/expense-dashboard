# 07 — Migrazione storico e ritiro del notebook

**What to build:** Uno script one-off importa i tre file Excel storici (`data/movimenti_poste.xlsx`, `data/movimenti_bbva.xlsx`, `data/movimenti_others.xlsx`) nel DB riusando le stesse funzioni di ingestion della webapp, escludendo la Transazione TFR nota (identificata per data/importo/descrizione, non per indice di riga come nel notebook attuale). Una volta verificato che i totali mostrati in dashboard sui dati migrati coincidono con quelli del notebook attuale, il notebook viene rimosso dal repository.

**Blocked by:** 01, 02, 03, 04, 05, 06, e `project-refactor/01-riorganizzazione-struttura-cartelle` (lo script scrive direttamente sulla nuova struttura, in `scripts/migrate_history.py`)

**Status:** ready-for-agent

- [ ] Lo script di migrazione (`scripts/migrate_history.py`) importa i tre file storici riusando `ingest_file`
- [ ] La Transazione TFR nota viene esclusa durante la migrazione, identificata per data/importo/descrizione
- [ ] I totali di spese/entrate/Trasferimenti prodotti dalla dashboard sui dati migrati coincidono con quelli prodotti dal notebook attuale sullo stesso range di date
- [ ] `src/notebook.ipynb` viene rimosso dal repository
- [ ] Viene introdotto un file di manifest delle dipendenze (`requirements.txt` o `pyproject.toml`) con le dipendenze effettivamente usate (`pandas`, `openpyxl`, `rapidfuzz`, `streamlit`, `pytest`, e `matplotlib` se ancora in uso)
