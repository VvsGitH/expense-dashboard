# Qual è il modo più diffuso per realizzare una web application con Python?

Non esiste un unico "modo standard": il panorama Python per il web si è consolidato attorno a tre framework dominanti per backend/API (Django, Flask, FastAPI) affiancati, per casi d'uso data-centrici come dashboard ed espansioni di progetti di analisi dati, da framework "pure-Python" che evitano di scrivere JavaScript (Streamlit, Dash, Gradio, NiceGUI, Reflex). Di seguito le categorie principali, con fonti ufficiali, e i dati di adozione reali reperiti da survey e statistiche PyPI ufficiali.

## 1. Framework full-stack: Django

[Django](https://www.djangoproject.com/) si definisce ufficialmente **"The web framework for perfectionists with deadlines"** ([djangoproject.com](https://www.djangoproject.com/)) — un framework "batteries included" con ORM, sistema di admin, autenticazione e templating integrati, pensato per applicazioni web complete lato server.

## 2. Micro-framework: Flask

[Flask](https://flask.palletsprojects.com/) è descritto nella documentazione ufficiale come **"a lightweight WSGI web application framework [...] designed to make getting started quick and easy, with the ability to scale up to complex applications"** ([flask.palletsprojects.com](https://flask.palletsprojects.com/en/stable/)). È un micro-framework: il core è minimale (routing, request/response) e le funzionalità aggiuntive (DB, form, auth) si aggiungono tramite estensioni.

## 3. Framework asincroni/API moderni: FastAPI e Starlette

[FastAPI](https://fastapi.tiangolo.com/) si presenta come **"a modern, fast (high-performance), web framework for building APIs with Python based on standard Python type hints"**, con prestazioni dichiarate **"on par with NodeJS and Go (thanks to Starlette and Pydantic)"** ([fastapi.tiangolo.com](https://fastapi.tiangolo.com/)). È costruito sopra due librerie: [Starlette](https://www.starlette.io/) per la parte web/ASGI (**"The little ASGI framework that shines"**, un **"lightweight ASGI framework/toolkit [...] ideal for building async web services in Python"**, [starlette.io](https://www.starlette.io/)) e Pydantic per la validazione dati.

## 4. Framework Python-puro per UI/dashboard (senza scrivere JS)

Categoria particolarmente rilevante per progetti di analisi dati come questo repo:

- **[Streamlit](https://streamlit.io/)**: **"A faster way to build and share data apps"**, con la promessa esplicita **"Turn your data scripts into shareable web apps in minutes. All in pure Python. No front‑end experience required"** ([streamlit.io](https://streamlit.io/)).
- **[Gradio](https://www.gradio.app/)**: **"Build machine learning apps in Python"**, per creare interfacce web attorno a modelli/script in pochi minuti ([gradio.app](https://www.gradio.app/)).
- **[NiceGUI](https://nicegui.io/)**: si definisce **"The Python UI framework that shows up in your browser"** ([nicegui.io](https://nicegui.io/)).
- **[Reflex](https://reflex.dev/)**: **"Open-source Python framework for building full-stack web apps in pure Python"** ([reflex.dev](https://reflex.dev/)).
- **[Dash](https://plotly.com/dash/)** (Plotly): si presenta come **"The most popular Python framework for analytical web apps"**, con approccio **"Pure Python reactive — Wire UI to Python. No HTML, CSS, or JavaScript"** ([plotly.com/dash](https://plotly.com/dash/), documentazione tecnica su [dash.plotly.com](https://dash.plotly.com/)).

## 5. Server WSGI/ASGI per il deployment

- **[Gunicorn](https://gunicorn.org/)**: **"Python WSGI HTTP Server for UNIX"**, descritto come "Battle-tested. Production-ready." ([gunicorn.org](https://gunicorn.org/)) — il server WSGI più comune per servire app Django/Flask in produzione.
- **[Uvicorn](https://www.uvicorn.org/)**: **"The lightning-fast ASGI server"**, un'implementazione ASGI (Asynchronous Server Gateway Interface) pensata per framework asincroni come FastAPI e Starlette (fonte: pagina ufficiale PyPI del progetto, [pypi.org/project/uvicorn](https://pypi.org/project/uvicorn/); il dominio uvicorn.org non è risultato raggiungibile al momento della ricerca).

## Dati di adozione/popolarità

### Python Developers Survey (JetBrains + Python Software Foundation)

Fonte primaria: [Python Developers Survey 2024](https://lp.jetbrains.com/python-developers-survey-2024/) (JetBrains + PSF, sondaggio condotto ottobre–novembre 2024, oltre 25.000 risposte valide), con confronto storico su [Python Developers Survey 2023](https://lp.jetbrains.com/python-developers-survey-2023/) e [Python Developers Survey 2022](https://lp.jetbrains.com/python-developers-survey-2022/).

Percentuali di utilizzo dei framework web tra gli sviluppatori Python (domanda a risposta multipla, quindi le percentuali non sommano a 100%):

| Framework | 2022 | 2023 | 2024 |
|---|---|---|---|
| Flask | 39% | 33% | 34% |
| Django | 39% | 33% | 35% |
| FastAPI | 25% | 29% | **38%** |
| Streamlit (sezione "web framework") | — | 8% | 12% |
| Starlette | — | 6% | 8% |
| Tornado | 4% | 3% | 2% |

**Osservazione chiave**: nel 2024, per la prima volta, FastAPI ha superato sia Flask che Django come framework web più usato in assoluto tra i Python developer intervistati, un'inversione di tendenza rispetto al 2022-2023 quando Flask e Django erano sostanzialmente appaiati e FastAPI era terzo.

Per gli strumenti di dashboard/visualizzazione (domanda separata "Libraries for creating dashboards"):

| Strumento | 2022 | 2023 | 2024 |
|---|---|---|---|
| Streamlit | 28% | 28% | 33% |
| Plotly Dash | 31% | 31% | 28% |
| Gradio | 12% | 12% | 11% |
| Panel | 12% | 12% | 10% |
| TensorBoard | — | — | 14% |
| Voilà | 4% | 4% | 4% |
| Nessuno | 26% | 26% | 28% |

Il blog ufficiale JetBrains ["The State of Python 2024"](https://blog.jetbrains.com/pycharm/2024/12/the-state-of-python/) conferma testualmente: *"There are three frameworks whose usage goes well beyond any others: Flask, Django, and FastAPI. They are nearly tied in usage"*, e segmenta l'uso per tipo di sviluppatore: **"63% of web developers use Django compared to 42% using Flask"**, mentre tra i data scientist Flask e FastAPI sono preferiti a Django (**36% e 31% contro 26%**) — un dato coerente con l'idea che, per progetti orientati ai dati, framework leggeri o pure-Python siano scelti più spesso di Django.

Nota metodologica: questi dati sono stati estratti dai grafici incorporati nelle pagine ufficiali del sondaggio tramite fetch automatico; il testo discorsivo dell'articolo JetBrains non riporta sempre le stesse percentuali esplicite nel corpo del testo (si concentra su tendenze), per cui le tabelle sopra si basano sui dati grezzi dei grafici della pagina sondaggio, incrociati su tre anni per coerenza interna (i valori sono risultati stabili su fetch ripetuti).

### Statistiche di download da PyPI (pypistats.org)

Fonte: [pypistats.org](https://pypistats.org), dati "recent downloads" rilevati il 17 luglio 2026:

| Pacchetto | Ultimo giorno | Ultima settimana | Ultimo mese |
|---|---|---|---|
| [django](https://pypistats.org/packages/django) | 2.221.267 | 12.528.195 | 50.285.742 |
| [flask](https://pypistats.org/packages/flask) | 7.958.072 | 48.441.505 | 200.715.680 |
| [fastapi](https://pypistats.org/packages/fastapi) | 21.305.563 | 121.146.376 | 502.786.405 |
| [streamlit](https://pypistats.org/packages/streamlit) | 1.091.701 | 6.866.167 | 27.178.290 |
| [gradio](https://pypistats.org/packages/gradio) | 523.440 | 3.366.221 | 14.335.967 |
| [uvicorn](https://pypistats.org/packages/uvicorn) | 22.025.466 | 133.661.981 | 538.614.715 |
| [gunicorn](https://pypistats.org/packages/gunicorn) | 5.248.986 | 30.701.013 | 126.751.010 |

**Attenzione all'interpretazione**: questi numeri misurano i *download* del pacchetto (inclusi quelli automatici da pipeline CI/CD, container Docker, mirror e installazioni ripetute), non il numero di "applicazioni create" né sviluppatori unici. I volumi altissimi di FastAPI e Uvicorn sono in parte spiegati dal fatto che sono dipendenze transitive di moltissimi altri pacchetti dell'ecosistema AI/ML (es. librerie che espongono API embedded), non solo di web app scritte direttamente dall'utente finale. Non ho trovato dati ufficiali su "download unici per sviluppatore" o simili — pypistats.org non fornisce questa metrica.

## Raccomandazione pratica

Matrice di scelta basata sulle caratteristiche ufficiali dei progetti e sui dati di adozione sopra riportati:

| Scenario | Scelta più comune/idiomatica | Perché |
|---|---|---|
| App web tradizionale con molte entità, utenti, admin, autenticazione | **Django** | Batteries-included: ORM, admin panel, auth pronti all'uso ([djangoproject.com](https://www.djangoproject.com/)); secondo JetBrains il 63% dei web developer lo usa ([blog.jetbrains.com](https://blog.jetbrains.com/pycharm/2024/12/the-state-of-python/)) |
| API REST leggera o microservizio semplice, poco boilerplate | **Flask** | Micro-framework minimale e flessibile, si aggiunge solo ciò che serve ([flask.palletsprojects.com](https://flask.palletsprojects.com/en/stable/)) |
| API moderna, con validazione automatica dei dati, documentazione OpenAPI automatica, necessità di performance/async | **FastAPI** | Framework col maggior tasso di crescita e ora il più usato in assoluto nel sondaggio 2024 (38%) ([lp.jetbrains.com](https://lp.jetbrains.com/python-developers-survey-2024/)); nativo su type hints e Pydantic ([fastapi.tiangolo.com](https://fastapi.tiangolo.com/)) |
| **Dashboard di analisi dati / reportistica personale (es. spese, grafici, tabelle) — caso più vicino a questo repo** | **Streamlit** (o Dash come alternativa) | Pensato esplicitamente per trasformare script di analisi dati in web app senza scrivere frontend ("All in pure Python. No front-end experience required", [streamlit.io](https://streamlit.io/)); tra gli strumenti dashboard è il più usato nel 2024 (33%, [lp.jetbrains.com](https://lp.jetbrains.com/python-developers-survey-2024/)); si integra naturalmente con pandas/matplotlib/plotly già presenti in un notebook Jupyter esistente |
| Dashboard analitiche più complesse, multi-pagina, con componenti grafici avanzati e maggiore controllo sul layout | **Dash (Plotly)** | "The most popular Python framework for analytical web apps" ([plotly.com/dash](https://plotly.com/dash/)); seconda scelta più usata per dashboard (28% nel 2024) |
| Demo rapida di un modello ML con input/output visuali | **Gradio** | Pensato specificamente per "Build machine learning apps in Python" ([gradio.app](https://www.gradio.app/)) |
| App con UI desktop-like nel browser, componenti interattivi custom, senza framework JS | **NiceGUI** o **Reflex** | Framework più recenti pure-Python, meno diffusi nei sondaggi ufficiali attuali (non ancora tracciati come categorie separate nel Python Developers Survey), ma con documentazione ufficiale chiara ([nicegui.io](https://nicegui.io/), [reflex.dev](https://reflex.dev/)) |
| Messa in produzione di un'app Django/Flask (sincrona, WSGI) | **Gunicorn** | Standard de facto per servire app WSGI in produzione ([gunicorn.org](https://gunicorn.org/)) |
| Messa in produzione di un'app FastAPI/Starlette (asincrona, ASGI) | **Uvicorn** | Server ASGI di riferimento, "lightning-fast" ([pypi.org/project/uvicorn](https://pypi.org/project/uvicorn/)) |

**Per un progetto come questo repository** (estrazione ed elaborazione di spese bancarie da notebook Jupyter, con pandas e grafici già presenti), l'opzione più idiomatica e a più basso attrito per aggiungere un frontend web è **Streamlit**: permette di riusare direttamente le funzioni pandas/matplotlib/plotly esistenti, non richiede di scrivere HTML/CSS/JS, ed è lo strumento per dashboard più diffuso secondo l'ultimo Python Developers Survey ufficiale. Se in futuro servisse un'API dedicata (es. per un'app mobile o integrazioni esterne) o un controllo più fine sull'interfaccia, FastAPI (per la parte API) o Dash (per dashboard più strutturate) sarebbero le alternative più diffuse da considerare.
