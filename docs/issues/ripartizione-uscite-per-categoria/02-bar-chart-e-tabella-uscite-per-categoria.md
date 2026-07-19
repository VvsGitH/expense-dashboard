# 02 — Bar chart orizzontale + tabella per "Uscite per Categoria"

**What to build:** Nella pagina "Dashboard", la sezione "Uscite per Categoria" mostra un bar chart orizzontale nativo di Streamlit (una barra per Categoria, ordinato per importo decrescente, con il colore per Categoria già in uso — corretto dal ticket `01`) al posto del grafico a torta matplotlib. Accanto al grafico, una tabella sempre visibile riporta Categoria, importo in € e percentuale sul totale delle Uscite del periodo selezionato. Il filtro di date indipendente della sezione e la logica di calcolo (`get_category_breakdown`) restano invariati.

**Blocked by:** 01

**Status:** ready-for-agent

- [ ] Nuova funzione pura `domain.charts.category_breakdown_table_data(breakdown: list[dict]) -> pd.DataFrame`: stesso input di `category_breakdown_chart_data` (output grezzo di `get_category_breakdown`), restituisce un DataFrame indicizzato per Categoria, ordinato per importo decrescente, con colonne per l'importo in € e la percentuale sul totale (somma di tutti gli importi in input); con input vuoto restituisce un DataFrame vuoto
- [ ] Test in `tests/test_charts.py` per `category_breakdown_table_data`: ordinamento decrescente, importo e percentuale corretti su un breakdown noto di almeno 3 categorie, e caso input vuoto → DataFrame vuoto
- [ ] Nella pagina Dashboard, il blocco matplotlib (`plt.subplots()` / `ax.pie(...)` / `st.pyplot(fig)`) è sostituito da `st.bar_chart` con `horizontal=True`, ordinamento decrescente per importo, e colore per Categoria tramite `category_colors`
- [ ] Sotto/accanto al bar chart, la tabella prodotta da `category_breakdown_table_data` è resa con `st.dataframe`
- [ ] Il tooltip on-hover del bar chart mostra il valore della barra (comportamento nativo di `st.bar_chart`, nessuna configurazione aggiuntiva richiesta)
- [ ] Il filtro di date indipendente della sezione continua a funzionare esattamente come oggi
- [ ] Quando non ci sono Uscite nel periodo selezionato, resta il messaggio informativo esistente ("Nessuna Uscita nel periodo selezionato."), invece di grafico e tabella vuoti
- [ ] Le chiavi dei widget data-range e le relative variabili Python, oggi `pie_date_from`/`pie_date_to`, sono rinominate (es. prefisso `category_` al posto di `pie_`) per riflettere che non è più un grafico a torta
- [ ] L'import `matplotlib.pyplot` è rimosso da `src/pages/dashboard.py` (nessun altro utilizzo nel file dopo questa modifica)
- [ ] La dipendenza `matplotlib` è rimossa da `requirements.txt`
- [ ] Verificato in browser: upload di Uscite in categorie diverse, bar chart con barre ordinate per importo decrescente e colori distinti, tabella affiancata coerente con i valori del grafico, tooltip on-hover funzionante, filtro data indipendente della sezione invariato
