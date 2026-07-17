# 01 — Caricamento estratti conto con deduplica

**What to build:** L'utente apre la pagina "Carica dati", seleziona la Banca (Poste, BBVA, o Others) e carica il file Excel corrispondente. Le Transazioni vengono estratte e salvate nel DB SQLite locale insieme ai metadati del Caricamento (banca, data caricamento, nome file), senza creare duplicati se il file si sovrappone a Caricamenti precedenti. L'utente vede un riepilogo di quante Transazioni sono state inserite e quante scartate come duplicate.

**Blocked by:** Nessuno — può partire subito.

**Status:** ready-for-agent

- [ ] La pagina "Carica dati" permette di selezionare la Banca (Poste, BBVA, Others) e caricare un file Excel
- [ ] Ogni Banca usa il parser corretto per il proprio formato di export (colonne/intestazioni specifiche, riusando la logica già presente nel notebook)
- [ ] Le Transazioni caricate vengono salvate nel DB con date, description, value (sempre positivo), bank, type (Entrata/Uscita), e i metadati del Caricamento (upload_id, uploaded_at, source_filename)
- [ ] Ricaricare un file che si sovrappone (parzialmente o interamente) a Transazioni già presenti nel DB non crea duplicati, usando la sola esistenza della chiave `(date, value, description, bank)`
- [ ] Due Transazioni realmente identiche (stessa data, importo, descrizione, banca) vengono trattate come duplicato — comportamento accettato per design
- [ ] Dopo ogni caricamento viene mostrato un riepilogo con il numero di Transazioni inserite e il numero scartate come duplicate
- [ ] Test automatici, passando attraverso `ingest_file`, coprono l'ingestion per ciascuna Banca (con fixture Excel sintetiche) e il comportamento di deduplica
