from domain.categorization import categorize_description


def test_categorizes_known_keyword_matches():
    assert categorize_description("Farmacia Rossi") == "salute"
    assert categorize_description("Supermercato Conad") == "spesa"
    assert categorize_description("PRELIEVO ATM Bancomat") == "contanti"


def test_falls_back_to_other_when_no_keyword_matches():
    assert categorize_description("Negozio Sconosciuto XYZ") == "other"
