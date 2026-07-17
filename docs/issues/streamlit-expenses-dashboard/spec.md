Status: ready-for-agent

# Dashboard locale di monitoraggio spese (Streamlit)

## Problem Statement

Oggi l'analisi delle mie spese personali vive interamente in `src/notebook.ipynb`: per vedere lo stato aggiornato devo aprire Jupyter, ricaricare a mano i file Excel esportati dalle banche, rieseguire le celle nell'ordine giusto e leggere grafici statici. Non c'è un modo rapido per consultare la situazione, filtrare per periodo/banca/categoria, o aggiungere nuovi dati senza sovrascrivere file e rieseguire tutto da capo. Il notebook mischia inoltre ingestion, elaborazione e visualizzazione nello stesso posto, rendendo fragile qualsiasi modifica (es. una correzione manuale hardcoded su un indice di riga specifico).

## Solution

Sostituire il notebook con una webapp Streamlit locale che gira su richiesta (`streamlit run`), sostenuta da un piccolo DB SQLite locale come unica fonte di verità delle Transazioni. L'app ha due pagine: **Carica dati** (form di upload di un estratto conto Excel, con selezione esplicita della Banca) e **Dashboard** (tre sezioni sulla stessa pagina — tabella transazioni, grafico a barre mensile, grafici a torta per Categoria — ciascuna con i propri filtri indipendenti). La logica di ingestion, categorizzazione e rilevamento Trasferimenti cross-bank viene estratta dal notebook in moduli Python riutilizzabili sia dall'app che da uno script di migrazione one-off per importare lo storico già raccolto. Vedi `CONTEXT.md` per il glossario di dominio e `docs/adr/0001-retire-notebook-for-streamlit-app.md` / `docs/adr/0002-sqlite-store-with-derived-data.md` per le decisioni architetturali di fondo.

## User Stories

### Migrazione e ritiro del notebook

1. Come utente che ha usato il notebook finora, voglio che tutto lo storico delle Transazioni venga migrato nel nuovo DB tramite uno script one-off, così da non perdere i dati già raccolti.
2. Come utente, voglio che la correzione manuale della Transazione TFR (oggi hardcoded sull'indice di riga 301 nel notebook) venga applicata automaticamente durante la migrazione, identificando quella Transazione per data/importo/descrizione e non per indice di riga, così i totali storici restano corretti senza intervento manuale ripetuto.
3. Come utente, voglio poter modificare le regole di categorizzazione in un modulo Python e vedere l'effetto immediatamente riavviando il dev server di Streamlit, così da non dover più usare il notebook per iterare sulle regole.
4. Come utente, voglio che il notebook venga rimosso dal repository una volta verificato che script di migrazione e dashboard riproducono correttamente lo storico, così da avere una sola fonte di verità per la logica.

### Caricamento dati

5. Come utente, voglio caricare un nuovo estratto conto Excel tramite un form nella pagina "Carica dati", così da aggiungere nuove Transazioni senza modificare file manualmente.
6. Come utente, voglio specificare esplicitamente la Banca a cui appartiene il file che sto caricando, così che l'app usi il parser corretto per quel formato.
7. Come utente, voglio che le Transazioni già presenti nel DB non vengano duplicate quando ricarico un file che si sovrappone a un Caricamento precedente, così da poter scaricare estratti conto con finestre temporali sovrapposte senza preoccuparmi dei duplicati.
8. Come utente, accetto che due Transazioni realmente identiche (stessa data, importo, descrizione, Banca) vengano trattate come un duplicato anche se non lo sono, poiché è un caso raro e la semplicità del controllo (sola esistenza della chiave) mi basta.
9. Come utente, voglio vedere un riepilogo di quante Transazioni sono state inserite e quante scartate come duplicate dopo ogni Caricamento, così da capire subito l'esito dell'operazione.
10. Come utente, voglio poter annullare l'ultimo Caricamento se mi accorgo di aver selezionato la Banca sbagliata o caricato il file sbagliato, così da correggere l'errore senza dover intervenire manualmente sul DB.
11. Come utente, voglio vedere uno storico dei Caricamenti effettuati (data, Banca, nome file, numero di Transazioni inserite), così da poter verificare cosa ho già importato e trovare il Caricamento da annullare.

### Trasferimenti cross-bank

12. Come utente, voglio che i Trasferimenti cross-bank (stesso importo, Banche diverse, entro 7 giorni) vengano automaticamente esclusi dai totali di spese ed entrate mostrati in dashboard, così che i totali riflettano solo movimenti reali.
13. Come utente/sviluppatore, voglio poter ispezionare quali coppie di Transazioni sono state classificate come Trasferimenti cross-bank in una tabella cache separata, così da poter fare debug se il matching sbaglia, senza che questi dati "sporchino" la tabella delle Transazioni grezze.
14. Come utente, voglio che la cache dei Trasferimenti cross-bank si ricostruisca automaticamente ad ogni Caricamento, ad ogni annullamento di un Caricamento, e ad ogni avvio dell'app, così da non doverla mai ricalcolare manualmente e da non rischiare che si disallinei dall'algoritmo di matching corrente.

### Dashboard — sezione tabella

15. Come utente, voglio vedere l'elenco di tutte le mie Transazioni (Entrate e Uscite) in una tabella, così da poter ispezionare i singoli movimenti.
16. Come utente, voglio filtrare la tabella per un range di date, così da concentrarmi su un periodo specifico.
17. Come utente, voglio filtrare la tabella per Tipologia (solo Entrate, solo Uscite, entrambe), così da separare i due flussi quando mi serve.
18. Come utente, voglio filtrare la tabella per Banca, così da vedere i movimenti di un singolo conto.
19. Come utente, voglio filtrare la tabella per testo libero nella descrizione, così da cercare rapidamente una Transazione specifica (es. un dato negozio).
20. Come utente, voglio che i filtri della tabella siano indipendenti da quelli delle altre due sezioni della dashboard, così da poter ispezionare un periodo diverso da quello che sto analizzando nei grafici.

### Dashboard — sezione grafico a barre

21. Come utente, voglio un grafico a barre che mostri Entrate e Uscite mensili, così da vedere l'andamento nel tempo a colpo d'occhio.
22. Come utente, voglio poter configurare dinamicamente il range di date del grafico a barre, indipendentemente dagli altri filtri della pagina, così da confrontare periodi diversi senza che le altre sezioni cambino.

### Dashboard — sezione grafici a torta

23. Come utente, voglio grafici a torta che mostrino la ripartizione delle Uscite per Categoria, così da capire dove vanno i miei soldi.
24. Come utente, voglio poter configurare il range di date dei grafici a torta, indipendentemente dalle altre due sezioni, così da analizzare periodi diversi in parallelo.
25. Come utente, voglio che la Categoria di ogni Uscita venga calcolata al momento della visualizzazione usando le regole correnti, così che una modifica alle regole si rifletta subito su tutto lo storico mostrato, senza bisogno di un ricalcolo esplicito.

### Non funzionali

26. Come utente, voglio che l'app giri interamente in locale, senza inviare dati a servizi esterni, poiché si tratta dei miei dati finanziari personali.
27. Come sviluppatore, voglio un livello di servizio testabile indipendente dalla UI Streamlit, così da poter scrivere test automatici senza bisogno di automazione del browser.

## Implementation Decisions

- **Livello di servizio (seam unico)**: le pagine Streamlit sono un guscio sottile su un piccolo insieme di funzioni di servizio, che sono anche l'unico punto testato:
  - `ingest_file(bank, file)` — parsing del file caricato, deduplica per esistenza della chiave `(date, value, description, bank)`, insert nel DB con i metadati del Caricamento, rebuild della cache Trasferimenti, ritorna un riepilogo (righe inserite/scartate).
  - `undo_upload(upload_id)` — rimuove tutte le Transazioni di quel Caricamento e forza il rebuild della cache Trasferimenti.
  - `get_transactions(filters)` — per la sezione tabella; filtri: range date, Tipologia (Entrata/Uscita/entrambe), Banca, testo descrizione.
  - `get_monthly_totals(date_range)` — per il grafico a barre; Entrate/Uscite mensili al netto dei Trasferimenti cross-bank.
  - `get_category_breakdown(date_range)` — per i grafici a torta; Categoria calcolata al volo sulle Uscite nel range.
- **Moduli di supporto** (nessun percorso di file vincolante, solo responsabilità):
  - Modulo DB: schema, connessione SQLite, funzioni di insert/query a basso livello.
  - Un modulo di ingestion per Banca (Poste, BBVA, Others): converte il file Excel caricato in un DataFrame con colonne standard (date, description, value, bank, type), riusando la logica già presente nel notebook (celle di lettura Poste/BBVA/Others).
  - Modulo di categorizzazione: le regole di fuzzy-matching (`EXP_CATEGORIES` e la funzione di scoring) portate dal notebook in un modulo importabile sia dall'app che dai test.
  - Modulo Trasferimenti: detection (join per importo, Banche diverse, finestra di 7 giorni) e rebuild della cache.
  - Modulo grafici: prepara i DataFrame aggregati per grafico a barre e grafici a torta a partire dai dati filtrati; la libreria di plotting concreta è un dettaglio implementativo lasciato alla fase di build.
  - Script di migrazione one-off: richiama gli stessi moduli di ingestion per i tre file storici in `data/`, escludendo esplicitamente la Transazione TFR nota (identificata per data/importo/descrizione).
- **Schema DB** (SQLite, `sqlite3` stdlib + pandas, nessun ORM — ADR-0002):
  - Tabella Transazioni: id (chiave primaria autoincrementale), date, description, value (sempre positivo), bank, type (expense/income), upload_id, uploaded_at, source_filename.
  - Tabella cache `cross_bank_transfers`: riferimenti (foreign key) alla Transazione di Uscita e alla Transazione di Entrata che compongono ciascun Trasferimento rilevato; ricostruita interamente (truncate + rebuild), mai accumulata in modo incrementale.
  - Categoria non è una colonna persistita: sempre calcolata al volo dalle regole correnti (ADR-0002).
- **Pagine Streamlit**: due pagine con navigazione multipagina nativa — "Dashboard" (le tre sezioni con filtri indipendenti) e "Carica dati" (form banca + file, riepilogo esito, storico Caricamenti con azione di annullamento).
- **Dipendenze**: il repository non ha oggi un file di manifest delle dipendenze (nessun `requirements.txt`/`pyproject.toml`, solo l'elenco libero in `README.md`) — va introdotto come parte di questo lavoro. Nuove dipendenze da aggiungere: `streamlit`, `pytest`. Dipendenze già in uso da riportare nel manifest: `pandas`, `openpyxl`, `rapidfuzz`, `matplotlib` (se mantenuto per i grafici).
- **Editing manuale delle Transazioni**: non incluso in questa spec (vedi Out of Scope); la correzione TFR storica è gestita esclusivamente nello script di migrazione.

## Testing Decisions

- Il repository non ha oggi alcun test automatico; `pytest` viene introdotto come framework, senza prior art diretto nel repo a cui ispirarsi — si seguono le convenzioni standard pytest (funzioni di test, fixture per DB temporaneo e dati di esempio).
- I test passano esclusivamente attraverso il livello di servizio (seam unico definito sopra), usando un DB SQLite temporaneo per ogni test (file temporaneo o `:memory:`); mai attraverso l'automazione della UI Streamlit.
- I test verificano comportamento esterno osservabile (input → output/stato del DB), non dettagli implementativi interni ai singoli moduli di supporto.
- Casi da coprire:
  - **Ingestion**: dato un file Excel di fixture per ciascuna Banca (colonne rappresentative reali, dati sintetici — mai i dati finanziari reali dell'utente), `ingest_file` produce il numero atteso di Transazioni con i campi attesi.
  - **Deduplica**: ricaricare lo stesso file, o un file con righe sovrapposte a un Caricamento precedente, non crea duplicati; una Transazione realmente ripetuta e identica viene comunque deduplicata (comportamento accettato per design, non un bug da correggere nel test).
  - **Undo**: `undo_upload` rimuove esattamente le Transazioni di quel batch e nessun'altra, e forza il rebuild della cache Trasferimenti.
  - **Categorizzazione**: `get_category_breakdown` riflette immediatamente una modifica alle regole di categorizzazione tra una chiamata e l'altra (nessuno stato persistito da invalidare).
  - **Trasferimenti**: coppie di Transazioni che rispettano i criteri (stesso importo, Banche diverse, entro 7 giorni) vengono escluse dai totali restituiti da `get_monthly_totals`; coppie che non li rispettano (stessa Banca, oltre 7 giorni, importo diverso) non vengono escluse.
  - **Filtri tabella**: `get_transactions` rispetta correttamente ciascun filtro (range date, Tipologia, Banca, testo descrizione), singolarmente e in combinazione.
  - **Filtri grafici**: `get_monthly_totals` e `get_category_breakdown` rispettano il proprio range di date in modo indipendente dai filtri delle altre sezioni.
  - **Migrazione**: lo script di migrazione, eseguito sui tre file storici, produce un DB coerente con l'output del notebook attuale (stessi totali di spese/entrate/Trasferimenti sullo stesso range di date), e la Transazione TFR nota risulta esclusa.

## Out of Scope

- UI di editing/esclusione manuale di singole Transazioni (rimandata a quando servirà di nuovo un caso simile al TFR).
- Feature "top 3 spese per mese" (TODO aperto in `README.md`, rimandata a un'iterazione successiva, distinta da questo restructuring).
- Supporto per nuove Banche oltre a Poste/BBVA/Others (richiederebbe un nuovo parser, non incluso ora).
- Conferma manuale dei Trasferimenti cross-bank rilevati (persistenza di uno stato "confermato/non confermato") — scartata a favore del calcolo al volo con cache derivata (ADR-0002).
- Deploy o accesso remoto: l'app resta strettamente locale e mono-utente; niente autenticazione, niente hosting, niente accesso da rete.
- Deduplica basata sul conteggio delle occorrenze (multiplicity-aware) — scartata a favore della sola esistenza della chiave (decisione esplicita, vedi User Story 8).
- Persistenza della Categoria come colonna nel DB — scartata a favore del calcolo al volo (ADR-0002).
- Filtri condivisi tra le tre sezioni della dashboard — scartati a favore di filtri indipendenti per sezione (decisione esplicita, vedi User Story 20).

## Further Notes

- Glossario di dominio completo in `CONTEXT.md` (Transazione, Tipologia, Categoria, Banca, Trasferimento cross-bank, Caricamento) — da usare come vocabolario per nomi di funzioni/variabili nell'implementazione.
- Decisioni architettoniche di fondo registrate in `docs/adr/0001-retire-notebook-for-streamlit-app.md` e `docs/adr/0002-sqlite-store-with-derived-data.md`.
- Il notebook `src/notebook.ipynb` resta presente come riferimento della logica esistente durante lo sviluppo, e va rimosso solo a migrazione verificata (vedi User Story 4).
