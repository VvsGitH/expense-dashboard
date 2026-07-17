# 05 — Dashboard: sezione grafico a barre mensile

**What to build:** Nella pagina "Dashboard", una sezione con un grafico a barre mostra Entrate e Uscite aggregate mensilmente, al netto dei Trasferimenti cross-bank, con un proprio filtro di range di date indipendente dalle altre sezioni.

**Blocked by:** 01, 02

**Status:** ready-for-agent

- [ ] Il grafico a barre mostra Entrate e Uscite aggregate per mese
- [ ] I totali mensili escludono le Transazioni classificate come Trasferimento cross-bank
- [ ] Il range di date del grafico è configurabile ed è indipendente dai filtri delle altre sezioni della dashboard
- [ ] Test automatici verificano che `get_monthly_totals` escluda correttamente i Trasferimenti e rispetti il proprio range di date
