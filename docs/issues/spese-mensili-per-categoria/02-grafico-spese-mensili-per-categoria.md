# 02 — Nuovo grafico "Spese mensili per Categoria" impilato al 100%

**What to build:** Nella pagina Dashboard, sezione "Uscite per Categoria", subito sotto il bar chart esistente, un nuovo grafico mostra come le Uscite si distribuiscono tra le Categorie mese per mese: una colonna verticale per mese, impilata per Categoria e normalizzata al 100% (l'altezza mostra sempre le proporzioni tra Categorie in quel mese, non l'importo assoluto speso). Usa lo stesso filtro di date indipendente già presente nella sezione (nessun filtro proprio), esclude sempre il mese solare in corso (dati parziali, coerente con `get_monthly_totals`), e mostra sempre tutte le Categorie note (nessun bucket "Altro").

**Blocked by:** 01

**Status:** ready-for-agent

- [ ] Nuova funzione di servizio `get_monthly_category_breakdown(conn=None, date_from=None, date_to=None, today=None)`: aggrega le Uscite (esclusi Trasferimenti cross-bank ed Entrate) per (mese, Categoria) nel range di date indicato, esclude il mese solare corrente con lo stesso pattern già in uso in `get_monthly_totals` (parametro `today` iniettabile), restituisce una lista di dict `{"month": ..., "category": ..., "value": ...}` (una riga per ogni combinazione mese/Categoria con importo diverso da zero)
- [ ] Test per `get_monthly_category_breakdown`: raggruppamento corretto per mese/Categoria, esclusione Entrate e Trasferimenti, esclusione del mese corrente (tramite `today` iniettato), range vuoto → lista vuota
- [ ] Nuova funzione pura `domain.charts.monthly_category_breakdown_chart_data(breakdown: list[dict]) -> pd.DataFrame`: prende l'output di `get_monthly_category_breakdown`, restituisce un DataFrame in formato long con colonne Mese/Categoria/Totale (€)/Percentuale (la Percentuale è la quota della Categoria sul totale di quel singolo mese, non sul totale del periodo); con input vuoto restituisce un DataFrame vuoto
- [ ] Test per `monthly_category_breakdown_chart_data`: su un breakdown noto con almeno 2 mesi e almeno 2 Categorie per mese, Totale (€) e Percentuale corretti per ciascuna riga (Percentuale calcolata sul totale del mese, non del periodo); input vuoto → DataFrame vuoto
- [ ] Il grafico è reso con colonne verticali (una per mese, in ordine cronologico), impilate per Categoria con `stack` normalizzato al 100%
- [ ] Ogni Categoria mantiene lo stesso colore già in uso nel bar chart sovrastante (stesso meccanismo a scale esplicito domain/range, per evitare il bug di scrambling colori già scoperto e risolto nel grafico esistente)
- [ ] Il grafico mostra una legenda visibile con i colori delle Categorie (qui necessaria: l'asse mostra i mesi, non le Categorie)
- [ ] Il tooltip on-hover su un segmento mostra Mese, Categoria, Totale (€) e Percentuale
- [ ] Il grafico usa `category_date_from`/`category_date_to` già presenti nella sezione, nessun filtro data proprio
- [ ] Quando `get_monthly_category_breakdown` non restituisce righe, viene mostrato lo stesso messaggio informativo già usato dal bar chart sovrastante ("Nessuna Uscita nel periodo selezionato."), invece del grafico
- [ ] Verificato in browser: colonne mensili tutte della stessa altezza, segmenti colorati coerentemente col bar chart sovrastante, legenda leggibile, tooltip corretto su hover, mese corrente assente, filtro data della sezione invariato
