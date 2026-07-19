Status: ready-for-agent

# Spese mensili per Categoria — revisione tooltip e nuovo grafico impilato

## Problem Statement

Nella sezione "Uscite per Categoria" della Dashboard, il bar chart appena introdotto (vedi `docs/issues/ripartizione-uscite-per-categoria/`) mostra il totale per Categoria affiancato da una tabella con Categoria/€/%. Dopo un controllo visivo, la tabella sotto il grafico risulta ridondante: duplica in forma tabellare informazioni già leggibili nel grafico stesso, appesantendo la sezione. Inoltre, la sezione oggi risponde solo alla domanda "quanto ho speso in ogni Categoria nel periodo selezionato" — non mostra come questa ripartizione sia cambiata nel tempo, mese per mese, un'informazione utile per capire se una Categoria sta assorbendo una quota crescente o calante della spesa complessiva.

## Solution

Nella sezione "Uscite per Categoria": la tabella viene rimossa; la percentuale sul totale, che oggi vive solo nella tabella, si sposta nel tooltip del bar chart esistente, accanto a Categoria e Totale (€) già presenti (nessuna informazione rimossa, solo consolidata nel tooltip). Subito sotto il bar chart, una nuova sotto-visualizzazione "Spese mensili per Categoria" mostra un grafico a colonne verticali, una per mese, ciascuna impilata per Categoria e normalizzata al 100% (l'altezza mostra sempre le proporzioni tra Categorie in quel mese, non l'importo assoluto). Usa lo stesso filtro di date indipendente già presente per la sezione (nessun filtro proprio), esclude sempre il mese solare in corso (dati parziali, coerente con `get_monthly_totals`), e mostra sempre tutte le Categorie note (nessun bucket "Altro").

## User Stories

1. Come utente, voglio che la sezione "Uscite per Categoria" non mostri più la tabella sotto il grafico, così da avere una vista più snella senza informazioni duplicate.
2. Come utente, voglio vedere la percentuale sul totale nel tooltip del bar chart, accanto all'importo in € già presente, così da non perdere questa informazione con la rimozione della tabella.
3. Come utente, voglio vedere, subito sotto il bar chart della stessa sezione, un nuovo grafico che mostra come la spesa si è distribuita tra le Categorie mese per mese, così da capire l'andamento nel tempo della composizione delle mie spese, non solo il totale del periodo.
4. Come utente, voglio che ogni colonna mensile sia alta uguale alle altre (normalizzata al 100%), con i segmenti che mostrano solo le proporzioni tra Categorie in quel mese, così da confrontare facilmente la composizione tra mesi diversi senza che la variazione della spesa totale mensile interferisca con il confronto.
5. Come utente, voglio che il nuovo grafico usi lo stesso filtro di date indipendente già presente nella sezione "Uscite per Categoria", senza dover impostare un secondo filtro per lo stesso periodo.
6. Come utente, voglio che il mese solare in corso sia sempre escluso dal nuovo grafico, coerentemente con gli altri grafici mensili della dashboard, così che un mese ancora incompleto non introduca una colonna fuorviante.
7. Come utente, voglio che ogni Categoria mantenga lo stesso colore già in uso nel bar chart sovrastante, così da riconoscere a colpo d'occhio la stessa Categoria in entrambi i grafici della sezione.
8. Come utente, voglio vedere una legenda con i colori delle Categorie nel nuovo grafico, dato che qui — a differenza del bar chart sovrastante — l'asse mostra i mesi e non le Categorie, così da poter identificare ogni segmento senza dover passare il mouse su ognuno.
9. Come utente, voglio che passando il mouse su un segmento veda mese, Categoria, importo in € e percentuale su quel mese, così da avere il dato esatto oltre alla proporzione visiva.
10. Come utente, voglio che tutte le Categorie note siano sempre mostrate come segmenti separati, senza un bucket "Altro" che le raggruppi, coerentemente con la scelta già fatta per il bar chart sovrastante.
11. Come utente, voglio che, quando non ci sono Uscite nel periodo selezionato, venga mostrato lo stesso messaggio informativo già usato dal bar chart sovrastante ("Nessuna Uscita nel periodo selezionato."), invece di un grafico vuoto o rotto.
12. Come sviluppatore, voglio che la query mese×Categoria riusi la stessa logica di esclusione Trasferimenti/Entrate ed escluda il mese corrente con lo stesso pattern già stabilito da `get_monthly_totals` (parametro `today` iniettabile), così da restare coerente e testabile deterministicamente.
13. Come sviluppatore, voglio un livello di shaping puro e testabile indipendente dalla UI Streamlit per il nuovo grafico, coerente con il resto del modulo `domain/charts.py`, così da poter scrivere test automatici senza automazione del browser.
14. Come sviluppatore, voglio che il grafico impilato usi lo stesso approccio con scale colore esplicito (dominio/range) già adottato per il bar chart, per evitare di reintrodurre il bug di scrambling colori scoperto e risolto nel ticket precedente.
15. Come sviluppatore, voglio che la funzione `category_breakdown_table_data`, diventata inutilizzata con la rimozione della tabella, sia eliminata insieme ai suoi test, così da non lasciare codice morto nel modulo.

## Implementation Decisions

- **Seam 1 — nuova funzione `service.get_monthly_category_breakdown`**: firma analoga a `get_monthly_totals` (`conn=None, date_from: str | None = None, date_to: str | None = None, today: pd.Timestamp | None = None`). Riusa `_read_non_transfer_transactions` per il filtro Trasferimenti/range-date già stabilito, filtra solo le Uscite, applica `categorize_description` (stessa logica di `get_category_breakdown`), raggruppa per (mese, Categoria) sommando l'importo, esclude il mese solare corrente con lo stesso pattern già in uso in `get_monthly_totals` (drop dell'indice corrispondente a `today` o `pd.Timestamp.now()`). Restituisce una lista di dict `{"month": ..., "category": ..., "value": ...}`, una riga per ogni combinazione (mese, Categoria) con importo diverso da zero — le combinazioni senza spesa in quel mese non compaiono, coerentemente con `get_category_breakdown`.
- **Seam 2 — nuova funzione pura `domain.charts.monthly_category_breakdown_chart_data`**: prende in input la lista di dict prodotta da `get_monthly_category_breakdown` e restituisce un DataFrame in formato long (una riga per combinazione mese/Categoria) con colonne "Mese", "Categoria", "Totale (€)" (riusa la costante `CATEGORY_TOTAL_COLUMN` già esistente) e "Percentuale" (quota della Categoria sul totale di Uscite di quel singolo mese — non sul totale del periodo). Con lista di input vuota, restituisce un DataFrame vuoto.
- **Pagina Dashboard, sezione "Uscite per Categoria"**:
  - Il tooltip del bar chart esistente passa da `["Categoria", "Totale (€)"]` a `["Categoria", "Totale (€)", "Percentuale"]`; la riga `st.dataframe(category_breakdown_table_data(...))` viene rimossa.
  - Subito sotto, una nuova sotto-visualizzazione (senza filtro proprio, riusa `category_date_from`/`category_date_to` già presenti in questa sezione) chiama `get_monthly_category_breakdown` con lo stesso range di date, passa il risultato a `monthly_category_breakdown_chart_data`, e rende un `alt.Chart(...).mark_bar()` con `x` = Mese (ordinale, ordine cronologico), `y` = Totale (€) con `stack="normalize"` (impilamento normalizzato al 100%), `color` = Categoria con lo stesso `alt.Scale(domain=category_names(), range=category_colors(...))` già usato per il bar chart sovrastante (stesso meccanismo, per evitare il bug di scrambling colori del ticket precedente) ma con **legenda visibile** (a differenza del bar chart sovrastante, che la nasconde perché l'asse etichetta già le Categorie direttamente — qui l'asse mostra i mesi, quindi la legenda è l'unico modo per identificare i segmenti oltre al tooltip), e `tooltip` su Mese/Categoria/Totale (€)/Percentuale.
  - Stato vuoto: se il risultato di `get_monthly_category_breakdown` è vuoto, viene mostrato lo stesso messaggio informativo già usato dal bar chart sovrastante ("Nessuna Uscita nel periodo selezionato."), invece del grafico.
- **Rimozione codice morto**: `domain.charts.category_breakdown_table_data` e i suoi 2 test in `tests/test_charts.py` vengono eliminati, non avendo più alcun chiamante in produzione dopo la rimozione della tabella.
- **Palette colori**: nessuna modifica a `CATEGORY_COLORS` — si riusa quella già validata e corretta nei ticket precedenti. Il limite noto già documentato (mancata piena separazione CVD su tutte le coppie non-adiacenti, con 11 colori) resta valido e si estende anche a questo nuovo grafico; la legenda visibile qui e il tooltip diretto restano la mitigazione, coerente con quanto già accettato per il bar chart.

## Testing Decisions

- Segue le convenzioni già stabilite in `docs/issues/ripartizione-uscite-per-categoria/spec.md`: test attraverso i due livelli già usati da ogni altro grafico della dashboard (funzione di servizio con DB reale via fixture, funzione pura di shaping senza DB), mai attraverso automazione della UI Streamlit; si verifica comportamento esterno osservabile (input → output).
- Prior art diretto:
  - `tests/test_get_monthly_totals.py` per il pattern di test di una funzione di servizio mensile con esclusione del mese corrente tramite parametro `today` iniettabile e la fixture `conn`/seed di `tests/conftest.py`.
  - `tests/test_get_category_breakdown.py` per il pattern di test dell'esclusione Entrate/Trasferimenti e della categorizzazione.
  - `tests/test_charts.py` per il pattern di test di funzioni pure di shaping senza DB (es. `test_category_breakdown_chart_data_shapes_data_for_pie_chart`, da adattare per il formato long a due chiavi mese+categoria).
- Casi da coprire in un nuovo `tests/test_get_monthly_category_breakdown.py` (o file analogo):
  - Le Uscite vengono raggruppate correttamente per (mese, Categoria) sommando gli importi; le Entrate e i Trasferimenti cross-bank sono esclusi.
  - Il mese solare corrente (determinato da un `today` iniettato nel test), se presente, viene escluso dal risultato.
  - Con nessuna Uscita nel range selezionato, il risultato è una lista vuota.
- Casi da coprire in `tests/test_charts.py` (nuovi test per `monthly_category_breakdown_chart_data`):
  - Su un breakdown noto con almeno 2 mesi e almeno 2 Categorie per mese, il DataFrame risultante riporta correttamente Mese/Categoria/Totale (€)/Percentuale, con la Percentuale calcolata sul totale del singolo mese (non sul totale del periodo).
  - Con lista di input vuota, il DataFrame risultante è vuoto.
- I 2 test esistenti per `category_breakdown_table_data` vengono rimossi insieme alla funzione.

## Out of Scope

- Bucket "Altro" per le Categorie minori nel nuovo grafico — esplicitamente scartato, coerente con la scelta già fatta per il bar chart sovrastante di mostrare sempre tutte le Categorie.
- Impilamento in valore assoluto (altezza colonna = spesa totale del mese) — scartato esplicitamente: la normalizzazione al 100% è la scelta voluta, per confrontare le proporzioni tra mesi indipendentemente dall'importo totale speso.
- Filtro di date proprio per il nuovo grafico — riusa esclusivamente `category_date_from`/`category_date_to` già presenti nella sezione.
- Piena conformità CVD su tutte le coppie di colori non-adiacenti (`--pairs all`) — limite preesistente e già accettato nei ticket precedenti, non riaperto da questo lavoro.
- Nuove voci di glossario in `CONTEXT.md` o nuovi ADR — è un incrocio presentazionale di concetti di dominio già definiti (Uscita, Categoria, mese), non un nuovo concetto di business da nominare.
- Modifica a `get_category_breakdown` o al bar chart totali-per-categoria oltre all'aggiunta della Percentuale nel tooltip e alla rimozione della tabella.

## Further Notes

- Spec precedente della stessa area: `docs/issues/ripartizione-uscite-per-categoria/spec.md` (ticket 01 correzione colori, ticket 02 introduzione bar chart + tabella, quest'ultima ora rimossa da questo lavoro).
- Emerso durante la sessione di grilling che ha preceduto questa spec: la richiesta iniziale conteneva un'ambiguità tra "grafico a barre orizzontale" e "barre verticali coi segmenti impilati" per lo stesso nuovo grafico — chiarita esplicitamente in favore di colonne verticali per mese, coerenti con il grafico "Andamento mese per mese" già esistente nella sezione "Entrate e Uscite mensili" (che resta un riferimento di stile, non la posizione del nuovo grafico).
- Il nome di lavoro "Spese mensili per Categoria" usato in questa spec per la nuova sotto-visualizzazione è provvisorio; l'eventuale titolo `st.subheader` esatto è un dettaglio di implementazione lasciato allo sviluppatore, coerente con lo stile delle altre sotto-sezioni della dashboard.
