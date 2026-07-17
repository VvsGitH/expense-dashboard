# 02 — Rilevamento trasferimenti cross-bank + cache derivata

**What to build:** Dopo un caricamento (o all'avvio dell'app), il sistema individua automaticamente le coppie di Transazioni che rappresentano Trasferimenti cross-bank (stesso importo, Banche diverse, entro 7 giorni) e le materializza in una tabella cache separata, ispezionabile per debug senza inquinare la tabella Transazioni grezza.

**Blocked by:** 01

**Status:** done

- [x] Le coppie di Transazioni con stesso importo, Banche diverse, e date entro 7 giorni vengono classificate come Trasferimento cross-bank (stessa logica del notebook attuale)
- [x] I Trasferimenti rilevati sono salvati in una tabella cache separata (`cross_bank_transfers`) che referenzia le Transazioni coinvolte, senza duplicare o modificare la tabella Transazioni grezza
- [x] La cache viene ricostruita interamente (truncate + rebuild) ad ogni nuovo Caricamento e ad ogni avvio dell'app — mai accumulata in modo incrementale
- [x] La cache è consultabile per verificare quali coppie sono state classificate come Trasferimento, a scopo di debug
- [x] Test automatici verificano che coppie che rispettano i criteri vengano rilevate, e che coppie che non li rispettano (stessa banca, oltre 7 giorni, importo diverso) non vengano rilevate

## Comments

Implementato con TDD sul modulo `transfers.py` (6 test, tutti verdi): rilevamento diretto (coppia valida, stessa banca, oltre 7 giorni, importo diverso, rebuild non incrementale) più un test di integrazione che verifica il trigger da `ingest_file`. Rebuild agganciato anche all'avvio di `Dashboard.py`. `undo_upload` (ticket 03, non ancora implementato) dovrà anch'esso richiamare `transfers.rebuild_cache` una volta introdotto. Code review a due assi: nessuna violazione hard su Standards né lacune su Spec.
