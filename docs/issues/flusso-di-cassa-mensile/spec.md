Status: ready-for-agent

# Flusso di cassa mensile

## Problem Statement

Nella pagina "Dashboard", la sezione "Entrate e Uscite mensili" mostra oggi solo un grafico a barre con i totali mensili di Entrate e Uscite. Per farmi un'idea di quanto guadagno o spendo "in un mese tipico" devo guardare il grafico a occhio e fare il calcolo a mente, mese per mese — un esercizio lento e impreciso, soprattutto su periodi lunghi con molti mesi da confrontare. Non ho un modo rapido per vedere, in forma numerica, quali sono i valori medi e mediani di Entrate, Uscite e differenza (saldo) mensile nel periodo che sto guardando.

## Solution

Aggiungere, sotto il grafico a barre della sezione "Entrate e Uscite mensili", un blocco "Flusso di cassa mensile" che mostra media e mediana mensile di Entrate, Uscite e Differenza (Entrate − Uscite), calcolate mese per mese sullo stesso range di date già configurato per quella sezione (`bar_date_from`/`bar_date_to`), escludendo sempre il mese solare in corso (dati parziali, mese non ancora concluso). Se il periodo selezionato non è sufficiente a calcolare un valore sensato, il blocco mostra un messaggio esplicativo al posto dei numeri.

## User Stories

1. Come utente, voglio vedere la media mensile delle mie Entrate nel periodo che sto guardando, così da sapere quanto incasso tipicamente in un mese.
2. Come utente, voglio vedere la mediana mensile delle mie Entrate, così da avere un valore robusto rispetto a mesi con Entrate eccezionalmente alte o basse (es. bonus, rimborsi una tantum).
3. Come utente, voglio vedere la media mensile delle mie Uscite nel periodo che sto guardando, così da sapere quanto spendo tipicamente in un mese.
4. Come utente, voglio vedere la mediana mensile delle mie Uscite, così da avere un valore robusto rispetto a mesi con spese eccezionali (es. un grande acquisto).
5. Come utente, voglio vedere la media mensile della differenza tra Entrate e Uscite (il mio saldo/risparmio mensile), così da capire se sto tipicamente risparmiando o andando in rosso.
6. Come utente, voglio vedere la mediana mensile della differenza tra Entrate e Uscite, così da avere un valore robusto per lo stesso motivo.
7. Come utente, voglio che la differenza mensile sia calcolata mese per mese come propria serie indipendente (Entrate del mese meno Uscite dello stesso mese, poi media/mediana su quella serie), e non come sottrazione delle medie/mediane già calcolate di Entrate e Uscite, così che la mediana della differenza rifletta davvero l'andamento mese per mese e non un'approssimazione statisticamente scorretta.
8. Come utente, voglio che il mese solare in corso venga sempre escluso dal calcolo di media e mediana quando presente nei dati, così che un mese ancora incompleto (poche settimane di Entrate/Uscite) non falsi verso il basso i valori tipici mensili.
9. Come utente, voglio che il blocco "Flusso di cassa mensile" reagisca allo stesso filtro di date già presente nella sezione "Entrate e Uscite mensili" (`bar_date_from`/`bar_date_to`), così da vedere media e mediana coerenti con lo stesso periodo che sto già analizzando nel grafico a barre soprastante.
10. Come utente, voglio che questo blocco sia indipendente dai filtri della sezione tabella (Tipologia, Banca, testo descrizione) e da quelli della sezione grafici a torta, così che restringere la tabella a una singola Banca o a una parola chiave non alteri accidentalmente il flusso di cassa mensile che sto guardando.
11. Come utente, voglio che il calcolo escluda i Trasferimenti cross-bank (coerentemente con il grafico a barre soprastante), così che uno spostamento di denaro tra i miei conti non venga contato due volte come Entrata e Uscita reali.
12. Come utente, voglio che se il periodo selezionato è troppo breve per calcolare un valore mensile sensato (meno di un mese di calendario tra `bar_date_from` e `bar_date_to`), venga mostrato un messaggio che me lo spiega, invece di numeri fuorvianti calcolati su una manciata di giorni.
13. Come utente, voglio lo stesso messaggio anche quando, escluso il mese in corso, non rimane alcun mese completo di dati su cui calcolare media/mediana (es. range senza Transazioni, o Transazioni presenti solo nel mese in corso), così da avere un comportamento coerente in tutti i casi in cui il calcolo non è possibile.
14. Come utente, voglio che i valori mostrati siano espressi in Euro con due decimali (es. "€ 1234.50"), così da leggerli come importi monetari familiari senza dover fare conversioni mentali.
15. Come utente, voglio che i sei valori (media/mediana di Entrate, Uscite, Differenza) siano organizzati in modo leggibile a colpo d'occhio (una colonna per Entrate, una per Uscite, una per Differenza, ciascuna con Media e Mediana), così da poter confrontare rapidamente le tre grandezze.
16. Come utente, voglio che la sotto-sezione abbia un titolo chiaro, "Flusso di cassa mensile", che comunichi che si tratta sia di Entrate sia di Uscite (e del loro saldo), così da non dover indovinare cosa rappresentano i numeri.
17. Come sviluppatore, voglio che "Flusso di cassa mensile" sia un termine di dominio documentato in `CONTEXT.md`, così da avere un vocabolario condiviso per codice, UI e documentazione futura.
18. Come sviluppatore, voglio un livello di servizio testabile indipendente dalla UI Streamlit per questo calcolo, coerente con il resto dell'app, così da poter scrivere test automatici senza automazione del browser.

## Implementation Decisions

- **Seam unico**: una nuova funzione `service.get_monthly_cashflow_summary(date_from, date_to)`, seguendo lo stesso pattern delle altre funzioni di servizio della dashboard (`get_transactions`, `get_monthly_totals`, `get_category_breakdown`).
  - Si appoggia alla stessa base dati già usata da `get_monthly_totals` (aggregazione mensile di Entrate/Uscite al netto dei Trasferimenti cross-bank via `transfers.get_transfer_leg_ids`), evitando di duplicare la logica di esclusione dei Trasferimenti.
  - Esclude dal calcolo il mese solare corrente (determinato dalla data di sistema, non dalla data massima presente nei dati), se presente tra i mesi aggregati.
  - Calcola, sui mesi rimanenti: la serie mensile di Entrate, la serie mensile di Uscite, e la serie mensile di Differenza (Entrate del mese − Uscite dello stesso mese). Media e mediana sono calcolate indipendentemente su ciascuna delle tre serie (non derivando la Differenza dalle medie/mediane di Entrate e Uscite già calcolate).
  - Contratto di ritorno: un dataclass `CashflowSummary` con tre campi `income`, `expense`, `difference`, ciascuno un dataclass `Stat` con `mean: float` e `median: float`. La funzione ritorna `None` quando il calcolo non è possibile (vedi condizioni sotto) — la UI interpreta `None` come segnale per mostrare il messaggio invece dei numeri, senza dover replicare la logica di soglia.
  - Condizioni che fanno ritornare `None`:
    - `date_from` e `date_to` sono entrambi impostati e `pd.Timestamp(date_from) + pd.DateOffset(months=1) > pd.Timestamp(date_to)` (periodo selezionato inferiore a un mese di calendario esatto; se uno dei due filtri non è impostato, questa condizione non si applica).
    - Dopo aver escluso il mese corrente, zero mesi aggregati rimangono su cui calcolare media/mediana (nessuna Transazione nel periodo, o Transazioni presenti solo nel mese corrente).
- **Pagina Dashboard**: il blocco "Flusso di cassa mensile" viene reso subito sotto il grafico a barre esistente, all'interno della stessa sezione "Entrate e Uscite mensili" (stesso `st.header`, nessun header di secondo livello proprio se non un'etichetta testuale "Flusso di cassa mensile"). Usa direttamente `bar_date_from`/`bar_date_to`, già presenti in `dashboard.py`, senza aggiungere controlli di filtro propri.
- **Visualizzazione**: quando `get_monthly_cashflow_summary` ritorna un valore, tre colonne Streamlit (Entrate / Uscite / Differenza), ciascuna con due `st.metric` (Media, Mediana), formattati come stringa `"€ {value:.2f}"`. Quando ritorna `None`, un messaggio informativo (es. `st.info`) con il testo: "Intervallo troppo piccolo per calcolare il flusso di cassa mensile".
- **Glossario di dominio**: aggiungere a `CONTEXT.md` la voce "Flusso di cassa mensile" — media e mediana mensile di Entrate, Uscite e Differenza (Entrate meno Uscite), calcolate mese per mese sulle Transazioni non-Trasferimento nel periodo selezionato, escludendo sempre il mese solare in corso.

## Testing Decisions

- Segue le convenzioni già stabilite in `docs/issues/streamlit-expenses-dashboard/spec.md`: test attraverso il livello di servizio (seam unico), mai attraverso automazione della UI Streamlit; DB SQLite temporaneo per test (fixture `conn` già presente in `tests/conftest.py`); si verifica comportamento esterno osservabile (input → output), non dettagli implementativi interni.
- Prior art diretto: `tests/test_get_monthly_totals.py` (stessa fixture `_insert`/`_seed`, stesso conn temporaneo, stesse coppie di Trasferimento cross-bank da escludere).
- Casi da coprire in `tests/test_get_monthly_cashflow_summary.py`:
  - Calcolo corretto di media e mediana mensile di Entrate e di Uscite su un set di mesi con valori noti (almeno 3 mesi, per avere una mediana non banale).
  - La Differenza mensile è calcolata come propria serie (Entrate del mese − Uscite dello stesso mese) e la sua mediana, su un caso con valori scelti apposta, non coincide con `mediana(Entrate) − mediana(Uscite)` — verificando che l'implementazione non stia derivando la Differenza dalle statistiche già calcolate.
  - Le Transazioni che sono gambe di un Trasferimento cross-bank rilevato vengono escluse dal calcolo (stesso scenario di test già usato in `test_get_monthly_totals.py`).
  - Il mese solare corrente, se presente tra i dati, viene escluso dal calcolo — richiede di parametrizzare/mockare la nozione di "oggi" nel test (es. inserendo dati con date relative alla data di sistema, oppure iniettando la data corrente come parametro/dipendenza testabile).
  - Quando `date_from`/`date_to` coprono meno di un mese di calendario esatto (via `pd.DateOffset(months=1)`), la funzione ritorna `None`.
  - Quando `date_from`/`date_to` non sono impostati e non ci sono Transazioni nel DB, la funzione ritorna `None`.
  - Quando, escluso il mese corrente, non rimangono mesi di dati (es. tutte le Transazioni cadono nel mese corrente), la funzione ritorna `None`.
  - Il calcolo rispetta il proprio range di date indipendentemente da eventuali altri filtri (nessuna interferenza da Tipologia/Banca/descrizione, che questa funzione non riceve come parametri).

## Out of Scope

- Filtri propri (Tipologia, Banca, descrizione) per questo blocco — usa esclusivamente il range di date già presente nella sezione "Entrate e Uscite mensili" (decisione esplicita, vedi User Story 10).
- Persistenza dei valori calcolati — coerentemente con `docs/adr/0002-sqlite-store-with-derived-data.md`, è un valore derivato calcolato al volo, mai salvato nel DB.
- Localizzazione italiana del formato numerico (virgola decimale, punto per le migliaia) — si usa un formato semplice con punto decimale (decisione esplicita).
- Indicatori visivi di tendenza (frecce su/giù, colori delta) sopra i valori di `st.metric` — solo il valore numerico formattato.
- Modifica del comportamento esistente del grafico a barre o della sezione tabella/grafici a torta.

## Further Notes

- Glossario di dominio esistente in `CONTEXT.md`; ADR di riferimento: `docs/adr/0002-sqlite-store-with-derived-data.md` (valori derivati calcolati al volo, mai persistiti — stesso principio già applicato a Categoria e Trasferimento cross-bank, ora esteso a questo calcolo statistico).
- Spec della feature "madre" (dashboard) in `docs/issues/streamlit-expenses-dashboard/spec.md`; il ticket più direttamente correlato è `05-dashboard-grafico-a-barre.md`, di cui questo lavoro estende la sezione senza modificarne il comportamento esistente.
