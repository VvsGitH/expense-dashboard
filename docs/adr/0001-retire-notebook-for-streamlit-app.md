---
status: accepted
---

# Ritiro del notebook a favore di una webapp Streamlit

Il progetto era organizzato attorno a `src/notebook.ipynb`, che copriva insieme ingestion, elaborazione ed esplorazione visuale dei dati. Passando a una dashboard Streamlit locale, il notebook viene ritirato del tutto anziché mantenuto come strumento di esplorazione affiancato all'app: tutta la logica (ingestion, categorizzazione, aggregazioni) viene estratta in moduli `.py` riutilizzabili, e l'iterazione — inclusa quella sulle regole di categorizzazione fuzzy — avviene tramite il dev server di Streamlit (hot-reload su salvataggio) invece che rieseguendo celle. La scelta è deliberata: un notebook mantenuto in parallelo rischierebbe di divergere dai moduli condivisi, e il dev server offre già un ciclo di feedback rapido equivalente per questo caso d'uso.
