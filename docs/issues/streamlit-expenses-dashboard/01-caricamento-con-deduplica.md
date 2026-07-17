# 01 — Caricamento estratti conto con deduplica

**What to build:** L'utente apre la pagina "Carica dati", seleziona la Banca (Poste, BBVA, o Others) e carica il file Excel corrispondente. Le Transazioni vengono estratte e salvate nel DB SQLite locale insieme ai metadati del Caricamento (banca, data caricamento, nome file), senza creare duplicati se il file si sovrappone a Caricamenti precedenti. L'utente vede un riepilogo di quante Transazioni sono state inserite e quante scartate come duplicate.

**Blocked by:** Nessuno — può partire subito.

**Status:** done

- [x] La pagina "Carica dati" permette di selezionare la Banca (Poste, BBVA, Others) e caricare un file Excel
- [x] Ogni Banca usa il parser corretto per il proprio formato di export (colonne/intestazioni specifiche, riusando la logica già presente nel notebook)
- [x] Le Transazioni caricate vengono salvate nel DB con date, description, value (sempre positivo), bank, type (Entrata/Uscita), e i metadati del Caricamento (upload_id, uploaded_at, source_filename)
- [x] Ricaricare un file che si sovrappone (parzialmente o interamente) a Transazioni già presenti nel DB non crea duplicati, usando la sola esistenza della chiave `(date, value, description, bank)`
- [x] Due Transazioni realmente identiche (stessa data, importo, descrizione, banca) vengono trattate come duplicato — comportamento accettato per design
- [x] Dopo ogni caricamento viene mostrato un riepilogo con il numero di Transazioni inserite e il numero scartate come duplicate
- [x] Test automatici, passando attraverso `ingest_file`, coprono l'ingestion per ciascuna Banca (con fixture Excel sintetiche) e il comportamento di deduplica

## Comments

Implementato con TDD sul seam `ingest_file` (6 test, tutti verdi). Code review a due assi (Standards + Spec) eseguita post-implementazione:
- Spec: nessuna lacuna, tutti i criteri di accettazione soddisfatti.
- Standards: risolta un'incoerenza tra ADR-0002 e l'implementazione (colonna `bank_selected` ridondante — il tagging della banca è stato spostato in `service.ingest_file`, unica fonte di verità, invece di essere hardcoded in ciascun parser); estratto un helper condiviso `type_from_sign` per eliminare la logica duplicata di segno→tipologia nei tre parser; reso il bootstrap del path Streamlit indipendente dalla profondità dei file.
