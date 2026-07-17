# 06 — Dashboard: sezione grafici a torta per categoria

**What to build:** Nella pagina "Dashboard", una sezione con grafici a torta mostra la ripartizione delle Uscite per Categoria (calcolata al volo dalle regole di fuzzy-matching correnti), al netto dei Trasferimenti cross-bank, con un proprio filtro di range di date indipendente dalle altre sezioni.

**Blocked by:** 01, 02

**Status:** ready-for-agent

- [ ] Le regole di categorizzazione (`EXP_CATEGORIES` e la funzione di scoring fuzzy) sono portate in un modulo importabile, riusando la logica già presente nel notebook
- [ ] La Categoria di ogni Uscita è calcolata al volo al momento della query, non persistita nel DB
- [ ] I grafici a torta mostrano la ripartizione delle Uscite per Categoria nel range di date selezionato
- [ ] Le Transazioni classificate come Trasferimento cross-bank sono escluse dal calcolo della ripartizione
- [ ] Il range di date dei grafici a torta è configurabile ed è indipendente dai filtri delle altre sezioni della dashboard
- [ ] Una modifica alle regole di categorizzazione nel modulo Python si riflette immediatamente in `get_category_breakdown` (riavviando il dev server), senza bisogno di ricalcolo esplicito
- [ ] Test automatici verificano `get_category_breakdown` rispetto a regole di categorizzazione note e al proprio range di date
