# 02 — Andamento risparmi: grafico a linee

**What to build:** Nella pagina "Dashboard", sezione "Entrate e Uscite mensili", una nuova sotto-sezione "Andamento risparmi" — posizionata subito sotto il grafico a barre esistente e prima di "Flusso di cassa mensile" — mostra un grafico a linee con due serie: la Differenza mensile (Entrate meno Uscite di ogni mese) e il Risparmio teorico accumulato (somma cumulata mese per mese della Differenza mensile, a partire dal primo mese del periodo selezionato). Usa lo stesso filtro data del grafico a barre soprastante (`bar_date_from`/`bar_date_to`), riusa gli stessi dati mensili già recuperati per quel grafico (nessuna nuova query DB), esclude i Trasferimenti cross-bank ed eredita l'esclusione del mese corrente dal ticket 01. Il glossario di dominio ("Differenza mensile", "Risparmio teorico accumulato") e l'ADR sulla semantica del cumulato sono già stati scritti in una sessione precedente.

**Blocked by:** 01 — riusa `service.get_monthly_totals` già esteso con l'esclusione del mese corrente, così il nuovo grafico la eredita senza lavoro aggiuntivo.

**Status:** done

- [x] Nuova funzione pura `domain.charts.savings_trend_chart_data`, analoga a `monthly_totals_chart_data`, che prende in input la stessa lista di dict prodotta da `get_monthly_totals` e produce un DataFrame indicizzato per mese con colonne "Differenza mensile" (Entrate meno Uscite del mese) e "Risparmio teorico accumulato" (somma cumulata della prima colonna, mese per mese, a partire dal primo mese presente nell'input)
- [x] Con lista di input vuota, `savings_trend_chart_data` ritorna un DataFrame vuoto (stesso comportamento di `monthly_totals_chart_data`)
- [x] Test in `tests/test_charts.py` verificano, su almeno 3 mesi con Differenza mensile nota (inclusi mesi con differenza negativa), sia i valori di "Differenza mensile" sia la somma cumulata corretta di "Risparmio teorico accumulato"
- [x] Nella pagina Dashboard, tra il grafico a barre esistente e "Flusso di cassa mensile", una nuova sotto-sezione `st.subheader("Andamento risparmi")`, senza filtri propri, usa `bar_date_from`/`bar_date_to` già esistenti
- [x] Il grafico è reso con `st.line_chart` nativo, con le due serie etichettate esattamente "Differenza mensile" e "Risparmio teorico accumulato" (nomi colonna del DataFrame passato al widget)
- [x] Quando `monthly_totals` (già recuperato per il grafico a barre) è vuoto, viene mostrato lo stesso messaggio "Nessuna Transazione nel periodo selezionato." invece del grafico a linee
- [x] La sotto-sezione non introduce filtri propri (Tipologia, Banca, descrizione) e non è influenzata dai filtri della sezione tabella o dei grafici a torta
- [x] Verificato manualmente in browser: il grafico a linee mostra le due serie coerenti con i dati, il messaggio di stato vuoto appare quando il periodo filtrato non ha Transazioni, e il mese corrente resta escluso (ereditato dal ticket 01)

## Comments

Implementato con TDD sul seam `domain.charts.savings_trend_chart_data`: funzione pura che riusa la stessa lista di dict di `get_monthly_totals` (nessuna nuova query DB), calcola "Differenza mensile" (Entrate − Uscite) e la sua somma cumulata "Risparmio teorico accumulato", riparte da zero al primo mese dell'input come previsto dall'ADR 0004. Nella Dashboard, la nuova sotto-sezione "Andamento risparmi" siede tra il grafico a barre e "Flusso di cassa mensile", riusa `bar_date_from_iso`/`bar_date_to_iso` e `monthly_totals`/`monthly_totals_df` già calcolati per il grafico a barre soprastante, nessun filtro proprio. Suite completa verde (56 test). Verificato manualmente in browser: le due linee sono coerenti con l'andamento del grafico a barre, il layout rispetta l'ordine richiesto, nessun errore.

Code review a due assi: Spec senza lacune (nessuno scope creep, verificata con attenzione la semantica del cumulato che riparte davvero dal primo mese dell'input). Standards ha segnalato due judgement call, entrambi applicati: estratto un helper privato `_monthly_totals_frame` condiviso tra `monthly_totals_chart_data` e `savings_trend_chart_data` (prima duplicavano la stessa costruzione del DataFrame), e rinominata la variabile locale generica `data` in `monthly`, coerente con lo stile del resto del modulo.
