# 01 — Layout centered con larghezza massima 1024px

**What to build:** Le pagine "Carica dati" e "Dashboard" usano il layout `centered` di Streamlit, ma con una larghezza massima del blocco di contenuto di 1024px invece del default di 736px — così tabelle e grafici hanno più respiro orizzontale, restando comunque centrati anziché occupare l'intera larghezza dello schermo (comportamento di `layout="wide"`).

**Blocked by:** None — può partire subito

**Status:** done

- [x] `st.set_page_config(layout="centered")` impostato sia in "Carica dati" sia in "Dashboard" (già fatto manualmente, da tracciare in questo ticket)
- [x] Il blocco di contenuto centrato ha `max-width: 1024px` su entrambe le pagine (Streamlit non espone un parametro ufficiale per questo — vedi `docs/research/streamlit-layout-centered-larghezza.md` per l'approccio via CSS custom mirato a `data-testid="stMainBlockContainer"`)
- [x] Verificato visivamente in browser che il contenuto resti centrato e leggibile alla nuova larghezza, su entrambe le pagine

## Comments

Implementato iniettando lo stesso blocco CSS (`st.markdown(..., unsafe_allow_html=True)`) subito dopo `st.set_page_config` in entrambe le pagine, mirato a `section[data-testid="stMain"] > div[data-testid="stMainBlockContainer"]` con `max-width: 1024px`, come raccomandato in `docs/research/streamlit-layout-centered-larghezza.md`. Verificato in browser (chrome devtools) su entrambe le pagine: `getComputedStyle(...).maxWidth` e larghezza renderizzata risultano esattamente `1024px`. Suite di test invariata (53 passed) — nessuna logica applicativa toccata.

Code review a due assi: Standards e Spec entrambi senza violazioni hard. Unico rilievo condiviso da entrambi gli assi (judgement call, non bloccante): il blocco CSS di 10 righe è duplicato identico in `carica_dati.py` e `dashboard.py` — da estrarre in un helper condiviso solo se una terza pagina adotta lo stesso pattern.
