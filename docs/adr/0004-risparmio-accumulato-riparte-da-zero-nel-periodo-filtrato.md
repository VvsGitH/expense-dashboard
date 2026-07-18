---
status: accepted
---

# Risparmio teorico accumulato riparte da zero nel periodo filtrato, non dall'inizio dello storico

La sotto-sezione "Andamento risparmi" mostra, oltre alla Differenza mensile, la sua somma cumulata mese per mese (Risparmio teorico accumulato). Quando l'utente restringe il periodo con `bar_date_from`/`bar_date_to`, la cumulata riparte da zero al primo mese visibile nel filtro, invece di riflettere l'accumulo di tutti i mesi precedenti anche se non mostrati. La scelta segue lo stesso principio già adottato da ogni altra funzione della dashboard (`get_monthly_totals`, `get_monthly_cashflow_summary`, `get_category_breakdown`): operare esclusivamente sul sottoinsieme di Transazioni nel range filtrato, senza mai interrogare dati fuori da quel range. L'alternativa — accumulare da tutta la storia e mostrare solo la finestra filtrata — sarebbe più fedele al significato letterale di "risparmi accumulati", ma richiederebbe una query separata e non filtrata solo per calcolare il punto di partenza, introducendo un'eccezione al pattern usato ovunque nella dashboard. Conseguenza esplicita: il grafico mostra l'accumulo *relativo al periodo scelto*, non un vero saldo di risparmio "da sempre" — cambiare il filtro data cambia il punto di partenza della cumulata.
