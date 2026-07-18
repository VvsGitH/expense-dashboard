Status: ready-for-agent

# Andamento risparmi

## Problem Statement

Nella pagina "Dashboard", la sezione "Entrate e Uscite mensili" mostra oggi un grafico a barre con Entrate e Uscite mensili, seguito dal blocco "Flusso di cassa mensile" con medie e mediane. Nessuno dei due aiuta a vedere a colpo d'occhio l'andamento nel tempo di quanto si risparmia o si va in rosso mese per mese, né a capire se, sommando mese dopo mese, si starebbe teoricamente accumulando un risparmio positivo o negativo lungo il periodo osservato. Per saperlo oggi bisognerebbe leggere il grafico a barre bar per bar, calcolare a mente la differenza di ogni mese e poi sommarle in sequenza — lento e impreciso, in particolare su periodi lunghi.

## Solution

Aggiungere, subito sotto il grafico a barre della sezione "Entrate e Uscite mensili" e prima del blocco "Flusso di cassa mensile", una nuova sotto-sezione "Andamento risparmi" con un grafico a linee sullo stesso range di date già configurato per quella sezione (`bar_date_from`/`bar_date_to`). Il grafico mostra due linee: la Differenza mensile (Entrate meno Uscite di ogni mese) e il Risparmio teorico accumulato (somma cumulata mese per mese della Differenza mensile, a partire dal primo mese del periodo selezionato). Come effetto collaterale deliberato, sia il grafico a barre sia il nuovo grafico a linee escludono sempre il mese solare in corso, i cui dati sono parziali.

## User Stories

1. Come utente, voglio vedere una linea che mostra la Differenza mensile (Entrate meno Uscite) mese per mese, così da capire subito se un dato mese è stato in attivo o in rosso senza fare la sottrazione a mente guardando le barre.
2. Come utente, voglio vedere una seconda linea che mostra il Risparmio teorico accumulato, sommando la Differenza mensile del mese K con quella di tutti i mesi precedenti nel periodo osservato, così da capire l'andamento complessivo del risparmio nel tempo, non solo mese per mese.
3. Come utente, voglio che la nuova sotto-sezione "Andamento risparmi" sia posizionata subito sotto il grafico a barre e prima di "Flusso di cassa mensile", così da leggerla come naturale prosecuzione dell'analisi del trend, prima dei numeri di sintesi.
4. Come utente, voglio che il grafico a linee usi lo stesso filtro di date già presente per il grafico a barre (`bar_date_from`/`bar_date_to`), senza dover impostare due volte lo stesso periodo.
5. Come utente, voglio che il Risparmio teorico accumulato riparta da zero al primo mese del periodo selezionato ogni volta che cambio il filtro data, così da avere una vista sempre coerente con ciò che sto effettivamente guardando, senza un "riporto" nascosto da mesi che non vedo sul grafico.
6. Come utente, voglio che il mese solare in corso sia sempre escluso, sia dal grafico a barre sia dal nuovo grafico a linee, così che un mese ancora incompleto non introduca un punto fuorviante alla fine del trend.
7. Come utente, voglio che le due linee siano etichettate chiaramente "Differenza mensile" e "Risparmio teorico accumulato" in legenda, riprendendo i termini del glossario di dominio, così da non dover indovinare cosa rappresentano.
8. Come utente, voglio che, quando non ci sono Transazioni nel periodo selezionato, venga mostrato lo stesso messaggio informativo già usato dal grafico a barre ("Nessuna Transazione nel periodo selezionato."), invece di un grafico vuoto o rotto.
9. Come utente, voglio che il calcolo escluda i Trasferimenti cross-bank, coerentemente con il grafico a barre soprastante, così che uno spostamento di denaro tra i miei conti non venga contato come un guadagno o una perdita reale.
10. Come utente, voglio che la sotto-sezione abbia un titolo chiaro "Andamento risparmi", con lo stesso stile visivo (`st.subheader`) delle altre due sotto-sezioni della stessa area ("Andamento mese per mese", "Flusso di cassa mensile"), così da percepire le tre sotto-sezioni come parte di un unico gruppo coerente.
11. Come utente, voglio che questa sotto-sezione sia indipendente dai filtri della sezione tabella (Tipologia, Banca, testo descrizione) e da quelli della sezione grafici a torta, così che restringere la tabella a una singola Banca o a una parola chiave non alteri accidentalmente l'andamento risparmi che sto guardando.
12. Come sviluppatore, voglio che "Differenza mensile" e "Risparmio teorico accumulato" siano termini di dominio documentati in `CONTEXT.md`, così da avere un vocabolario condiviso per codice, UI e documentazione futura.
13. Come sviluppatore, voglio che la scelta di far ripartire da zero il Risparmio teorico accumulato ad ogni cambio di filtro (invece di accumulare dall'inizio reale dello storico) sia documentata come ADR, così un futuro lettore capisca perché il grafico si comporta così e non "corregga" questa scelta deliberata.
14. Come sviluppatore, voglio che l'esclusione del mese corrente da `get_monthly_totals` sia testabile indipendentemente dall'orologio di sistema, tramite un parametro `today` iniettabile — stesso pattern già usato da `get_monthly_cashflow_summary` — così da poter scrivere test automatici deterministici.
15. Come sviluppatore, voglio che il calcolo del Risparmio teorico accumulato riusi i dati mensili già recuperati per il grafico a barre (`get_monthly_totals`), senza eseguire una query DB aggiuntiva, così da non duplicare l'accesso ai dati per due grafici che mostrano lo stesso periodo.
16. Come sviluppatore, voglio un livello testabile indipendente dalla UI Streamlit sia per l'esclusione del mese corrente sia per il calcolo della Differenza/cumulata, coerente con il resto dell'app, così da poter scrivere test automatici senza automazione del browser.

## Implementation Decisions

- **Seam 1 — `service.get_monthly_totals`**: viene esteso con un parametro `today: pd.Timestamp | None = None` (default alla data di sistema se non passato), che esclude dal risultato aggregato il mese solare corrente, se presente tra i mesi aggregati. Questo è un cambiamento di comportamento deliberato di una funzione già esistente e già usata dal grafico a barre (ticket `05-dashboard-grafico-a-barre.md`, già `done`): dopo questa modifica, anche il grafico a barre esclude sempre il mese in corso, non solo il nuovo grafico a linee. Segue lo stesso pattern già stabilito da `get_monthly_cashflow_summary` (che esclude il mese corrente in modo analogo e indipendente, e non viene toccato da questa modifica).
- **Seam 2 — `domain.charts.savings_trend_chart_data`**: nuova funzione pura, analoga a `monthly_totals_chart_data` già presente nello stesso modulo. Prende in input la stessa lista di dict prodotta da `get_monthly_totals` (già recuperata in `dashboard.py` per il grafico a barre, nessuna nuova chiamata) e produce un DataFrame indicizzato per mese con due colonne: "Differenza mensile" (Entrate meno Uscite del mese) e "Risparmio teorico accumulato" (somma cumulata della prima colonna, mese per mese, a partire dal primo mese presente nell'input).
- **Pagina Dashboard**: la nuova sotto-sezione viene resa nella sezione "Entrate e Uscite mensili", tra il grafico a barre esistente e "Flusso di cassa mensile". Ha un proprio `st.subheader("Andamento risparmi")`, coerente con lo stile delle altre due sotto-sezioni. Usa direttamente `bar_date_from`/`bar_date_to` già presenti in `dashboard.py`, senza filtri propri. Il grafico è reso con `st.line_chart` nativo di Streamlit, passando il DataFrame prodotto da `savings_trend_chart_data`.
- **Stato vuoto**: quando `monthly_totals` (già recuperato per il grafico a barre) è vuoto, viene mostrato lo stesso messaggio già usato per il grafico a barre ("Nessuna Transazione nel periodo selezionato."), invece del grafico a linee.
- **Glossario di dominio**: già aggiornato in questa sessione — "Differenza" promossa da definizione inline (dentro "Flusso di cassa mensile") a voce autonoma "Differenza mensile"; aggiunta la nuova voce "Risparmio teorico accumulato", con riferimento esplicito all'ADR che ne spiega la semantica di finestra filtrata.
- **ADR**: già creato in questa sessione — `docs/adr/0004-risparmio-accumulato-riparte-da-zero-nel-periodo-filtrato.md`, che documenta perché il Risparmio teorico accumulato riparte da zero nel periodo filtrato invece di accumulare dall'inizio reale dello storico (coerenza con il pattern "opera solo sul sottoinsieme filtrato" già seguito da ogni altra funzione della dashboard).

## Testing Decisions

- Segue le convenzioni già stabilite in `docs/issues/streamlit-expenses-dashboard/spec.md`: test attraverso i livelli di servizio/dominio (i due seam sopra), mai attraverso automazione della UI Streamlit; si verifica comportamento esterno osservabile (input → output), non dettagli implementativi interni.
- Prior art diretto:
  - `tests/test_get_monthly_cashflow_summary.py` per il pattern di test dell'esclusione del mese corrente tramite parametro `today` iniettabile (es. `test_excludes_current_month_from_the_calculation`).
  - `tests/test_get_monthly_totals.py` per la fixture `_insert`/`_seed` e il DB SQLite temporaneo (fixture `conn` di `tests/conftest.py`), da estendere con un nuovo test sull'esclusione del mese corrente.
  - `tests/test_charts.py` per il pattern di test di funzioni pure di shaping senza DB (es. `test_monthly_totals_chart_data_shapes_data_for_bar_chart`), da estendere con test per `savings_trend_chart_data`.
- Casi da coprire in `tests/test_get_monthly_totals.py` (nuovo test, i 4 esistenti restano invariati):
  - Il mese solare corrente (determinato da un parametro `today` iniettato nel test, non dall'orologio di sistema), se presente tra i mesi aggregati, viene escluso dal risultato.
- Casi da coprire in `tests/test_charts.py` (nuovi test per `savings_trend_chart_data`):
  - Su un set di almeno 3 mesi con Differenza mensile nota (inclusi mesi con differenza negativa), la colonna "Differenza mensile" riporta il valore corretto per ciascun mese e la colonna "Risparmio teorico accumulato" riporta la somma cumulata corretta, mese per mese, a partire dal primo mese.
  - Con lista di input vuota, il DataFrame risultante è vuoto (stesso comportamento di `monthly_totals_chart_data`).

## Out of Scope

- Filtro data indipendente per "Andamento risparmi" — usa esclusivamente `bar_date_from`/`bar_date_to` già presenti (decisione esplicita, vedi User Story 4).
- Risparmio teorico accumulato calcolato su tutta la storia delle Transazioni indipendentemente dal filtro data selezionato — decisione esplicita documentata nell'ADR 0004, il cumulato riparte sempre da zero nel periodo filtrato.
- Modifica retroattiva della checklist del ticket `docs/issues/streamlit-expenses-dashboard/05-dashboard-grafico-a-barre.md` (rimane un record storico di cosa fu costruito allora); questo ticket documenta invece il nuovo comportamento (esclusione del mese corrente) come estensione esplicita di quella funzione.
- Modifica del comportamento di `get_monthly_cashflow_summary`, che già esclude il mese corrente in modo indipendente e non viene toccato da questo lavoro.
- Localizzazione italiana del formato numerico sugli assi/tooltip del grafico a linee — si usa il rendering di default di `st.line_chart`.
- Personalizzazioni visive (colori, stile linee) oltre al rendering di default di `st.line_chart`.
- Persistenza dei valori calcolati — coerentemente con `docs/adr/0002-sqlite-store-with-derived-data.md`, sono valori derivati calcolati al volo, mai salvati nel DB.

## Further Notes

- Glossario di dominio aggiornato in `CONTEXT.md` (voci "Differenza mensile" e "Risparmio teorico accumulato"); ADR di riferimento: `docs/adr/0004-risparmio-accumulato-riparte-da-zero-nel-periodo-filtrato.md` e, per il principio più generale di dati derivati calcolati al volo, `docs/adr/0002-sqlite-store-with-derived-data.md`.
- Spec della feature "madre" (dashboard) in `docs/issues/streamlit-expenses-dashboard/spec.md`; ticket più direttamente correlati: `05-dashboard-grafico-a-barre.md` (di cui questo lavoro estende sia la sezione sia il comportamento di `get_monthly_totals`) e `docs/issues/flusso-di-cassa-mensile/spec.md` (sotto-sezione immediatamente successiva nella stessa area, non impattata da questo lavoro).
- Emerso durante la sessione di grilling che ha preceduto questa spec: l'utente ha osservato che il grafico a barre esistente avrebbe dovuto escludere il mese corrente fin da subito, coerentemente con "Flusso di cassa mensile" — da qui la decisione esplicita di allargare lo scope di questo ticket per correggere anche quel comportamento, invece di limitarsi al solo nuovo grafico a linee.
