# 03 — Storico caricamenti e annullamento

**What to build:** Nella pagina "Carica dati", l'utente vede l'elenco dei Caricamenti effettuati (data, Banca, nome file, numero di Transazioni inserite) e può annullare un Caricamento, rimuovendo tutte le Transazioni di quel batch e aggiornando di conseguenza la cache dei Trasferimenti cross-bank — utile se ha selezionato la Banca sbagliata o caricato il file sbagliato per errore.

**Blocked by:** 01, 02

**Status:** done

- [x] La pagina "Carica dati" mostra lo storico dei Caricamenti effettuati (data, Banca, nome file, numero di Transazioni inserite)
- [x] Per ciascun Caricamento è disponibile un'azione di annullamento
- [x] Annullare un Caricamento (`undo_upload`) rimuove esattamente le Transazioni di quel batch e nessun'altra
- [x] L'annullamento forza il rebuild della cache dei Trasferimenti cross-bank
- [x] Test automatici verificano che `undo_upload` rimuova solo le Transazioni del batch indicato e triggeri il rebuild della cache

## Comments

Implementato con TDD sul seam `service.undo_upload` / `service.list_uploads` (3 test, tutti verdi): rimozione isolata al solo `upload_id` indicato, rebuild forzato della cache Trasferimenti, e storico caricamenti con conteggio corretto. Pagina "Carica dati" estesa con storico e azione di annullamento per riga. Code review a due assi: Spec senza lacune; Standards ha segnalato due judgement call risolti prima del commit — `Upload` ora costruito con keyword arg espliciti invece di `Upload(**row)` (evita fragilità su drift di colonne e scalari numpy), e il messaggio di conferma dopo l'annullamento ora sopravvive al rerun tramite `st.session_state` invece di essere scartato da `st.rerun()`.
