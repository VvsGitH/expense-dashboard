from rapidfuzz import fuzz

EXP_CATEGORIES = {
    "salute": [
        "farmacia", "dottore", "dott.", "chirurgo", "psicologo", "psicoterapeuta",
        "psicologica", "ospedale", "clinica", "dentista", "dental top",
    ],
    "casa": [
        "affitto", "utenze", "bolletta", "gas", "elettricità", "acqua", "fastweb",
        "iliad", "condominio", "domiciliazione", "pec postel",
    ],
    "spesa": [
        "supermercato", "coop", "conad", "famila", "rossotono", "despar", "dok",
        "carrefour", "eurospin", "frutta", "verdura", "alimentari", "carne", "pesce",
        "panificio",
    ],
    "shopping": [
        "abbigliamento", "zalando", "amazon", "amzn mktp", "elettronica",
        "mediaworld", "eprice", "ebay", "unieuro", "regalo", "ikea", "leroy merlin",
        "brico", "scarpe",
    ],
    "hobby": [
        "libri", "cinema", "teatro", "musica", "steam", "*gog", "gog sp", "nintendo",
        "games", "feltrinelli", "kobo", "udemy",
    ],
    "viaggi": [
        "hotel", "albergo", "ostello", "booking", "airbnb", "oasi", "turismo",
        "campeggio", "camping", "treno", "volo", "fiumicino", "malpensa", "wojtyla",
        "autostrada", "autogrill",
    ],
    "fitness": [
        "gym", "fitness", "workout", "mcfit", "metalabs", "wellness", "palestra",
        "rsg group", "yoga", "pilates", "calistenics", "decathlon",
    ],
    "auto": [
        "benzina", "carburante", "gpl", "dills", "dill s", "iperstaroil", "Q8",
        "assicurazione", "prima", "meccanico", "riparazione", "tagliando",
        "autolavaggio", "revisione", "gomme", "carrozziere",
    ],
    "tasse": ["tassa", "irpef", "imposta", "canone", "imposta di bollo", "pagopa"],
    "contanti": ["prelievo", "atm"],
}

DEFAULT_THRESHOLD = 80


def categorize_description(
    description: str, categories=EXP_CATEGORIES, threshold: int = DEFAULT_THRESHOLD
) -> str:
    to_match = description.lower()

    best_score = threshold
    best_category = "other"

    for category, keywords in categories.items():
        category_score = 0
        for keyword in keywords:
            score = fuzz.partial_ratio(to_match, keyword)
            if score == 100:
                category_score += 1.5 * score
            elif score >= threshold:
                category_score += score
        if category_score > best_score:
            best_score = category_score
            best_category = category

    return best_category
