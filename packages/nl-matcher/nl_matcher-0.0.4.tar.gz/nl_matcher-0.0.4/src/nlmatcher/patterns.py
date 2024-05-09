patterns = [
    [
        {"TEXT": "oversteekplaats"},
        {"TEXT": "tussen"},
        {"TEXT": "de"},
        {"ENT_TYPE": {"IN": ["GPE", "FAC", "LOC", "ORG"]}, "OP": "+"},
        {
            "POS": {"IN": ["ADP", "DET", "NOUN", "CCONJ"]},
            "TEXT": {"NOT_IN": ["naar"]},
            "OP": "+"
        },
        {"ENT_TYPE": {"IN": ["GPE", "FAC", "LOC"]}}
    ],

    # ---

    [
        {"TEXT": "in"},
        {"TEXT": "de"},
        {"ENT_TYPE": {"IN": ["GPE", "FAC", "LOC", "ORG"]}, "OP": "+"},
    ],

    # --

    # Example: 'Barn in de Meadow' in Benschop
    [
        {"IS_PUNCT": True},
        {
            "POS": {"IN": ["PROPN", "ADP", "DET"]},
            "OP": "+"
        },
        {"IS_PUNCT": True},
        {
            "POS": {"IN": ["ADP", "DET", "NOUN"]},
            "TEXT": {"NOT_IN": ["naar"]},
            "OP": "+"
        },
        {"ENT_TYPE": {"IN": ["GPE", "FAC", "LOC"]}}
    ],


    # Examples: 'Fluitekamp in Hoogland', 'Maarssense wijk Zwanenkamp'
    [
        {
            "ENT_TYPE": {"IN": ["GPE", "FAC", "LOC", "ORG"]},
            "OP": "+"
        },
        {
            "POS": {"IN": ["ADP", "DET", "NOUN"]},
            "TEXT": {"NOT_IN": ["naar"]},
            "OP": "+"
        },
        {"ENT_TYPE": {"IN": ["GPE", "FAC", "LOC"]}}
    ],

    # ---

    # Pattern that starts with person names and ends with a location.
    # Example: 'Marco Pololaan in de Utrechtse wijk Kanaleneiland'
    [
        {"ENT_TYPE": "PERSON", "OP": "+"},
        {"POS": {"IN": ['ADP', "DET"]},  "OP": "+"},
        {"ENT_TYPE": "NORP"},
        {"POS": "NOUN"},
        {"POS": "PROPN"},
    ],

    # ---

    # At last catch simple locations.
    [{
        "ENT_TYPE": {"IN": ["LOC", "GPE"]},
        "LOWER": {"NOT_IN": ["zondagavond"]},
        "OP": "+"
    }],
]
