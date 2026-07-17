---
status: accepted
---

# DB locale SQLite con caricamento incrementale e dati derivati calcolati al volo

In alternativa a leggere direttamente i file Excel ad ogni avvio (come faceva il notebook), l'app usa un piccolo DB SQLite locale come unica fonte di verità per le transazioni grezze, popolato tramite un form di upload che richiede di specificare esplicitamente la banca del file caricato. Ogni riga importata porta i metadati del batch di caricamento (`upload_id`, `uploaded_at`, `bank_selected`, `source_filename`), così un caricamento errato (es. banca sbagliata selezionata) può essere annullato cancellando quel batch. La deduplica tra caricamenti che si sovrappongono si basa sulla sola esistenza della chiave composita `(data, importo, descrizione, banca)` — non sul conteggio delle occorrenze — escludendo deliberatamente il caso raro di due transazioni realmente identiche nello stesso giorno.

Categoria di spesa e trasferimenti cross-bank restano dati derivati, non colonne della tabella transazioni: la categoria viene ricalcolata al volo dalle regole di fuzzy-matching correnti ad ogni lettura, così una modifica alle regole si riflette immediatamente su tutto lo storico senza bisogno di un ricalcolo esplicito. I trasferimenti cross-bank vengono invece materializzati in una tabella cache separata (`cross_bank_transfers`), ricostruita da zero (truncate + rebuild) ad ogni caricamento di un nuovo batch e ad ogni avvio dell'app — così restano ispezionabili per debug senza inquinare la tabella transazioni grezza, e non rischiano di disallinearsi dall'algoritmo di matching corrente perché non vengono mai accumulati incrementalmente.

L'accesso al DB usa `sqlite3` della standard library più `pandas.read_sql`/`to_sql`, senza ORM: lo schema è volutamente minimo (una tabella transazioni, una cache derivata) e non giustifica lo strato di astrazione di un ORM per un'app locale mono-utente.
