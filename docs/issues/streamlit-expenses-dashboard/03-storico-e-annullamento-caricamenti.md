# 03 — Storico caricamenti e annullamento

**What to build:** Nella pagina "Carica dati", l'utente vede l'elenco dei Caricamenti effettuati (data, Banca, nome file, numero di Transazioni inserite) e può annullare un Caricamento, rimuovendo tutte le Transazioni di quel batch e aggiornando di conseguenza la cache dei Trasferimenti cross-bank — utile se ha selezionato la Banca sbagliata o caricato il file sbagliato per errore.

**Blocked by:** 01, 02

**Status:** ready-for-agent

- [ ] La pagina "Carica dati" mostra lo storico dei Caricamenti effettuati (data, Banca, nome file, numero di Transazioni inserite)
- [ ] Per ciascun Caricamento è disponibile un'azione di annullamento
- [ ] Annullare un Caricamento (`undo_upload`) rimuove esattamente le Transazioni di quel batch e nessun'altra
- [ ] L'annullamento forza il rebuild della cache dei Trasferimenti cross-bank
- [ ] Test automatici verificano che `undo_upload` rimuova solo le Transazioni del batch indicato e triggeri il rebuild della cache
