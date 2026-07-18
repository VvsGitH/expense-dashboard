# 01 — Flusso di cassa mensile

**What to build:** Nella pagina "Dashboard", sotto il grafico a barre della sezione "Entrate e Uscite mensili", un blocco "Flusso di cassa mensile" mostra media e mediana mensile di Entrate, Uscite e Differenza (Entrate − Uscite), calcolate mese per mese sullo stesso range di date già configurato per quella sezione (`bar_date_from`/`bar_date_to`), al netto dei Trasferimenti cross-bank e del mese solare in corso. Se il periodo non è sufficiente, mostra un messaggio invece dei numeri.

**Blocked by:** nessuno (estende `docs/issues/streamlit-expenses-dashboard/05-dashboard-grafico-a-barre.md`, già `done`)

**Status:** done

- [x] Nuova funzione `service.get_monthly_cashflow_summary(date_from, date_to)` che ritorna un dataclass `CashflowSummary` (campi `income`, `expense`, `difference`, ciascuno un dataclass `MonthlyStat` con `mean` e `median`), oppure `None` se il calcolo non è possibile
- [x] Il calcolo si appoggia alla stessa aggregazione mensile usata da `get_monthly_totals`, escludendo le Transazioni che sono gambe di un Trasferimento cross-bank
- [x] Il mese solare corrente (data di sistema), se presente tra i mesi aggregati, viene escluso dal calcolo
- [x] La Differenza mensile è calcolata come propria serie (Entrate del mese − Uscite dello stesso mese), non come sottrazione delle medie/mediane già calcolate di Entrate e Uscite
- [x] Ritorna `None` quando `date_from` e `date_to` sono entrambi impostati e coprono meno di un mese di calendario esatto (`pd.Timestamp(date_from) + pd.DateOffset(months=1) > pd.Timestamp(date_to)`)
- [x] Ritorna `None` anche quando, escluso il mese corrente, non rimane alcun mese di dati (nessuna Transazione nel periodo, o Transazioni presenti solo nel mese corrente)
- [x] Nella pagina Dashboard, il blocco usa `bar_date_from`/`bar_date_to` già esistenti, senza filtri propri e senza dipendere dai filtri della sezione tabella o dei grafici a torta
- [x] Quando `get_monthly_cashflow_summary` ritorna un valore: tre colonne (Entrate / Uscite / Differenza), ciascuna con due `st.metric` (Media, Mediana), formattati come `"€ {value:.2f}"`
- [x] Quando ritorna `None`: messaggio informativo "Intervallo troppo piccolo per calcolare il flusso di cassa mensile" al posto dei numeri
- [x] La sotto-sezione ha l'etichetta "Flusso di cassa mensile"
- [x] `CONTEXT.md` include una nuova voce di glossario per "Flusso di cassa mensile"
- [x] Test automatici in `tests/test_get_monthly_cashflow_summary.py` coprono: calcolo media/mediana di Entrate e Uscite, calcolo indipendente della Differenza come propria serie (con un caso in cui `mediana(differenza) != mediana(entrate) - mediana(uscite)`), esclusione dei Trasferimenti cross-bank, esclusione del mese corrente, `None` per periodo < 1 mese di calendario, `None` per assenza di dati/mesi dopo l'esclusione del mese corrente

## Comments

Implementato con TDD sul seam `service.get_monthly_cashflow_summary` (8 test, tutti verdi), che riusa la stessa aggregazione mensile di `get_monthly_totals` tramite un nuovo helper condiviso `_monthly_income_expense` (estratto per evitare duplicazione). Differenza calcolata come serie mensile propria (Entrate − Uscite per mese), verificato con un caso in cui la mediana della differenza diverge dalla sottrazione naive delle mediane già calcolate. Mese corrente escluso via un parametro `today` iniettabile (default data di sistema), che rende il comportamento testabile senza dipendere dall'orologio reale. Verificato end-to-end in browser sul DB reale: blocco con valori coerenti sotto il grafico a barre, e messaggio "Intervallo troppo piccolo..." quando il filtro data è ristretto a meno di un mese.

Code review a due assi: Standards ha segnalato tre judgement call, tutti applicati — rinominato il dataclass `Stat` in `MonthlyStat` (nome più onesto in un modulo con altri dataclass simili), estratta la conversione `.isoformat()` di `bar_date_from`/`bar_date_to` in variabili locali riusate da entrambe le chiamate di servizio (prima duplicata), e fattorizzato il seed di quattro mesi condiviso tra due test (prima duplicato). Spec ha trovato una violazione reale: la sezione usava `st.subheader` invece della semplice etichetta testuale richiesta dalla spec ("nessun header di secondo livello proprio") — corretto con `st.markdown("**Flusso di cassa mensile**")`, verificato che l'anchor-link automatico di Streamlit (proprio degli header) sia sparito e i valori restino invariati.
