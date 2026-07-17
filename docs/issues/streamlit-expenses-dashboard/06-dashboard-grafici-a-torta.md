# 06 — Dashboard: sezione grafici a torta per categoria

**What to build:** Nella pagina "Dashboard", una sezione con grafici a torta mostra la ripartizione delle Uscite per Categoria (calcolata al volo dalle regole di fuzzy-matching correnti), al netto dei Trasferimenti cross-bank, con un proprio filtro di range di date indipendente dalle altre sezioni.

**Blocked by:** 01, 02

**Status:** done

- [x] Le regole di categorizzazione (`EXP_CATEGORIES` e la funzione di scoring fuzzy) sono portate in un modulo importabile, riusando la logica già presente nel notebook
- [x] La Categoria di ogni Uscita è calcolata al volo al momento della query, non persistita nel DB
- [x] I grafici a torta mostrano la ripartizione delle Uscite per Categoria nel range di date selezionato
- [x] Le Transazioni classificate come Trasferimento cross-bank sono escluse dal calcolo della ripartizione
- [x] Il range di date dei grafici a torta è configurabile ed è indipendente dai filtri delle altre sezioni della dashboard
- [x] Una modifica alle regole di categorizzazione nel modulo Python si riflette immediatamente in `get_category_breakdown` (riavviando il dev server), senza bisogno di ricalcolo esplicito
- [x] Test automatici verificano `get_category_breakdown` rispetto a regole di categorizzazione note e al proprio range di date

## Comments

Portate `EXP_CATEGORIES` e `categorize_description` dal notebook in `app/categorization.py` (porting fedele, verificato codepoint per codepoint contro il notebook — inclusa la "à" di "elettricità"). Implementato con TDD `service.get_category_breakdown` (6 test, tutti verdi): esclusione Entrate, esclusione Trasferimenti cross-bank (via la cache già esistente), range di date indipendente, e verifica che una modifica a `EXP_CATEGORIES` a runtime si rifletta immediatamente (nessuno stato persistito da invalidare). Grafico a torta reso con matplotlib (`st.pyplot`), riusando i colori per Categoria già definiti nel notebook. Verificato end-to-end in browser: upload di Uscite in categorie diverse, grafico a torta con percentuali e colori corretti, Entrate correttamente escluse.

Code review a due assi: Spec senza lacune. Standards ha segnalato due judgement call, entrambi risolti: estratto un helper `_read_non_transfer_transactions` condiviso tra `get_monthly_totals` e `get_category_breakdown` per eliminare la duplicazione di "leggi transazioni, escludi Trasferimenti, filtra per range date"; spostata la mappatura colore-per-categoria da `Dashboard.py` (Feature Envy su `charts.CATEGORY_COLORS`) a una funzione `charts.category_colors`, mantenendo la pagina un guscio sottile come le altre due sezioni.
