# 04 — Dashboard: sezione tabella con filtri

**What to build:** Nella pagina "Dashboard", una sezione tabella mostra tutte le Transazioni presenti nel DB (Entrate e Uscite, inclusi eventuali Trasferimenti cross-bank — è una vista di ispezione dei dati grezzi), filtrabile per range di date, Tipologia (solo Entrate/solo Uscite/entrambe), Banca, e testo libero nella descrizione. I filtri di questa sezione sono indipendenti da quelli delle altre due sezioni della dashboard.

**Blocked by:** 01

**Status:** done

- [x] La sezione tabella mostra tutte le Transazioni presenti nel DB, Trasferimenti cross-bank inclusi
- [x] È filtrabile per range di date
- [x] È filtrabile per Tipologia (solo Entrate, solo Uscite, entrambe)
- [x] È filtrabile per Banca
- [x] È filtrabile per testo libero nella descrizione
- [x] I filtri di questa sezione sono indipendenti da quelli delle altre sezioni della dashboard
- [x] Test automatici verificano `get_transactions` per ciascun filtro singolarmente e in combinazione

## Comments

Implementato con TDD sul seam `service.get_transactions` (9 test, tutti verdi): filtro per range date, Tipologia, Banca e testo descrizione, singolarmente e in combinazione, inclusi i Trasferimenti cross-bank (vista di ispezione sui dati grezzi). Sezione "Tabella transazioni" aggiunta alla pagina Dashboard con filtri propri (`table_*` keys), indipendenti dalle sezioni future (grafico a barre, grafici a torta). Verificato end-to-end in browser: upload → tabella filtrata → annullamento caricamento.

Code review a due assi: Standards senza violazioni hard (solo judgement call su due dizionari label/enum con convenzioni di chiave leggermente diverse, risolto armonizzando entrambi su `None` come sentinella "nessun filtro"). Spec ha trovato un bug reale: il filtro descrizione passava l'input a `str.contains` con `regex=True` (default pandas), quindi caratteri come parentesi nella descrizione (comuni nei movimenti bancari, es. "POS (Conad)") mandavano in errore la query invece di fare match letterale — corretto con `regex=False` e aggiunto un test di non-regressione.
