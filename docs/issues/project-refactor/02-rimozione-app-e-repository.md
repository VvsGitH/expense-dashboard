# 02 — Rimozione cartella `app` e `repository`: struttura flat sotto `src/`

**What to build:** Appiattire `src/app/` eliminando il livello di package `app` — tutti i moduli (`domain/`, `ingestion/`, `pages/`, `service.py`, `router.py`) vivono direttamente sotto `src/`, importati senza prefisso `app.`. Eliminare anche la cartella `repository/`, spostando `db.py` come modulo flat sotto `src/` insieme agli altri: il nome "repository" lasciava intendere un pattern architetturale (Repository) che il progetto non adotta, coerentemente con ADR-0002 che esclude esplicitamente strati di astrazione sul DB. Refactor puramente meccanico: nessun comportamento dell'app cambia, la suite di test esistente è la rete di sicurezza.

**Blocked by:** Nessuno — può partire subito (il ticket 01, che ha introdotto la struttura `app/domain/repository/pages` ora superata, è già `done`).

**Status:** done

- [x] `src/domain/`, `src/ingestion/`, `src/pages/` esistono al posto di `src/app/domain/`, `src/app/ingestion/`, `src/app/pages/` (spostati con `git mv`)
- [x] `src/db.py` esiste al posto di `src/app/repository/db.py`; la cartella `repository/` non esiste più
- [x] `src/service.py` e `src/router.py` vivono direttamente sotto `src/`
- [x] La cartella `src/app/` (incluso `src/app/__init__.py`) non esiste più
- [x] Tutti gli import in `src/`, `scripts/migrate_history.py` e `tests/` usano lo schema flat (`domain.x`, `ingestion.x`, `service`, `db`) senza prefisso `app.`
- [x] `router.py` non contiene più il fixup manuale di `sys.path` (il walk-up per trovare la cartella `app`) — non più necessario perché Streamlit aggiunge automaticamente la directory dello script (`src/`) a `sys.path`
- [x] `db.py` calcola `DEFAULT_DB_PATH` con un helper inline che risale le directory alla ricerca di un marker `.git`, invece dell'indice hardcoded `parents[3]`
- [x] `README.md` riflette la nuova struttura del progetto e il nuovo comando di avvio (`streamlit run src/router.py`), senza più menzionare il fixup di `sys.path`
- [x] Il ticket 01 ha un commento in fondo, sotto `## Comments`, che rimanda a questo ticket spiegando perché la motivazione del nome `repository/` non vale più
- [x] La suite di test esistente (45 test, non 42 come nel ticket 01 — evidentemente ne sono stati aggiunti nel frattempo) passa invariata dopo il refactor, senza necessità di nuovi test
