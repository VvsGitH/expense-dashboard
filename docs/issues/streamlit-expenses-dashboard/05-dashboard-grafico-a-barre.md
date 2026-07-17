# 05 — Dashboard: sezione grafico a barre mensile

**What to build:** Nella pagina "Dashboard", una sezione con un grafico a barre mostra Entrate e Uscite aggregate mensilmente, al netto dei Trasferimenti cross-bank, con un proprio filtro di range di date indipendente dalle altre sezioni.

**Blocked by:** 01, 02

**Status:** done

- [x] Il grafico a barre mostra Entrate e Uscite aggregate per mese
- [x] I totali mensili escludono le Transazioni classificate come Trasferimento cross-bank
- [x] Il range di date del grafico è configurabile ed è indipendente dai filtri delle altre sezioni della dashboard
- [x] Test automatici verificano che `get_monthly_totals` escluda correttamente i Trasferimenti e rispetti il proprio range di date

## Comments

Implementato con TDD sul seam `service.get_monthly_totals` (4 test, tutti verdi): aggregazione mensile di Entrate/Uscite, esclusione delle Transazioni che sono una gamba di un Trasferimento cross-bank rilevato (via `transfers.get_transfer_leg_ids`, che legge la cache già costruita da `rebuild_cache`), range di date indipendente dalla sezione tabella. Grafico a barre reso con `st.bar_chart` nativo di Streamlit (`stack=False`, per non sommare Entrate e Uscite che sono serie indipendenti). Verificato end-to-end in browser: upload di un Caricamento Poste + un Caricamento BBVA che forma un Trasferimento cross-bank, confermato che il grafico esclude il mese del solo Trasferimento mentre la tabella (ticket 04) continua a mostrarlo.

Code review a due assi: Spec senza lacune. Standards ha segnalato una violazione reale — la spec assegna la preparazione dei DataFrame per i grafici a un "Modulo grafici" separato dalle pagine, mentre il reshaping (`pd.DataFrame(...).rename(...).set_index(...)`) viveva inline in `Dashboard.py`, non testato — estratto in un nuovo modulo `app/charts.py` (`monthly_totals_chart_data`, con test dedicato). Applicati anche due judgement call: rinominata `transfers.get_transaction_ids` in `get_transfer_leg_ids` per chiarezza, ed estratto un helper `_filter_date_range` condiviso tra `get_transactions` e `get_monthly_totals` per eliminare la duplicazione del filtro per range di date.
