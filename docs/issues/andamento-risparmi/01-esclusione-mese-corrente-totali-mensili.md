# 01 — Esclusione del mese corrente dai totali mensili

**What to build:** Nella pagina "Dashboard", il grafico a barre della sotto-sezione "Andamento mese per mese" smette di mostrare il mese solare in corso (dati parziali), coerentemente con quanto già fa "Flusso di cassa mensile". `service.get_monthly_totals` accetta un parametro `today` iniettabile, sullo stesso pattern già usato da `service.get_monthly_cashflow_summary`, e usa quel valore (o la data di sistema se non passato) per escludere il mese corrente dal risultato aggregato.

**Blocked by:** Nessuno — può partire subito.

**Status:** done

- [x] `service.get_monthly_totals` accetta un parametro `today: pd.Timestamp | None = None`; se non passato, usa la data di sistema
- [x] Il mese solare corrente (determinato da `today`), se presente tra i mesi aggregati, viene escluso dal risultato di `get_monthly_totals`
- [x] I 4 test esistenti in `tests/test_get_monthly_totals.py` restano verdi (aggiornati per pinnare esplicitamente `today`, vedi Comments)
- [x] Nuovo test in `tests/test_get_monthly_totals.py` (pattern analogo a `test_excludes_current_month_from_the_calculation` in `tests/test_get_monthly_cashflow_summary.py`) verifica che, iniettando un `today` di test, un mese con dati presente tra quelli aggregati ma coincidente con `today` viene escluso dal risultato
- [x] Verificato manualmente in browser che il grafico a barre "Andamento mese per mese" non mostra più il mese in corso

## Comments

Implementato con TDD sul seam `service.get_monthly_totals`: aggiunto il parametro `today` iniettabile, stesso pattern già usato da `get_monthly_cashflow_summary` (`(today or pd.Timestamp.now()).strftime("%Y-%m")` + `.drop(index=current_month, errors="ignore")`). Suite completa verde (54 test). Verificato manualmente in browser: l'app carica senza errori e il grafico a barre mostra come ultimo mese 2026-06 (coerente con l'esclusione di 2026-07, mese corrente); il DB reale non ha ancora transazioni nel mese corrente, quindi la differenza di comportamento non era osservabile ad occhio sui dati reali — la copertura sostanziale resta nei test automatici con `today` iniettato.

Code review a due assi: Spec senza lacune (nessuno scope creep, nessun requisito implementato in modo sbagliato). Standards ha segnalato un'inconsistenza reale — in `test_get_monthly_cashflow_summary.py` ogni test pinna esplicitamente `today=`, anche quelli non legati al mese corrente, per non far mai dipendere un test da `pd.Timestamp.now()`; i 3 test preesistenti in `test_get_monthly_totals.py` non lo facevano. Corretto aggiungendo `today=pd.Timestamp("2024-06-15")` a tutti e 3 (deviando quindi dal criterio originale "senza modifiche", ma allineando il file alla convenzione già stabilita dal file gemello). Aggiunta anche una docstring a `get_monthly_totals` ("current month always excluded"), allineandola a `get_monthly_cashflow_summary` che già la documentava.
