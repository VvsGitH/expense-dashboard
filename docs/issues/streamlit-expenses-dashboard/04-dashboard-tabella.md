# 04 — Dashboard: sezione tabella con filtri

**What to build:** Nella pagina "Dashboard", una sezione tabella mostra tutte le Transazioni presenti nel DB (Entrate e Uscite, inclusi eventuali Trasferimenti cross-bank — è una vista di ispezione dei dati grezzi), filtrabile per range di date, Tipologia (solo Entrate/solo Uscite/entrambe), Banca, e testo libero nella descrizione. I filtri di questa sezione sono indipendenti da quelli delle altre due sezioni della dashboard.

**Blocked by:** 01

**Status:** ready-for-agent

- [ ] La sezione tabella mostra tutte le Transazioni presenti nel DB, Trasferimenti cross-bank inclusi
- [ ] È filtrabile per range di date
- [ ] È filtrabile per Tipologia (solo Entrate, solo Uscite, entrambe)
- [ ] È filtrabile per Banca
- [ ] È filtrabile per testo libero nella descrizione
- [ ] I filtri di questa sezione sono indipendenti da quelli delle altre sezioni della dashboard
- [ ] Test automatici verificano `get_transactions` per ciascun filtro singolarmente e in combinazione
