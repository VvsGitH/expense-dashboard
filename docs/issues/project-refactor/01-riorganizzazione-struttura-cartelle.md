# 01 — Riorganizzazione struttura cartelle del progetto

**What to build:** Riorganizzare i file di `src/app/` in un'alberatura di cartelle intuitiva, standard e prevedibile — `domain/`, `repository/`, `ingestion/`, `pages/` — introducendo un entrypoint Streamlit esplicito basato su `st.Page`/`st.navigation` (vedi ADR-0003) al posto della cartella `pages/` magica attuale. Refactor puramente meccanico: nessun comportamento dell'app cambia, la suite di test esistente è la rete di sicurezza.

**Blocked by:** Nessuno — deve però completarsi prima del ticket 07 (`streamlit-expenses-dashboard`), che scriverà direttamente sulla nuova struttura.

**Status:** ready-for-agent

- [ ] `src/app/domain/` contiene `enums.py`, `transfers.py`, `categorization.py`, `charts.py` (spostati dalla radice di `src/app/`)
- [ ] `src/app/repository/` contiene `db.py` (spostato dalla radice di `src/app/`) — solo posizione/nome della cartella, nessun nuovo pattern Repository (resta coerente con ADR-0002: niente ORM, niente strato di astrazione)
- [ ] `src/app/ingestion/` resta invariato (`_shared.py`, `bbva.py`, `others.py`, `poste.py`)
- [ ] `src/app/service.py` resta un singolo file flat alla radice di `src/app/`, non spostato in `domain/` — resta distinto come l'unico seam testato
- [ ] Tutte le pagine Streamlit vivono uniformemente in `src/app/pages/`, con nomi in snake_case e senza prefisso numerico (`dashboard.py`, `carica_dati.py`)
- [ ] `src/app/router.py` è il nuovo entrypoint Streamlit: costruisce le pagine con `st.Page(...)` e chiama `st.navigation([...]).run()`, nell'ordine desiderato (vedi ADR-0003)
- [ ] Il fixup di `sys.path` (individuare la cartella `app` e aggiungerla a `sys.path`) vive solo in `router.py`, rimosso dai singoli file pagina
- [ ] Viene creata la cartella `scripts/` (sibling di `src/app/`), pronta per lo script di migrazione del ticket 07
- [ ] `tests/` resta piatta, nessuna riorganizzazione in sottocartelle
- [ ] Tutti gli import esistenti (in `src/app/` e `tests/`) sono aggiornati ai nuovi percorsi dei moduli
- [ ] La suite di test esistente (42 test) passa invariata dopo il refactor, senza necessità di nuovi test
