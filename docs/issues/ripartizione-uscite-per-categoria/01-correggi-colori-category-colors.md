# 01 — Correggi i colori fuori standard in CATEGORY_COLORS

**What to build:** In `domain.charts.CATEGORY_COLORS`, i 3 colori che non superano la verifica di leggibilità/accessibilità colore (banda di luminosità, soglia di chroma, separazione CVD sulle coppie adiacenti — vedi `docs/issues/ripartizione-uscite-per-categoria/spec.md`) vengono sostituiti con le varianti validate. Il grafico a torta esistente (non ancora sostituito — verrà rimosso dal ticket `02`) continua a funzionare esattamente come oggi, ma con questi 3 colori aggiornati.

**Blocked by:** Nessuno — può partire subito

**Status:** done

- [x] `viaggi` passa da `#ffff33` a `#a68f00`
- [x] `tasse` passa da `#4012bd` a `#00917f`
- [x] `other` passa da `#bdbdbd` a `#c58e50`
- [x] Gli altri 8 colori (`salute`, `casa`, `spesa`, `shopping`, `hobby`, `fitness`, `auto`, `contanti`) restano invariati
- [x] L'ordine delle chiavi nel dizionario riflette l'ordine verificato: `salute, casa, spesa, shopping, hobby, fitness, auto, viaggi, tasse, contanti, other` (nessun effetto sul comportamento a runtime — il lookup resta per chiave, non per posizione — serve solo come riferimento documentato dell'ordine verificato)
- [x] I test esistenti in `tests/test_charts.py` (`test_category_colors_maps_known_categories`, `test_category_colors_falls_back_to_other_for_unknown_category`) restano verdi senza modifiche, usando i nuovi valori tramite `CATEGORY_COLORS`
- [x] Verificato in browser: la dashboard, sezione "Uscite per Categoria", mostra il grafico a torta esistente con i 3 colori aggiornati (giallo "viaggi" più scuro/saturo, "tasse" un teal al posto del viola scuro, "other" un ambra/ocra distinguibile da tutte le altre categorie incluso "fitness")

## Comments

Implementato: 3 colori sostituiti in `CATEGORY_COLORS` (`src/domain/charts.py`) con valori verificati dallo script `validate_palette.js` della skill `dataviz` (banda di luminosità, soglia di chroma, separazione CVD — tutti PASS sia sulle coppie adiacenti sia su tutte le 55 coppie possibili con `--pairs all`). L'ordine delle chiavi è stato aggiornato di conseguenza (`viaggi` spostato dopo `auto` invece che dopo `hobby`, per non restare adiacente al colore arancione — coppia con separazione CVD insufficiente sotto simulazione di daltonismo); il riordino non ha alcun effetto a runtime, serve solo a documentare l'ordine verificato.

Prima code review (a due assi, Standards e Spec) su una bozza con `other: #9c6030` (marrone-tan) non aveva sollevato nulla, perché entrambi gli assi verificano conformità a standard/spec, non leggibilità percettiva. Rileggendo il grafico in browser, l'utente ha notato che `other` e `fitness` (`#a65628`) erano praticamente lo stesso colore — confermato con lo script: ΔE 2.7 a visione normale sotto `--pairs all`, indistinguibile anche senza daltonismo. Sostituito con `#c58e50` (ambra/ocra dorato): ΔE 15.2 a visione normale contro `fitness`, nessuna nuova coppia peggiore introdotta altrove. Resta, per l'intero set di 11 colori, una collisione preesistente e fuori scope tra `contanti` e `casa`/`shopping` (colori originali, non toccati da questo ticket) — vedi spec, sezione Implementation Decisions.

Verificato di nuovo in browser (Streamlit dev server, dati reali già presenti nel DB) dopo la correzione: grafico a torta esistente in "Uscite per Categoria" mostra "other" come ambra/oro nettamente distinto dal marroncino sottile di "fitness", "viaggi" oliva scuro, "tasse" un sottile spicchio teal distinguibile dal verde e dal rosso adiacenti.

Code review a due assi: Standards e Spec entrambe pulite, nessuna violazione hard. Standards ha segnalato due judgement call minori: primitive obsession pre-esistente su `CATEGORY_COLORS` (stringhe hex invece di un tipo `Color` dedicato — non introdotta da questa modifica, da considerare se il file verrà ritoccato ancora per motivi simili) e il riordino delle chiavi come "diff noise" senza spiegazione — risolto documentando il motivo qui sopra. Nessuna delle due review ha rilevato la collisione other/fitness (fuori dal loro perimetro, non una violazione di standard o spec) — individuata dall'utente in revisione visiva.
