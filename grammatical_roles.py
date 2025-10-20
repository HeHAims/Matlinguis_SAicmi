# cmis/data/grammatical_roles.py

GRAMMATICAL_ROLES = {
    "y": {"category": "pronoun", "symbol": "p"},
    "x": {"category": ["noun", "variable"], "symbol": "x"},
    "m": {"category": ["noun", "verb"], "symbol": ["m", "v"]},
    "b": {"category": ["adverb", "article"], "symbol": ["b", "r"]},
    "+": {"category": "conjunction", "symbol": "+"},
    "=": {"category": "verb", "symbol": "="},
    "∫": {"category": "verb", "symbol": "∫"},
    "∂": {"category": "verb", "symbol": "∂"},
    "Σ": {"category": "noun", "symbol": "Σ"}
}
