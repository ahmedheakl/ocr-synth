# from random import randint

# from synthetic_data_generation.templates.util.font_style import FontStyle
# from synthetic_data_generation.templates.util.template_values import TemplateValues

# class AvailableFontStyles:

#     _pkg_key = "p"
#     _code_key = "c"
#     _default_font_style = "amiri"
    
#     _language_font_map = {
#         "arabic": [
#             "amiri",
#             "scheherazade",
#             "lateef",
#             "noto naskh arabic",
#             "noto nastaliq arabic",
#             "noto sans arabic",
#             "reem kufi",
#             "cairo",
#             "harmattan",
#             "ibm plex sans arabic"
#         ],
#         "english": [
#             "tex-gyre-termes",
#             "times",
#             "utopia",
#             "palatino",
#             "charter",
#             "helvetica",
#             "tex-gyre pagella",
#             "tex-gyre-bonum",
#             "tex-gyre-schola",
#             "times",
#             "bookman",
#             "computer-modern-roman",
#             "computer-modern-sans-serif",
#             "tex-gyre-adventor",
#             "tex-gyre-heros",
#             "computer-modern-typewriter",
#             "tex-gyre-cursor"
#         ],
#         "chinese": [
#             "noto sans sc",
#             "noto serif sc",
#             "noto sans tc",
#             "noto serif tc",
#             "ibm plex sans jp",
#             "wdxllubrifontsc",
#             "wdxllubrifontjpn",
#             "lxgw marker gothic",
#             "chiron hei hk",
#             "chiron sung hk",
#             "huninn",
#             "uoqmunthenkhung"
#         ],
#         "hebrew": [
#             "david clm",           # Traditional Hebrew font
#             "frank ruehl clm",     # Classic Hebrew serif font
#             "noto serif hebrew",   # Google's Noto Hebrew serif
#             "noto sans hebrew",    # Google's Noto Hebrew sans-serif
#             "ezra sil",           # SIL's Hebrew font
#             "taamey david clm",   # Hebrew font with cantillation marks
#             "hadasim clm",        # Modern Hebrew sans-serif
#             "miriam clm",         # Hebrew monospace font
#             "nachlieli clm",      # Decorative Hebrew font
#             "shofar",             # Traditional Hebrew display font
#         ],
#         "urdu": [
#             "noto nastaliq urdu",     # Google's Noto Urdu font (best for Urdu)
#             "jameel noori nastaleeq", # Popular Urdu font
#             "alvi nastaleeq",        # Traditional Urdu font
#             "pak nastaleeq",         # Pakistani Urdu font
#             "faiz lahori nastaleeq", # Beautiful Urdu calligraphy font
#             "noto sans arabic",      # Fallback Arabic font for Urdu
#             "lateef",               # SIL font with good Urdu support
#             "scheherazade new",     # SIL font for Arabic/Urdu
#             "amiri",                # Arabic font with Urdu support
#             "reem kufi",            # Modern Arabic/Urdu font
#         ]
#     }


#     _table = {
#         "computer-modern-roman": {
#             _pkg_key: "",
#             _code_key: "cmr"
#         },
#         "tex-gyre-termes": {
#             _pkg_key: "tgtermes",
#             _code_key: "qtm"
#         },
#         "tex-gyre pagella": {
#             _pkg_key: "tgpagella",
#             _code_key: "qpl"
#         },
#         "tex-gyre-bonum": {
#             _pkg_key: "tgbonum",
#             _code_key: "qbk"
#         },
#         "tex-gyre-schola": {
#             _pkg_key: "tgschola",
#             _code_key: "qcs"
#         },
#         "times": {
#             _pkg_key: "mathptmx",
#             _code_key: "ptm"
#         },
#         "utopia": {
#             _pkg_key: "utopia",
#             _code_key: "put"
#         },
#         "palatino": {
#             _pkg_key: "palatino",
#             _code_key: "ppl"
#         },
#         "bookman": {
#             _pkg_key: "bookman",
#             _code_key: "pbk"
#         },
#         "charter": {
#             _pkg_key: "charter",
#             _code_key: "bch"
#         },
#         "computer-modern-sans-serif": {
#             _pkg_key: "",
#             _code_key: "cmss"
#         },
#         "tex-gyre-adventor": {
#             _pkg_key: "tgadventor",
#             _code_key: "qag"
#         },
#         "tex-gyre-heros": {
#             _pkg_key: "tgheros",
#             _code_key: "qhv"
#         },
#         "helvetica": {
#             _pkg_key: "helvet",
#             _code_key: "phv"
#         },
#         "computer-modern-typewriter": {
#             _pkg_key: "",
#             _code_key: "cmtt"
#         },
#         "tex-gyre-cursor": {
#             _pkg_key: "tgcursor",
#             _code_key: "qcr"
#         },

#         # Arabic fonts (for XeLaTeX via fontspec)
#         "amiri": {
#             _pkg_key: "",
#             _code_key: "amiri"
#         },
#         "scheherazade": {
#             _pkg_key: "",
#             _code_key: "scheherazade"
#         },
#         "lateef": {
#             _pkg_key: "",
#             _code_key: "lateef"
#         },
#         "noto naskh arabic": {
#             _pkg_key: "",
#             _code_key: "noto naskh arabic"
#         },
#         "noto nastaliq arabic": {
#             _pkg_key: "",
#             _code_key: "noto nastaliq arabic"
#         },
#         "noto sans arabic": {
#             _pkg_key: "",
#             _code_key: "noto sans arabic"
#         },
#         "reem kufi": {
#             _pkg_key: "",
#             _code_key: "reem kufi"
#         },
#         "cairo": {
#             _pkg_key: "",
#             _code_key: "cairo"
#         },
#         "harmattan": {
#             _pkg_key: "",
#             _code_key: "harmattan"
#         },
#         "ibm plex sans arabic": {
#             _pkg_key: "",
#             _code_key: "ibm plex sans arabic"
#         },

#         # Chinese fonts (for XeLaTeX via fontspec)
#         "noto sans sc": {
#             _pkg_key: "",
#             _code_key: "noto sans sc"
#         },
#         "noto serif sc": {
#             _pkg_key: "",
#             _code_key: "noto serif sc"
#         },
#         "noto sans tc": {
#             _pkg_key: "",
#             _code_key: "noto sans tc"
#         },
#         "noto serif tc": {
#             _pkg_key: "",
#             _code_key: "noto serif tc"
#         },
#         "ibm plex sans jp": {
#             _pkg_key: "",
#             _code_key: "ibm plex sans jp"
#         },
#         "wdxllubrifontsc": {
#             _pkg_key: "",
#             _code_key: "wdxllubrifontsc"
#         },
#         "wdxllubrifontjpn": {
#             _pkg_key: "",
#             _code_key: "wdxllubrifontjpn"
#         },
#         "lxgw marker gothic": {
#             _pkg_key: "",
#             _code_key: "lxgw marker gothic"
#         },
#         "chiron hei hk": {
#             _pkg_key: "",
#             _code_key: "chiron hei hk"
#         },
#         "chiron sung hk": {
#             _pkg_key: "",
#             _code_key: "chiron sung hk"
#         },
#         "huninn": {
#             _pkg_key: "",
#             _code_key: "huninn"
#         },
#         "uoqmunthenkhung": {
#             _pkg_key: "",
#             _code_key: "uoqmunthenkhung"
#         },
#         "david clm": {
#             _pkg_key: "",
#             _code_key: "david clm"
#         },
#         "frank ruehl clm": {
#             _pkg_key: "",
#             _code_key: "frank ruehl clm"
#         },
#         "noto serif hebrew": {
#             _pkg_key: "",
#             _code_key: "noto serif hebrew"
#         },
#         "noto sans hebrew": {
#             _pkg_key: "",
#             _code_key: "noto sans hebrew"
#         },
#         "ezra sil": {
#             _pkg_key: "",
#             _code_key: "ezra sil"
#         },
#         "taamey david clm": {
#             _pkg_key: "",
#             _code_key: "taamey david clm"
#         },
#         "hadasim clm": {
#             _pkg_key: "",
#             _code_key: "hadasim clm"
#         },
#         "miriam clm": {
#             _pkg_key: "",
#             _code_key: "miriam clm"
#         },
#         "nachlieli clm": {
#             _pkg_key: "",
#             _code_key: "nachlieli clm"
#         },
#         "shofar": {
#             _pkg_key: "",
#             _code_key: "shofar"
#         },
#         "noto nastaliq urdu": {
#             _pkg_key: "",
#             _code_key: "noto nastaliq urdu"
#         },
#         "jameel noori nastaleeq": {
#             _pkg_key: "",
#             _code_key: "jameel noori nastaleeq"
#         },
#         "alvi nastaleeq": {
#             _pkg_key: "",
#             _code_key: "alvi nastaleeq"
#         },
#         "pak nastaleeq": {
#             _pkg_key: "",
#             _code_key: "pak nastaleeq"
#         },
#         "faiz lahori nastaleeq": {
#             _pkg_key: "",
#             _code_key: "faiz lahori nastaleeq"
#         },
#         "scheherazade new": {
#             _pkg_key: "",
#             _code_key: "scheherazade new"
#         }
#     }

#     def font_style_to_instance(style: str) -> FontStyle:
#         style = AvailableFontStyles.get_this_or_default_font_style(style)
#         return FontStyle(
#             style,
#             AvailableFontStyles._table[style][AvailableFontStyles._code_key],
#             AvailableFontStyles._table[style][AvailableFontStyles._pkg_key]
#         )

#     def get_this_or_default_font_style(style: str) -> str:
#         if (TemplateValues.is_random_identifier_str(style)):
#             return AvailableFontStyles.get_random_font_style()
#         if (style in AvailableFontStyles._table):
#             return style
#         return AvailableFontStyles.get_default_font_style()

#     def get_default_font_style() -> str:
#         return AvailableFontStyles._default_font_style

#     def get_random_font_style() -> str:
#         random_index = randint(0, len(AvailableFontStyles._table)-1)
#         return list(AvailableFontStyles._table)[random_index]

#     @staticmethod
#     def get_fonts_for_language(language: str) -> list:
#         lang = language.lower()
#         return AvailableFontStyles._language_font_map.get(lang, [])

#     @staticmethod
#     def get_default_font_for_language(language: str) -> str:
#         fonts = AvailableFontStyles.get_fonts_for_language(language)
#         if fonts:
#             return fonts[0]
#         return AvailableFontStyles.get_default_font_style()

#     @staticmethod
#     def get_random_font_for_language(language: str) -> str:
#         fonts = AvailableFontStyles.get_fonts_for_language(language)
#         if fonts:
#             return fonts[randint(0, len(fonts)-1)]
#         return AvailableFontStyles.get_random_font_style()

from random import randint

from synthetic_data_generation.templates.util.font_style import FontStyle
from synthetic_data_generation.templates.util.template_values import TemplateValues

class AvailableFontStyles:

    _pkg_key = "p"
    _code_key = "c"
    _default_font_style = "amiri"
    
    _language_font_map = {
        "arabic": [
            "amiri",
            "scheherazade",
            "lateef",
            "noto naskh arabic",
            "noto nastaliq arabic",
            "noto sans arabic",
            "reem kufi",
            "cairo",
            "harmattan",
            "ibm plex sans arabic"
        ],
        "english": [
            "tex-gyre-termes",
            "times",
            "utopia",
            "palatino",
            "charter",
            "helvetica",
            "tex-gyre pagella",
            "tex-gyre-bonum",
            "tex-gyre-schola",
            "times",
            "bookman",
            "computer-modern-roman",
            "computer-modern-sans-serif",
            "tex-gyre-adventor",
            "tex-gyre-heros",
            "computer-modern-typewriter",
            "tex-gyre-cursor"
        ],
        "chinese": [
            "noto sans sc",
            "noto serif sc",
            "noto sans tc",
            "noto serif tc",
            "ibm plex sans jp",
            "wdxllubrifontsc",
            "wdxllubrifontjpn",
            "lxgw marker gothic",
            "chiron hei hk",
            "chiron sung hk",
            "huninn",
            "uoqmunthenkhung"
        ],
        "hebrew": [
            "david clm",           # Traditional Hebrew font
            "frank ruehl clm",     # Classic Hebrew serif font
            "noto serif hebrew",   # Google's Noto Hebrew serif
            "noto sans hebrew",    # Google's Noto Hebrew sans-serif
            "ezra sil",           # SIL's Hebrew font
            "taamey david clm",   # Hebrew font with cantillation marks
            "hadasim clm",        # Modern Hebrew sans-serif
            "miriam clm",         # Hebrew monospace font
            "nachlieli clm",      # Decorative Hebrew font
            "shofar",             # Traditional Hebrew display font
        ],
        "urdu": [
            "noto nastaliq urdu",     # Google's Noto Urdu font (best for Urdu)
            "jameel noori nastaleeq", # Popular Urdu font
            "alvi nastaleeq",        # Traditional Urdu font
            "pak nastaleeq",         # Pakistani Urdu font
            "faiz lahori nastaleeq", # Beautiful Urdu calligraphy font
            "noto sans arabic",      # Fallback Arabic font for Urdu
            "lateef",               # SIL font with good Urdu support
            "scheherazade new",     # SIL font for Arabic/Urdu
            "amiri",                # Arabic font with Urdu support
            "reem kufi",            # Modern Arabic/Urdu font
        ],
        "persian": [
            "vazir",                 # Modern Persian sans-serif font
            "sahel",                 # Persian sans-serif font
            "samim",                 # Persian serif font
            "tanha",                 # Elegant Persian font
            "iranian sans",          # Clean Persian sans-serif
            "noto sans arabic",      # Google Noto with Persian support
            "noto naskh arabic",     # Traditional Arabic/Persian font
            "b nazanin",            # Classic Persian font
            "iran nastaliq",        # Persian Nastaliq script
            "lateef",               # SIL font with Persian support
            "scheherazade new",     # SIL font for Arabic/Persian
            "amiri",                # Arabic font with Persian support
            "harmattan",            # West African Arabic font (works for Persian)
            "reem kufi",            # Modern Arabic/Persian font
        ]
    }

    _table = {
        "computer-modern-roman": {
            _pkg_key: "",
            _code_key: "cmr"
        },
        "tex-gyre-termes": {
            _pkg_key: "tgtermes",
            _code_key: "qtm"
        },
        "tex-gyre pagella": {
            _pkg_key: "tgpagella",
            _code_key: "qpl"
        },
        "tex-gyre-bonum": {
            _pkg_key: "tgbonum",
            _code_key: "qbk"
        },
        "tex-gyre-schola": {
            _pkg_key: "tgschola",
            _code_key: "qcs"
        },
        "times": {
            _pkg_key: "mathptmx",
            _code_key: "ptm"
        },
        "utopia": {
            _pkg_key: "utopia",
            _code_key: "put"
        },
        "palatino": {
            _pkg_key: "palatino",
            _code_key: "ppl"
        },
        "bookman": {
            _pkg_key: "bookman",
            _code_key: "pbk"
        },
        "charter": {
            _pkg_key: "charter",
            _code_key: "bch"
        },
        "computer-modern-sans-serif": {
            _pkg_key: "",
            _code_key: "cmss"
        },
        "tex-gyre-adventor": {
            _pkg_key: "tgadventor",
            _code_key: "qag"
        },
        "tex-gyre-heros": {
            _pkg_key: "tgheros",
            _code_key: "qhv"
        },
        "helvetica": {
            _pkg_key: "helvet",
            _code_key: "phv"
        },
        "computer-modern-typewriter": {
            _pkg_key: "",
            _code_key: "cmtt"
        },
        "tex-gyre-cursor": {
            _pkg_key: "tgcursor",
            _code_key: "qcr"
        },

        # Arabic fonts (for XeLaTeX via fontspec)
        "amiri": {
            _pkg_key: "",
            _code_key: "amiri"
        },
        "scheherazade": {
            _pkg_key: "",
            _code_key: "scheherazade"
        },
        "lateef": {
            _pkg_key: "",
            _code_key: "lateef"
        },
        "noto naskh arabic": {
            _pkg_key: "",
            _code_key: "noto naskh arabic"
        },
        "noto nastaliq arabic": {
            _pkg_key: "",
            _code_key: "noto nastaliq arabic"
        },
        "noto sans arabic": {
            _pkg_key: "",
            _code_key: "noto sans arabic"
        },
        "reem kufi": {
            _pkg_key: "",
            _code_key: "reem kufi"
        },
        "cairo": {
            _pkg_key: "",
            _code_key: "cairo"
        },
        "harmattan": {
            _pkg_key: "",
            _code_key: "harmattan"
        },
        "ibm plex sans arabic": {
            _pkg_key: "",
            _code_key: "ibm plex sans arabic"
        },

        # Chinese fonts (for XeLaTeX via fontspec)
        "noto sans sc": {
            _pkg_key: "",
            _code_key: "noto sans sc"
        },
        "noto serif sc": {
            _pkg_key: "",
            _code_key: "noto serif sc"
        },
        "noto sans tc": {
            _pkg_key: "",
            _code_key: "noto sans tc"
        },
        "noto serif tc": {
            _pkg_key: "",
            _code_key: "noto serif tc"
        },
        "ibm plex sans jp": {
            _pkg_key: "",
            _code_key: "ibm plex sans jp"
        },
        "wdxllubrifontsc": {
            _pkg_key: "",
            _code_key: "wdxllubrifontsc"
        },
        "wdxllubrifontjpn": {
            _pkg_key: "",
            _code_key: "wdxllubrifontjpn"
        },
        "lxgw marker gothic": {
            _pkg_key: "",
            _code_key: "lxgw marker gothic"
        },
        "chiron hei hk": {
            _pkg_key: "",
            _code_key: "chiron hei hk"
        },
        "chiron sung hk": {
            _pkg_key: "",
            _code_key: "chiron sung hk"
        },
        "huninn": {
            _pkg_key: "",
            _code_key: "huninn"
        },
        "uoqmunthenkhung": {
            _pkg_key: "",
            _code_key: "uoqmunthenkhung"
        },

        # Hebrew fonts
        "david clm": {
            _pkg_key: "",
            _code_key: "david clm"
        },
        "frank ruehl clm": {
            _pkg_key: "",
            _code_key: "frank ruehl clm"
        },
        "noto serif hebrew": {
            _pkg_key: "",
            _code_key: "noto serif hebrew"
        },
        "noto sans hebrew": {
            _pkg_key: "",
            _code_key: "noto sans hebrew"
        },
        "ezra sil": {
            _pkg_key: "",
            _code_key: "ezra sil"
        },
        "taamey david clm": {
            _pkg_key: "",
            _code_key: "taamey david clm"
        },
        "hadasim clm": {
            _pkg_key: "",
            _code_key: "hadasim clm"
        },
        "miriam clm": {
            _pkg_key: "",
            _code_key: "miriam clm"
        },
        "nachlieli clm": {
            _pkg_key: "",
            _code_key: "nachlieli clm"
        },
        "shofar": {
            _pkg_key: "",
            _code_key: "shofar"
        },

        # Urdu fonts
        "noto nastaliq urdu": {
            _pkg_key: "",
            _code_key: "noto nastaliq urdu"
        },
        "jameel noori nastaleeq": {
            _pkg_key: "",
            _code_key: "jameel noori nastaleeq"
        },
        "alvi nastaleeq": {
            _pkg_key: "",
            _code_key: "alvi nastaleeq"
        },
        "pak nastaleeq": {
            _pkg_key: "",
            _code_key: "pak nastaleeq"
        },
        "faiz lahori nastaleeq": {
            _pkg_key: "",
            _code_key: "faiz lahori nastaleeq"
        },
        "scheherazade new": {
            _pkg_key: "",
            _code_key: "scheherazade new"
        },

        # Persian fonts
        "vazir": {
            _pkg_key: "",
            _code_key: "vazir"
        },
        "sahel": {
            _pkg_key: "",
            _code_key: "sahel"
        },
        "samim": {
            _pkg_key: "",
            _code_key: "samim"
        },
        "tanha": {
            _pkg_key: "",
            _code_key: "tanha"
        },
        "iranian sans": {
            _pkg_key: "",
            _code_key: "iranian sans"
        },
        "b nazanin": {
            _pkg_key: "",
            _code_key: "b nazanin"
        },
        "iran nastaliq": {
            _pkg_key: "",
            _code_key: "iran nastaliq"
        }
    }

    def font_style_to_instance(style: str) -> FontStyle:
        style = AvailableFontStyles.get_this_or_default_font_style(style)
        return FontStyle(
            style,
            AvailableFontStyles._table[style][AvailableFontStyles._code_key],
            AvailableFontStyles._table[style][AvailableFontStyles._pkg_key]
        )

    def get_this_or_default_font_style(style: str) -> str:
        if (TemplateValues.is_random_identifier_str(style)):
            return AvailableFontStyles.get_random_font_style()
        if (style in AvailableFontStyles._table):
            return style
        return AvailableFontStyles.get_default_font_style()

    def get_default_font_style() -> str:
        return AvailableFontStyles._default_font_style

    def get_random_font_style() -> str:
        random_index = randint(0, len(AvailableFontStyles._table)-1)
        return list(AvailableFontStyles._table)[random_index]

    @staticmethod
    def get_fonts_for_language(language: str) -> list:
        lang = language.lower()
        return AvailableFontStyles._language_font_map.get(lang, [])

    @staticmethod
    def get_default_font_for_language(language: str) -> str:
        fonts = AvailableFontStyles.get_fonts_for_language(language)
        if fonts:
            return fonts[0]
        return AvailableFontStyles.get_default_font_style()

    @staticmethod
    def get_random_font_for_language(language: str) -> str:
        fonts = AvailableFontStyles.get_fonts_for_language(language)
        if fonts:
            return fonts[randint(0, len(fonts)-1)]
        return AvailableFontStyles.get_random_font_style()