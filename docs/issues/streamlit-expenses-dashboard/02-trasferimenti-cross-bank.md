# 02 — Rilevamento trasferimenti cross-bank + cache derivata

**What to build:** Dopo un caricamento (o all'avvio dell'app), il sistema individua automaticamente le coppie di Transazioni che rappresentano Trasferimenti cross-bank (stesso importo, Banche diverse, entro 7 giorni) e le materializza in una tabella cache separata, ispezionabile per debug senza inquinare la tabella Transazioni grezza.

**Blocked by:** 01

**Status:** ready-for-agent

- [ ] Le coppie di Transazioni con stesso importo, Banche diverse, e date entro 7 giorni vengono classificate come Trasferimento cross-bank (stessa logica del notebook attuale)
- [ ] I Trasferimenti rilevati sono salvati in una tabella cache separata (`cross_bank_transfers`) che referenzia le Transazioni coinvolte, senza duplicare o modificare la tabella Transazioni grezza
- [ ] La cache viene ricostruita interamente (truncate + rebuild) ad ogni nuovo Caricamento e ad ogni avvio dell'app — mai accumulata in modo incrementale
- [ ] La cache è consultabile per verificare quali coppie sono state classificate come Trasferimento, a scopo di debug
- [ ] Test automatici verificano che coppie che rispettano i criteri vengano rilevate, e che coppie che non li rispettano (stessa banca, oltre 7 giorni, importo diverso) non vengano rilevate
