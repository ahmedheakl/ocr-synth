from pylatex import Document, NoEscape, Package
from synthetic_data_generation.templates.template import Template
import random

class PackageExtender:

    def add_base_packages(self, doc: Document):
        layout_setting = Template().get_layout_settings()
        language = layout_setting.get_language()

        if language == "arabic":
            font_name = layout_setting.get_font_style().get_name()
            supported_fonts = {
                "amiri": "Amiri",
                "scheherazade": "Scheherazade New",
                "lateef": "Lateef",
                "noto naskh arabic": "Noto Naskh Arabic",
                "noto nastaliq arabic": "Noto Nastaliq Urdu",
                "noto sans arabic": "Noto Sans Arabic",
                "reem kufi": "Reem Kufi",
                "cairo": "Cairo",
                "harmattan": "Harmattan",
                "ibm plex sans arabic": "IBM Plex Sans Arabic"
            }
            if font_name == "random":
                font_name = random.choice(list(supported_fonts.keys()))
            self.set_font_name = supported_fonts.get(font_name, "Amiri")

        elif language == "chinese":
            font_name = layout_setting.get_font_style().get_name()
            supported_fonts = {
                "noto serif sc": "Noto Serif SC",
                "source han sans": "Source Han Sans SC",
                "source han serif": "Source Han Serif SC",
                "ukai": "AR PL UKai CN",
                "uming": "AR PL UMing CN",
                "wenquanyi zen hei": "WenQuanYi Zen Hei"
            }
            if font_name == "random":
                font_name = random.choice(list(supported_fonts.keys()))
            self.set_font_name = supported_fonts.get(font_name, "Noto Serif SC")

        elif language == "hebrew":
            font_name = layout_setting.get_font_style().get_name()
            supported_fonts = {
                "david clm": "David CLM",
                "frank ruehl clm": "Frank Ruehl CLM", 
                "noto serif hebrew": "Noto Serif Hebrew",
                "noto sans hebrew": "Noto Sans Hebrew",
                "ezra sil": "Ezra SIL",
                "taamey david clm": "Taamey David CLM",
                "hadasim clm": "Hadasim CLM",
                "miriam clm": "Miriam CLM",
                "nachlieli clm": "Nachlieli CLM",
                "shofar": "Shofar"
            }
            if font_name == "random":
                font_name = random.choice(list(supported_fonts.keys()))
            self.set_font_name = supported_fonts.get(font_name, "David CLM")

        elif language == "urdu":
            font_name = layout_setting.get_font_style().get_name()
            supported_fonts = {
                "noto nastaliq urdu": "Noto Nastaliq Urdu",
                "jameel noori nastaleeq": "Jameel Noori Nastaleeq",
                "alvi nastaleeq": "Alvi Nastaleeq",
                "pak nastaleeq": "Pak Nastaleeq",
                "faiz lahori nastaleeq": "Faiz Lahori Nastaleeq",
                "noto sans arabic": "Noto Sans Arabic",
                "lateef": "Lateef",
                "scheherazade new": "Scheherazade New",
                "amiri": "Amiri",
                "reem kufi": "Reem Kufi"
            }
            if font_name == "random":
                font_name = random.choice(list(supported_fonts.keys()))
            self.set_font_name = supported_fonts.get(font_name, "Noto Nastaliq Urdu")

        packages_list = layout_setting.get_packages()
        self.packages = set()
        self.add_color_package(doc)
        self.add_xurl_package(doc)
        self.add_landscape_package(doc)
        self.add_varwidth_package(doc)
        self.add_position_log_packages(doc)

        if language == "arabic":
            self.add_arabic_support_packages(doc)
        elif language == "chinese":
            self.add_chinese_support_packages(doc)
        elif language == "hebrew":
            self.add_hebrew_support_packages(doc)
        elif language == "urdu":
            self.add_urdu_support_packages(doc)

        for package in packages_list:
            if package not in self.packages:
                doc.packages.append(Package(NoEscape(package)))

    def add_arabic_support_packages(self, doc: Document):
        doc.packages.append(Package("fontspec"))
        doc.packages.append(Package("multirow"))
        doc.packages.append(Package("polyglossia"))
        doc.packages.append(Package("ragged2e"))

        doc.preamble.append(NoEscape(r"\renewcommand{\arraystretch}{1.3}"))
        doc.preamble.append(NoEscape(r"\setmainlanguage{arabic}"))
        doc.preamble.append(NoEscape(r"\setotherlanguage{english}"))
        doc.preamble.append(NoEscape(
            fr"\newfontfamily\arabicfont[Script=Arabic, FallbackFonts={{Amiri, Times New Roman, Noto Color Emoji, Symbola}}]{{{self.set_font_name}}}"
        ))

        self.packages.update({"fontspec", "polyglossia", "ragged2e"})

    def add_chinese_support_packages(self, doc: Document):
        doc.packages.append(Package("fontspec"))
        doc.packages.append(Package("multirow"))
        doc.packages.append(Package("polyglossia"))
        doc.packages.append(Package("ragged2e"))

        doc.preamble.append(NoEscape(r"\renewcommand{\arraystretch}{1.3}"))
        doc.preamble.append(NoEscape(r"\setmainlanguage{chinese}"))
        doc.preamble.append(NoEscape(r"\setotherlanguage{english}"))
        doc.preamble.append(NoEscape(
            fr"\newfontfamily\chinesefont[Script=CJK, FallbackFonts={{AR PL UKai CN, Source Han Serif SC, Noto Color Emoji, Symbola}}]{{{self.set_font_name}}}"
        ))
        doc.preamble.append(NoEscape(r"\newfontfamily\cjkfonttt{Noto Sans Mono CJK SC}"))
        doc.preamble.append(NoEscape(r"\renewcommand{\ttfamily}{\cjkfonttt}"))
        doc.append(NoEscape(r"\chinesefont"))

        self.packages.update({"fontspec", "polyglossia", "ragged2e"})

    def add_hebrew_support_packages(self, doc: Document):
        """Add Hebrew language support packages for LuaTeX"""
        doc.packages.append(Package("fontspec"))
        doc.packages.append(Package("multirow"))
        doc.packages.append(Package("polyglossia"))
        doc.packages.append(Package("ragged2e"))
        # Note: Do NOT add bidi package - it's XeTeX only!

        doc.preamble.append(NoEscape(r"\renewcommand{\arraystretch}{1.3}"))
        doc.preamble.append(NoEscape(r"\setmainlanguage{hebrew}"))
        doc.preamble.append(NoEscape(r"\setotherlanguage{english}"))
        
        # Set up Hebrew font with proper fallbacks
        doc.preamble.append(NoEscape(
            fr"\newfontfamily\hebrewfont[Script=Hebrew, Direction=RTL, FallbackFonts={{David CLM, Frank Ruehl CLM, Noto Color Emoji, Symbola}}]{{{self.set_font_name}}}"
        ))
        
        # LuaTeX native RTL support - no bidi package needed
        doc.preamble.append(NoEscape(r"\def\setRTL{\pardir TRT \textdir TRT}"))
        doc.preamble.append(NoEscape(r"\def\setLTR{\pardir TLT \textdir TLT}"))
        
        # Set Hebrew as default direction
        doc.preamble.append(NoEscape(r"\setRTL"))
        doc.preamble.append(NoEscape(r"\hebrewfont"))

        # Use Hebrew-aware line breaking
        doc.preamble.append(NoEscape(r"\tolerance=1000"))
        doc.preamble.append(NoEscape(r"\emergencystretch=3em"))

        self.packages.update({"fontspec", "polyglossia", "ragged2e"})

    def add_urdu_support_packages(self, doc: Document):
        """Add Urdu language support packages"""
        doc.packages.append(Package("fontspec"))
        doc.packages.append(Package("multirow"))
        doc.packages.append(Package("polyglossia"))
        doc.packages.append(Package("ragged2e"))

        doc.preamble.append(NoEscape(r"\renewcommand{\arraystretch}{1.3}"))
        doc.preamble.append(NoEscape(r"\setmainlanguage{urdu}"))
        doc.preamble.append(NoEscape(r"\setotherlanguage{english}"))
        
        # Set up Urdu font with proper Arabic script support
        doc.preamble.append(NoEscape(
            fr"\newfontfamily\urdufont[Script=Arabic, Language=Urdu, Direction=RTL, FallbackFonts={{Noto Nastaliq Urdu, Jameel Noori Nastaleeq, Amiri, Noto Color Emoji, Symbola}}]{{{self.set_font_name}}}"
        ))
        
        # LuaTeX native RTL support for Urdu
        doc.preamble.append(NoEscape(r"\def\setRTL{\pardir TRT \textdir TRT}"))
        doc.preamble.append(NoEscape(r"\def\setLTR{\pardir TLT \textdir TLT}"))
        
        # Set Urdu-specific typography settings
        doc.preamble.append(NoEscape(r"\setRTL"))
        doc.preamble.append(NoEscape(r"\urdufont"))
        
        # Urdu-specific line breaking and spacing
        doc.preamble.append(NoEscape(r"\tolerance=2000"))  # Higher tolerance for Urdu
        doc.preamble.append(NoEscape(r"\emergencystretch=4em"))
        doc.preamble.append(NoEscape(r"\hyphenpenalty=10000"))  # Avoid hyphenation in Urdu
        
        # Urdu punctuation and number handling
        doc.preamble.append(NoEscape(r"\def\urdunumbers#1{\bgroup\urdufont\textdir TRT #1\egroup}"))

        self.packages.update({"fontspec", "polyglossia", "ragged2e"})

    def add_color_package(self, doc: Document):
        doc.packages.append(Package("background"))
        doc.packages.append(Package("minted"))
        doc.packages.append(Package("listings"))
        doc.packages.append(Package("xcolor"))
        doc.packages.append(Package("booktabs"))
        doc.packages.append(Package("colortbl"))

        self.packages.update({"background", "minted", "listings", "xcolor", "colortbl", "booktabs"})

        doc.preamble.append(NoEscape(r"\usepackage[most]{tcolorbox}"))  # avoid clash
        doc.preamble.append(NoEscape(r"\tcbuselibrary{listings, minted}"))
        doc.preamble.append(NoEscape(r"\newfontfamily\myotherfont{Times New Roman}"))

        doc.preamble.append(NoEscape(r"""
            \newtcblisting{dynamiccodeboxminted}[4][]{%
            listing engine=minted,
            colback=#2, colframe=#3,
            #1,
            minted language=#4,
            minted options={fontsize=\small, linenos},
            listing only,
            left=5pt, right=5pt, top=5pt, bottom=5pt,
            boxrule=0.5pt,
            }
        """))

        doc.preamble.append(NoEscape(r"""
            \newtcblisting{dynamiccodeboxlisting}[4][]{%
            listing engine=listings,
            colback=#2, colframe=#3,
            #1,
            language=#4,
            basicstyle=\small\ttfamily,
            numbers=left,
            listing only,
            left=5pt, right=5pt, top=5pt, bottom=5pt,
            boxrule=0.5pt,
            }
        """))

        doc.preamble.append(NoEscape(r"""
        \newtcblisting{verbatimcodebox}[3][]{%
        listing engine=minted,
        minted language=javascript,  % Or typescript
        minted options={fontsize=\small, breaklines, linenos},
        colback=#1, colframe=#2,
        #3,
        listing only,
        left=5pt, right=5pt, top=5pt, bottom=5pt,
        boxrule=0.5pt,
        }
        """))
        # Use \providecommand to avoid redefinition errors
        eng_macro = r"\providecommand{\eng}[1]{{\myotherfont\textdir TLT #1}}"
        # eng_macro2 = r"\providecommand{\eng2}[1]{\LR{\myotherfont #1}}"
        doc.preamble.append(NoEscape(eng_macro))
        # doc.preamble.append(NoEscape(eng_macro2))

    def add_line_nums_package(self, doc: Document):
        doc.packages.append(Package("lineno"))

    def add_xurl_package(self, doc: Document):
        doc.packages.append(Package("xurl"))
        self.packages.add("xurl")

    def add_landscape_package(self, doc: Document):
        doc.packages.append(Package("lscape"))
        self.packages.add("lscape")

    def add_varwidth_package(self, doc: Document):
        doc.packages.append(Package("varwidth"))
        self.packages.add("varwidth")

    def add_position_log_packages(self, doc: Document):
        doc.packages.append(Package("geometry"))
        doc.packages.append(Package("refcount"))
        doc.packages.append(Package(NoEscape("zref-user")))
        doc.packages.append(Package(NoEscape("zref-savepos")))
        doc.packages.append(Package("multirow"))
        doc.packages.append(Package("tabularx"))
        doc.packages.append(Package("array"))
        doc.packages.append(Package("caption"))
        doc.packages.append(Package("amsmath"))
        doc.packages.append(Package("amssymb"))
        doc.preamble.append(NoEscape(r"\newenvironment{nullenv}{}{}"))
        self.packages.update([
            "geometry", "refcount", "zref-user", "zref-savepos",
            "array", "caption", "amsmath", "amssymb", "tabularx", "multirow"
        ])