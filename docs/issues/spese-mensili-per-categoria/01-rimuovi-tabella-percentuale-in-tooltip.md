# 01 — Rimuovi tabella "Uscite per Categoria", sposta percentuale nel tooltip

**What to build:** Nella pagina Dashboard, sezione "Uscite per Categoria", la tabella sotto il bar chart sparisce. La percentuale sul totale, che oggi vive solo nella tabella, compare invece nel tooltip on-hover del bar chart, accanto a Categoria e Totale (€) già presenti — nessuna informazione viene persa, solo consolidata nel tooltip. La funzione `category_breakdown_table_data`, diventata inutilizzata, viene rimossa insieme ai suoi test.

**Blocked by:** Nessuno — può partire subito

**Status:** done

- [x] Il tooltip del bar chart mostra Categoria, Totale (€) e Percentuale (la Percentuale è la quota della Categoria sul totale delle Uscite del periodo selezionato, la stessa già calcolata oggi dalla tabella)
- [x] La tabella sotto il bar chart non viene più renderizzata
- [x] `domain.charts.category_breakdown_table_data` è rimossa dal modulo
- [x] I 2 test esistenti per `category_breakdown_table_data` in `tests/test_charts.py` sono rimossi
- [x] Il resto della sezione (filtro data indipendente, colori per Categoria, ordinamento decrescente, stato vuoto "Nessuna Uscita nel periodo selezionato.") resta invariato
- [x] Verificato in browser: hover su una barra mostra Categoria/Totale (€)/Percentuale corretti, nessuna tabella visibile sotto il grafico

## Comments

Implementato rimuovendo `category_breakdown_table_data` da `src/domain/charts.py` e i suoi 2 test da `tests/test_charts.py`, e aggiungendo la Percentuale al tooltip del bar chart esistente in `src/pages/dashboard.py`.

Code review a due assi: Spec pulita (nessuna lacuna, nessuno scope creep). Standards ha segnalato 1 hard violation, risolta: il calcolo della percentuale era stato scritto inline in `dashboard.py`, in contrasto con la convenzione già documentata (Testing Decisions in `spec.md`) per cui ogni funzione di shaping dei grafici della dashboard vive come funzione pura testata in `domain/charts.py`, mai come logica nella pagina Streamlit — estratta `category_breakdown_percentages(totals: pd.Series) -> pd.Series` con un test dedicato, e sostituito il join posizionale (`.values`) con un `.map()` esplicito sulla colonna Categoria per evitare un accoppiamento implicito sull'ordine delle righe.

Verificato in browser (Streamlit dev server, dati reali già presenti nel DB), sia via screenshot sia via ispezione dell'accessibility tree del grafico Vega: il tooltip mostra Categoria/Totale (€)/Percentuale (%) corretti per tutte le 11 categorie, nessuna tabella visibile sotto il grafico, resto della sezione (filtro data, colori, ordinamento, stato vuoto) invariato.
