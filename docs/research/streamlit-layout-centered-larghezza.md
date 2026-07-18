# Come si definisce/modifica la larghezza del blocco centrato in Streamlit quando layout="centered"?

Risposta breve: **non esiste** un modo ufficiale supportato (né parametro di `set_page_config`, né opzione `[theme]` in `config.toml`) per configurare la larghezza del blocco centrato in Streamlit 1.59.2. La larghezza è un valore fisso (736px) cablato nel tema di default del frontend, non esposto via API pubblica Python. La soluzione praticata e raccomandata dalla community (avallata anche in thread ufficiali del forum Streamlit) è **CSS custom** iniettato via `st.markdown(..., unsafe_allow_html=True)`.

## 1. Come funziona oggi il layout "centered"

La firma pubblica di `st.set_page_config` — verificata sia nel sorgente locale installato (`D:\MyProjects\Scripting\extract_expenses\venv\Lib\site-packages\streamlit\commands\page_config.py`, righe 112-119) sia sulla pagina ufficiale [docs.streamlit.io/develop/api-reference/configuration/st.set_page_config](https://docs.streamlit.io/develop/api-reference/configuration/st.set_page_config) — è:

```python
def set_page_config(
    page_title: str | None = None,
    page_icon: PageIcon | None = None,
    layout: Layout | None = None,          # Literal["centered", "wide"]
    initial_sidebar_state: InitialSideBarState | None = None,
    menu_items: MenuItems | None = None,
) -> None:
```

La documentazione ufficiale descrive i due valori di `layout` testualmente così:

| Valore | Descrizione ufficiale |
|---|---|
| `"centered"` | *"Page elements are constrained to a centered column of fixed width."* |
| `"wide"` | *"Page elements use the entire screen width."* |

Nessuno dei due valori accetta un numero o una stringa parametrica: sono letteralmente solo due preset booleani, confermato sia dal sorgente locale sia dalla pagina API ufficiale.

La larghezza fissa del preset `"centered"` è definita nel tema di base del frontend React, non in Python. Nel bundle JS installato in questo repo (`D:\MyProjects\Scripting\extract_expenses\venv\Lib\site-packages\streamlit\static\static\js\utils.paqmDQdB.js`) risulta:

```js
contentMaxWidth: "736px",
wideSidePadding: "5rem"
```

Lo stesso token è verificabile nel sorgente pubblico non minificato su GitHub, file [`frontend/lib/src/theme/primitives/sizes.ts`](https://github.com/streamlit/streamlit/blob/develop/frontend/lib/src/theme/primitives/sizes.ts):

```ts
contentMaxWidth: "736px",   // "Use px here since we want to keep the width the same regardless of the root font size"
wideSidePadding: "5rem",
```

Il commento nel sorgente spiega esplicitamente perché è in `px` e non in `rem`: la larghezza del blocco centrato deve restare fissa a 736px indipendentemente dal font size della root, per cui non è nemmeno influenzabile tramite `baseFontSize` in `[theme]`.

## 2. Esiste un parametro ufficiale per configurare questa larghezza?

**No.** Verificato su tre fronti indipendenti:

| Punto di verifica | Esito |
|---|---|
| Parametri di `st.set_page_config` (docs ufficiali + sorgente locale) | Solo `page_title`, `page_icon`, `layout` (`"centered"`/`"wide"`/`None`), `initial_sidebar_state`, `menu_items`. Nessun parametro `width` o simile. |
| Opzioni `[theme]` in `config.toml` (pagina ufficiale [docs.streamlit.io/develop/api-reference/configuration/config.toml](https://docs.streamlit.io/develop/api-reference/configuration/config.toml)) | `base`, `primaryColor`, `backgroundColor`, `secondaryBackgroundColor`, `textColor`, `linkColor`, `codeTextColor`/`codeBackgroundColor`, i colori base (`redColor`, `orangeColor`, ecc.), `font`/`headingFont`, `baseFontSize`, `baseFontWeight`, `baseRadius`/`buttonRadius`, `borderColor`, `chartCategoricalColors`/`chartSequentialColors`/`chartDivergingColors`, `showSidebarBorder`. Nessuna opzione relativa a larghezza del contenuto. |
| Changelog ufficiale ([docs.streamlit.io/develop/quick-reference/changelog](https://docs.streamlit.io/develop/quick-reference/changelog), versione più recente esaminata 1.59.0, 6 luglio 2026) | Nessuna voce relativa a `contentMaxWidth`, "content width", "layout width" o modifiche al comportamento di `centered`/`wide`. |

C'è una sola eccezione, non pertinente alla domanda ma degna di nota: da Streamlit recente `initial_sidebar_state` accetta anche un valore `int`, con vincolo *"The width must be between 200 and 600 pixels, inclusive."* — ma questo controlla la larghezza iniziale della **sidebar**, non del blocco centrato del contenuto principale.

La richiesta di una larghezza configurabile per il layout è un **feature request aperto e non implementato** nel repository ufficiale: [streamlit/streamlit#5466 "Customisable layout sizes"](https://github.com/streamlit/streamlit/issues/5466), stato **open**, etichettato `area:layout`, `feature:st.set_page_config`, `type:enhancement`, senza risposta di roadmap da parte del team Streamlit al momento della verifica (2026-07-18). Esiste anche una issue correlata più ampia, [streamlit/streamlit#708 "Responsive / Adaptive Widths & Sizes"](https://github.com/streamlit/streamlit/issues/708), sullo stesso tema di fondo.

## 3. Soluzione pratica raccomandata: CSS custom

In assenza di un parametro ufficiale, la soluzione che la community e i thread del forum ufficiale Streamlit (`discuss.streamlit.io`, gestito da Streamlit Inc.) raccomandano è iniettare CSS custom via `st.markdown(..., unsafe_allow_html=True)` mirato al contenitore principale.

**Attenzione alla versione**: il selettore CSS è cambiato tra le versioni. Il thread del forum ufficiale ["CSS for Controlling App Width No Longer Works in Streamlit 1.40"](https://discuss.streamlit.io/t/css-for-controlling-app-width-no-longer-works-in-streamlit-1-40/86205) (forum ufficiale Streamlit) documenta che il vecchio selettore basato su classi CSS ha smesso di funzionare a partire dalla 1.40, perché la classe `.main` è stata sostituita da `.stMain` nel markup del frontend. Il selettore aggiornato, valido da 1.40 in poi (quindi coerente con questo repo su 1.59.2), è:

```python
import streamlit as st

st.markdown(
    """
    <style>
    section[data-testid="stMain"] > div[data-testid="stMainBlockContainer"] {
        max-width: 900px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
```

Questo è coerente con quanto già osservato nel bundle JS locale (`D:\MyProjects\Scripting\extract_expenses\venv\Lib\site-packages\streamlit\static\static\js\index.D7cltBCg.js`), dove il contenitore principale espone sia la classe `block-container` sia l'attributo `data-testid="stMainBlockContainer"`:

```
className:`stMainBlockContainer block-container`, "data-testid":`stMainBlockContainer`
```

Il selettore basato su `data-testid` è quello raccomandato perché più stabile: gli attributi `data-testid` sono pensati esplicitamente per essere target stabili (usati anche nei test), a differenza dei nomi di classe CSS che sono cambiati almeno una volta (1.40) e potrebbero cambiare ancora.

Una variante alternativa, per allargare solo una sezione invece che tutto il blocco, discussa nel thread ufficiale del forum ["How to Set Custom Width for Specific Sections in Streamlit App"](https://discuss.streamlit.io/t/how-to-set-custom-width-for-specific-sections-in-streamlit-app/84288): impostare `layout="wide"` globalmente e poi usare `st.columns` per "restringere" artificialmente le sezioni che devono restare a larghezza normale, invece di provare a "allargare" sezioni dentro un layout `"centered"`:

```python
st.set_page_config(layout="wide")

def st_normal():
    _, col, _ = st.columns([1, 2, 1])
    return col

with st_normal():
    st.write("Questo contenuto resta a larghezza 'normale'")
```

Questo approccio evita del tutto il CSS custom, ma inverte il problema (parte da `"wide"` e restringe, invece di partire da `"centered"` e allargare).

## 4. Differenze comportamentali "centered" vs "wide" rilevanti

Dal bundle JS locale (`utils.paqmDQdB.js` + `index.D7cltBCg.js`), il componente styled che genera lo stile del contenitore applica in sintesi:

```js
maxWidth: c.sizes.contentMaxWidth, ...(isWideMode && KU(c))
```

dove per `layout="wide"`, sopra un breakpoint di viewport, la funzione `KU` rimuove il vincolo di larghezza massima e applica invece un padding laterale fisso:

```js
KU = e => ({
  [`@media (min-width: calc(${e.sizes.contentMaxWidth} + 2 * (${e.sizes.wideSidePadding} - ${e.spacing.lg})))`]: {
    paddingLeft: e.sizes.wideSidePadding,
    paddingRight: e.sizes.wideSidePadding
  },
  minWidth: `auto`,
  maxWidth: `initial`
})
```

| Layout | Comportamento sotto il breakpoint | Comportamento sopra il breakpoint |
|---|---|---|
| `"centered"` | `max-width: 736px`, sempre | `max-width: 736px`, sempre (nessun breakpoint applicabile: il vincolo è statico) |
| `"wide"` | Si comporta come "centered" (viewport troppo stretto per beneficiare della modalità wide) | `max-width: initial` (nessun limite), `min-width: auto`, padding laterale fisso a `5rem` (`wideSidePadding`) |

In pratica: `"wide"` non è "una larghezza diversa" ma "nessun limite di larghezza oltre un certo breakpoint, con padding laterale fisso invece di un max-width fisso". Questo spiega perché in `"wide"` il contenuto si adatta alla finestra invece di restare fisso a un valore in pixel.

## 5. Nota sulla versione usata in questo repo

Tutte le evidenze di codice sorgente citate sopra (percorso file, valori `736px`/`5rem`, classi/attributi del container) sono state estratte direttamente dal pacchetto `streamlit==1.59.2` — pin in `requirements.txt` riga 7 — installato in questo stesso repo in `D:\MyProjects\Scripting\extract_expenses\venv\Lib\site-packages\streamlit\`. Non è quindi necessario extrapolare da altre versioni: sono le stesse identiche stringhe/valori che l'app di questo repo (`src/pages/carica_dati.py`, `src/pages/dashboard.py`, entrambe con `st.set_page_config(..., layout="centered")`) sta effettivamente eseguendo oggi. Il selettore CSS raccomandato nella sezione 3 (`section[data-testid="stMain"] > div[data-testid="stMainBlockContainer"]`) è verificato come valido per versioni ≥ 1.40, quindi pienamente applicabile alla 1.59.2 di questo repo.

## Riepilogo

| Cosa | Configurabile ufficialmente? | Dove agire |
|---|---|---|
| Scegliere tra due preset di layout (`"centered"` fisso a 736px vs `"wide"` senza limite) | Sì | `st.set_page_config(layout=...)` |
| Impostare un valore numerico di larghezza per il blocco centrato | No | Nessun parametro pubblico esiste; feature request aperta ([#5466](https://github.com/streamlit/streamlit/issues/5466)) |
| Impostare la larghezza via `[theme]` in `config.toml` | No | Nessuna chiave `[theme]` relativa a larghezza esiste |
| Impostare la larghezza iniziale della sidebar (200-600px) | Sì (diverso dal blocco centrato) | `st.set_page_config(initial_sidebar_state=<int>)` |
| Allargare/restringere il blocco centrato in pratica | Sì, non ufficiale | CSS custom via `st.markdown(unsafe_allow_html=True)` su `[data-testid="stMainBlockContainer"]`, oppure invertire il problema con `layout="wide"` + `st.columns` di contenimento |
