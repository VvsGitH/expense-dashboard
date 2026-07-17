---
status: accepted
---

# Routing multipage app con st.Page/st.navigation invece della cartella pages/ magica

Streamlit auto-scopre le pagine in una cartella `pages/` accanto all'entrypoint, ordinandole per prefisso numerico nel nome file, e richiede che l'entrypoint stesso resti fuori da `pages/`. Riorganizzando il progetto in `pages/domain/repository/ingestion`, volevamo che ogni pagina — dashboard inclusa — vivesse in `pages/` con nomi semplici e senza prefissi, e che l'ordine fosse esplicito invece che codificato nel nome del file. L'API `st.Page` + `st.navigation` (stabile da Streamlit 1.36, confermata contro la 1.59.2 installata) supporta questo direttamente: un singolo entrypoint `router.py` costruisce gli oggetti `st.Page(...)` per ogni pagina e chiama `st.navigation([...]).run()`, così `pages/` può contenere tutte le pagine in modo uniforme senza il vincolo del prefisso numerico né un file entrypoint "speciale".
