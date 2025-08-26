
# import re
# from pylatex.utils import escape_latex
# from pylatex import Command
# from pylatex.utils import NoEscape

# HEBREW_PATTERN = re.compile(r'[\u0590-\u05FF\uFB1D-\uFB4F]')
# ARABIC_PATTERN = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]')
# URDU_PATTERN = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]') 
# LATIN_TOKEN_RE = re.compile(r'(?<!\\)([A-Za-z0-9][A-Za-z0-9_\-/+&%$@:.]*)')
# ENG_BLOCK_RE = re.compile(r"(\\eng2\{.*?\})", re.S)

# def wrap_latin_segments(text: str) -> str:
#     """Wrap all Latin tokens (including numbers) with \eng{...}, skipping existing ones."""
#     def repl(m):
#         return rf"\eng{{{m.group(0)}}}"
    
#     # Split on already wrapped blocks
#     parts = re.split(r'(\\eng2?\{.*?\})', text, flags=re.S)
#     for i in range(0, len(parts), 2):  # only wrap unwrapped parts
#         parts[i] = LATIN_TOKEN_RE.sub(repl, parts[i])
#     return ''.join(parts)

# def escape_everything_except_eng(text: str) -> str:
#     """Escape LaTeX except for inside \\eng{...} or \\eng2{...}."""
#     # Match both \eng{...} and \eng2{...}
#     parts = re.split(r'(\\eng2?\{.*?\})', text)
    
#     for i in range(0, len(parts), 2):  # Only escape non-\eng parts
#         parts[i] = escape_latex(parts[i])
    
#     return ''.join(parts)

# def clean_latin_in_eng_tag(text):
#     # Join split Latin words inside \eng{}
#     return re.sub(r'\\eng\{([^}]*)\\ ([^}]*)\}', lambda m: f"\\eng{{{m.group(1)}{m.group(2)}}}", text)

# def is_latin_text(text: str) -> bool:
#     # Heuristic: if >50% characters are Latin letters or numbers
#     latin_chars = re.findall(r"[A-Za-z0-9]", text)
#     return len(latin_chars) / max(len(text), 1) > 0.5


# def _wrap_latin_segments(text: str) -> str:
#     # Skip LaTeX commands (e.g., \textbf{...}, \section, etc.)
#     def latex_command_replacer(match):
#         return match.group(0)  # Don't touch commands

#     def replacer(match):
#         segment = match.group(0)
#         if re.search(r'[A-Za-z]', segment):  # Ensure real Latin content
#             return rf'\eng{{{segment.strip()}}}'
#         return segment

#     # Protect LaTeX commands first
#     protected_text = re.sub(r'\\[a-zA-Z]+\*?(?:\[[^\]]*\])?(?:\{[^}]*\})*', latex_command_replacer, text)

#     # Now wrap Latin segments, including words with punctuation or digits
#     return re.sub(r'(?<!\\)([A-Za-z0-9][A-Za-z0-9_ .,:;!?/\-\'"()&%$@]*)', replacer, protected_text)


# def is_latin_text(text: str) -> bool:
#     # Heuristic: if >50% characters are Latin letters or numbers
#     latin_chars = re.findall(r"[A-Za-z0-9]", text)
#     return len(latin_chars) / max(len(text), 1) > 0.5


# def wrap_latin_segments(txt: str) -> str:
#     """Wrap every Latin token in \eng{…}, unless already wrapped."""
#     def repl(m):
#         return rf"\eng{{{m.group(0)}}}"

#     chunks = re.split(r'(\\eng\{.*?\})', txt)  # protect existing
#     for i in range(0, len(chunks), 2):         # only outside blocks
#         chunks[i] = LATIN_TOKEN_RE.sub(repl, chunks[i])
#     return ''.join(chunks)

# # def escape_everything_except_eng(txt: str) -> str:
# #     """Escape LaTeX specials, but leave existing \eng{…} untouched."""
# #     pieces = ENG_BLOCK_RE.split(txt)
# #     for i, p in enumerate(pieces):
# #         if i % 2 == 0:                       # not an \eng{…} block
# #             pieces[i] = escape_latex(p, backslash=True)  # choose your own flags
# #     return "".join(pieces)

# def _escape_all_except_eng_blocks(text: str) -> str:
#     # Split into parts, keeping \eng{...}
#     parts = re.split(r'(\\eng2\{.*?\})', text)

#     escaped_parts = []
#     for part in parts:
#         if part.startswith(r'\eng2{'):
#             escaped_parts.append(part)  # don't escape
#         else:
#             escaped_parts.append(escape_latex(part))  # escape safely
#     return ''.join(escaped_parts)

# def _wrap_latin_segments_1(text: str) -> str:
#     def replacer(match):
#         return rf"\eng{{{match.group(0)}}}"
#     return re.sub(r'(?<!\\)[A-Za-z0-9_]{2,}', replacer, text)

# def is_hebrew_text(text: str) -> bool:
#     """Check if text contains Hebrew characters"""
#     return bool(HEBREW_PATTERN.search(text))

# def is_rtl_text(text: str) -> bool:
#     """Check if text is right-to-left (Hebrew or Arabic)"""
#     # Hebrew Unicode ranges
#     hebrew_chars = re.findall(r"[\u0590-\u05FF\uFB1D-\uFB4F]", text)
#     # Arabic Unicode ranges  
#     arabic_chars = re.findall(r"[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]", text)
    
#     rtl_chars = len(hebrew_chars) + len(arabic_chars)
#     return rtl_chars / max(len(text), 1) > 0.3

# def wrap_latin_segments_hebrew(text: str) -> str:
#     """Wrap Latin text segments in Hebrew context with LuaTeX direction markers"""
#     def repl(m):
#         # Use LuaTeX direction primitives instead of bidi package commands
#         return rf"\textdir TLT {{\eng{{{m.group(0)}}}}}\textdir TRT "
    
#     # Split on already wrapped blocks
#     parts = re.split(r'(\\(?:eng2?|textdir)\s*\w*\s*\{.*?\})', text, flags=re.S)
#     for i in range(0, len(parts), 2):  # only wrap unwrapped parts
#         parts[i] = LATIN_TOKEN_RE.sub(repl, parts[i])
#     return ''.join(parts)

# def wrap_hebrew_segments(text: str) -> str:
#     """Wrap Hebrew text segments properly for LuaTeX"""
#     if is_hebrew_text(text):
#         # For primarily Hebrew text, wrap Latin segments
#         return wrap_latin_segments_hebrew(text)
#     else:
#         # For primarily Latin text, use standard wrapping
#         return wrap_latin_segments(text)

# def escape_everything_except_hebrew_eng(text: str) -> str:
#     """Escape LaTeX except for inside Hebrew font commands and \\eng{...}"""
#     # Match Hebrew font commands and \eng{...} blocks and textdir commands
#     parts = re.split(r'(\\(?:hebrewfont|eng2?|textdir)\s*\w*\s*\{.*?\})', text)
    
#     for i in range(0, len(parts), 2):  # Only escape non-command parts
#         parts[i] = escape_latex(parts[i])
    
#     return ''.join(parts)

# # Update existing functions to handle Hebrew with LuaTeX
# def wrap_latin_segments(text: str) -> str:
#     """Enhanced version that handles Hebrew context with LuaTeX"""
#     if is_hebrew_text(text):
#         return wrap_hebrew_segments(text)
    
#     def repl(m):
#         return rf"\eng{{{m.group(0)}}}"
    
#     # Split on already wrapped blocks
#     parts = re.split(r'(\\eng2?\{.*?\})', text, flags=re.S)
#     for i in range(0, len(parts), 2):  # only wrap unwrapped parts
#         parts[i] = LATIN_TOKEN_RE.sub(repl, parts[i])
#     return ''.join(parts)

# def _wrap_latin_segments(text: str) -> str:
#     """Main wrapper function for Hebrew text processing"""
#     if is_hebrew_text(text):
#         # Use Hebrew-aware processing
#         def hebrew_repl(match):
#             return rf"\textdir TLT \eng{{{match.group(0)}}}\textdir TRT "
        
#         # Process Latin segments in Hebrew text
#         return LATIN_TOKEN_RE.sub(hebrew_repl, text)
#     else:
#         # Standard Latin processing
#         def latin_repl(match):
#             return rf"\eng{{{match.group(0)}}}"
#         return LATIN_TOKEN_RE.sub(latin_repl, text)

# def is_urdu_text(text: str) -> bool:
#     """Check if text contains Urdu/Arabic script characters"""
#     return bool(URDU_PATTERN.search(text))

# def is_arabic_text(text: str) -> bool:
#     """Check if text contains Arabic characters"""
#     return bool(ARABIC_PATTERN.search(text))

# def is_hebrew_text(text: str) -> bool:
#     """Check if text contains Hebrew characters"""
#     return bool(HEBREW_PATTERN.search(text))

# def is_rtl_text(text: str) -> bool:
#     """Check if text is right-to-left (Hebrew, Arabic, or Urdu)"""
#     # Hebrew Unicode ranges
#     hebrew_chars = re.findall(r"[\u0590-\u05FF\uFB1D-\uFB4F]", text)
#     # Arabic/Urdu Unicode ranges  
#     arabic_urdu_chars = re.findall(r"[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]", text)
    
#     rtl_chars = len(hebrew_chars) + len(arabic_urdu_chars)
#     return rtl_chars / max(len(text), 1) > 0.3

# def detect_text_language(text: str) -> str:
#     """Detect the primary language of text"""
#     if is_hebrew_text(text):
#         return "hebrew"
#     elif is_urdu_text(text) or is_arabic_text(text):
#         # For now, treat Arabic and Urdu similarly
#         # Could add more sophisticated detection later
#         return "urdu"  # or "arabic"
#     else:
#         return "latin"

# def wrap_latin_segments_urdu(text: str) -> str:
#     """Wrap Latin text segments in Urdu context with LuaTeX direction markers"""
#     def repl(m):
#         # Use LuaTeX direction primitives for Urdu context
#         return rf"\textdir TLT {{\eng{{{m.group(0)}}}}}\textdir TRT "
    
#     # Split on already wrapped blocks
#     parts = re.split(r'(\\(?:eng2?|textdir)\s*\w*\s*\{.*?\})', text, flags=re.S)
#     for i in range(0, len(parts), 2):  # only wrap unwrapped parts
#         parts[i] = LATIN_TOKEN_RE.sub(repl, parts[i])
#     return ''.join(parts)

# def wrap_urdu_segments(text: str) -> str:
#     """Wrap Urdu text segments properly for LuaTeX"""
#     if is_urdu_text(text):
#         # For primarily Urdu text, wrap Latin segments
#         return wrap_latin_segments_urdu(text)
#     else:
#         # For primarily Latin text, use standard wrapping
#         return wrap_latin_segments(text)

# def escape_everything_except_urdu_eng(text: str) -> str:
#     """Escape LaTeX except for inside Urdu font commands and \\eng{...}"""
#     # Match Urdu font commands and \eng{...} blocks and textdir commands
#     parts = re.split(r'(\\(?:urdufont|arabicfont|eng2?|textdir)\s*\w*\s*\{.*?\})', text)
    
#     for i in range(0, len(parts), 2):  # Only escape non-command parts
#         parts[i] = escape_latex(parts[i])
    
#     return ''.join(parts)

# # Enhanced main wrapper function
# def wrap_latin_segments(text: str) -> str:
#     """Enhanced version that handles Hebrew, Arabic, and Urdu contexts with LuaTeX"""
#     language = detect_text_language(text)
    
#     if language == "hebrew":
#         return wrap_hebrew_segments(text)
#     elif language == "urdu":
#         return wrap_urdu_segments(text)
#     else:
#         # Standard Latin processing
#         def repl(m):
#             return rf"\eng{{{m.group(0)}}}"
        
#         # Split on already wrapped blocks
#         parts = re.split(r'(\\eng2?\{.*?\})', text, flags=re.S)
#         for i in range(0, len(parts), 2):  # only wrap unwrapped parts
#             parts[i] = LATIN_TOKEN_RE.sub(repl, parts[i])
#         return ''.join(parts)

# def _wrap_latin_segments(text: str) -> str:
#     """Main wrapper function for multilingual text processing"""
#     language = detect_text_language(text)
    
#     if language == "hebrew":
#         # Use Hebrew-aware processing
#         def hebrew_repl(match):
#             return rf"\textdir TLT \eng{{{match.group(0)}}}\textdir TRT "
#         return LATIN_TOKEN_RE.sub(hebrew_repl, text)
    
#     elif language == "urdu":
#         # Use Urdu-aware processing
#         def urdu_repl(match):
#             return rf"\textdir TLT \eng{{{match.group(0)}}}\textdir TRT "
#         return LATIN_TOKEN_RE.sub(urdu_repl, text)
    
#     else:
#         # Standard Latin processing
#         def latin_repl(match):
#             return rf"\eng{{{match.group(0)}}}"
#         return LATIN_TOKEN_RE.sub(latin_repl, text)

# # Urdu-specific helper functions
# def format_urdu_numbers(text: str) -> str:
#     """Convert Latin numbers to Urdu context where appropriate"""
#     # This could be expanded to handle Urdu numerals if needed
#     number_pattern = re.compile(r'\b\d+\b')
    
#     def number_repl(match):
#         return rf"\urdunumbers{{{match.group(0)}}}"
    
#     return number_pattern.sub(number_repl, text)

# def handle_urdu_punctuation(text: str) -> str:
#     """Handle Urdu-specific punctuation spacing"""
#     # Add appropriate spacing around Urdu punctuation
#     text = re.sub(r'([۔؍؎؏؞؟])', r' \1 ', text)  # Urdu punctuation
#     text = re.sub(r'\s+', ' ', text)  # Clean up multiple spaces
#     return text.strip()

import re
from pylatex.utils import escape_latex
from pylatex import Command
from pylatex.utils import NoEscape

HEBREW_PATTERN = re.compile(r'[\u0590-\u05FF\uFB1D-\uFB4F]')
ARABIC_PATTERN = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]')
URDU_PATTERN = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]') 
PERSIAN_PATTERN = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF\u200C-\u200F]')  # Includes ZWNJ and other Persian-specific chars
LATIN_TOKEN_RE = re.compile(r'(?<!\\)([A-Za-z0-9][A-Za-z0-9_\-/+&%$@:.]*)')
ENG_BLOCK_RE = re.compile(r"(\\eng2\{.*?\})", re.S)

def wrap_latin_segments(text: str) -> str:
    """Wrap all Latin tokens (including numbers) with \eng{...}, skipping existing ones."""
    def repl(m):
        return rf"\eng{{{m.group(0)}}}"
    
    # Split on already wrapped blocks
    parts = re.split(r'(\\eng2?\{.*?\})', text, flags=re.S)
    for i in range(0, len(parts), 2):  # only wrap unwrapped parts
        parts[i] = LATIN_TOKEN_RE.sub(repl, parts[i])
    return ''.join(parts)

def escape_everything_except_eng(text: str) -> str:
    """Escape LaTeX except for inside \\eng{...} or \\eng2{...}."""
    # Match both \eng{...} and \eng2{...}
    parts = re.split(r'(\\eng2?\{.*?\})', text)
    
    for i in range(0, len(parts), 2):  # Only escape non-\eng parts
        parts[i] = escape_latex(parts[i])
    
    return ''.join(parts)

def clean_latin_in_eng_tag(text):
    # Join split Latin words inside \eng{}
    return re.sub(r'\\eng\{([^}]*)\\ ([^}]*)\}', lambda m: f"\\eng{{{m.group(1)}{m.group(2)}}}", text)

def is_latin_text(text: str) -> bool:
    # Heuristic: if >50% characters are Latin letters or numbers
    latin_chars = re.findall(r"[A-Za-z0-9]", text)
    return len(latin_chars) / max(len(text), 1) > 0.5

def is_hebrew_text(text: str) -> bool:
    """Check if text contains Hebrew characters"""
    return bool(HEBREW_PATTERN.search(text))

def is_arabic_text(text: str) -> bool:
    """Check if text contains Arabic characters"""
    return bool(ARABIC_PATTERN.search(text))

def is_urdu_text(text: str) -> bool:
    """Check if text contains Urdu/Arabic script characters"""
    return bool(URDU_PATTERN.search(text))

def is_persian_text(text: str) -> bool:
    """Check if text contains Persian/Farsi characters"""
    return bool(PERSIAN_PATTERN.search(text))

def is_rtl_text(text: str) -> bool:
    """Check if text is right-to-left (Hebrew, Arabic, Urdu, or Persian)"""
    # Hebrew Unicode ranges
    hebrew_chars = re.findall(r"[\u0590-\u05FF\uFB1D-\uFB4F]", text)
    # Arabic/Urdu/Persian Unicode ranges  
    arabic_script_chars = re.findall(r"[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]", text)
    
    rtl_chars = len(hebrew_chars) + len(arabic_script_chars)
    return rtl_chars / max(len(text), 1) > 0.3

def detect_text_language(text: str) -> str:
    """Detect the primary language of text with Persian support"""
    if is_hebrew_text(text):
        return "hebrew"
    elif is_persian_text(text):
        # Persian detection - check for Persian-specific characters or patterns
        persian_specific = re.search(r'[\u06A9\u06AF\u06CC\u06F0-\u06F9\u200C]', text)  # ک، گ، ی، Persian digits, ZWNJ
        if persian_specific:
            return "persian"
        # If no specific Persian markers but has Arabic script, could be Arabic/Urdu
        elif is_urdu_text(text) or is_arabic_text(text):
            # Fallback to Persian if no other clear indicators
            return "persian"  # Default to Persian for Arabic script
    elif is_urdu_text(text) or is_arabic_text(text):
        return "urdu"  # or "arabic"
    else:
        return "latin"

def wrap_latin_segments_persian(text: str) -> str:
    """Wrap Latin text segments in Persian context with LuaTeX direction markers"""
    def repl(m):
        # Use LuaTeX direction primitives for Persian context
        return rf"\textdir TLT {{\eng{{{m.group(0)}}}}}\textdir TRT "
    
    # Split on already wrapped blocks
    parts = re.split(r'(\\(?:eng2?|textdir)\s*\w*\s*\{.*?\})', text, flags=re.S)
    for i in range(0, len(parts), 2):  # only wrap unwrapped parts
        parts[i] = LATIN_TOKEN_RE.sub(repl, parts[i])
    return ''.join(parts)

def wrap_persian_segments(text: str) -> str:
    """Wrap Persian text segments properly for LuaTeX"""
    if is_persian_text(text):
        # For primarily Persian text, wrap Latin segments
        return wrap_latin_segments_persian(text)
    else:
        # For primarily Latin text, use standard wrapping
        return wrap_latin_segments(text)

def escape_everything_except_persian_eng(text: str) -> str:
    """Escape LaTeX except for inside Persian font commands and \\eng{...}"""
    # Match Persian font commands and \eng{...} blocks and textdir commands
    parts = re.split(r'(\\(?:persianfont|arabicfont|eng2?|textdir)\s*\w*\s*\{.*?\})', text)
    
    for i in range(0, len(parts), 2):  # Only escape non-command parts
        parts[i] = escape_latex(parts[i])
    
    return ''.join(parts)

# Enhanced main wrapper function
def wrap_latin_segments(text: str) -> str:
    """Enhanced version that handles Hebrew, Arabic, Urdu, and Persian contexts with LuaTeX"""
    language = detect_text_language(text)
    
    if language == "hebrew":
        return wrap_hebrew_segments(text)
    elif language == "urdu":
        return wrap_urdu_segments(text)
    elif language == "persian":
        return wrap_persian_segments(text)
    else:
        # Standard Latin processing
        def repl(m):
            return rf"\eng{{{m.group(0)}}}"
        
        # Split on already wrapped blocks
        parts = re.split(r'(\\eng2?\{.*?\})', text, flags=re.S)
        for i in range(0, len(parts), 2):  # only wrap unwrapped parts
            parts[i] = LATIN_TOKEN_RE.sub(repl, parts[i])
        return ''.join(parts)

def _wrap_latin_segments(text: str) -> str:
    """Main wrapper function for multilingual text processing"""
    language = detect_text_language(text)
    
    if language == "hebrew":
        # Use Hebrew-aware processing
        def hebrew_repl(match):
            return rf"\textdir TLT \eng{{{match.group(0)}}}\textdir TRT "
        return LATIN_TOKEN_RE.sub(hebrew_repl, text)
    
    elif language == "urdu":
        # Use Urdu-aware processing
        def urdu_repl(match):
            return rf"\textdir TLT \eng{{{match.group(0)}}}\textdir TRT "
        return LATIN_TOKEN_RE.sub(urdu_repl, text)
    
    elif language == "persian":
        # Use Persian-aware processing
        def persian_repl(match):
            return rf"\textdir TLT \eng{{{match.group(0)}}}\textdir TRT "
        return LATIN_TOKEN_RE.sub(persian_repl, text)
    
    else:
        # Standard Latin processing
        def latin_repl(match):
            return rf"\eng{{{match.group(0)}}}"
        return LATIN_TOKEN_RE.sub(latin_repl, text)

# Persian-specific helper functions
def format_persian_numbers(text: str) -> str:
    """Convert Latin numbers to Persian numerals where appropriate"""
    # Persian numerals: ۰۱۲۳۴۵۶۷۸۹
    persian_numerals = '۰۱۲۳۴۵۶۷۸۹'
    latin_numerals = '0123456789'
    
    # Create translation table
    translation = str.maketrans(latin_numerals, persian_numerals)
    
    # Apply translation to numbers in the text
    def replace_numbers(match):
        number = match.group(0)
        return number.translate(translation)
    
    return re.sub(r'\b\d+\b', replace_numbers, text)

def handle_persian_punctuation(text: str) -> str:
    """Handle Persian-specific punctuation spacing and characters"""
    # Persian punctuation marks: ؟ ؍ ؎ ؏ ؞ ٪ ٫ ٬
    # Add appropriate spacing around Persian punctuation
    text = re.sub(r'([؟؍؎؏؞٪٫٬])', r' \1 ', text)  # Persian punctuation
    
    # Handle Persian decimal separator and thousands separator
    text = re.sub(r'([٫٬])', r'\1 ', text)  # Add space after Persian separators
    
    # Clean up multiple spaces
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def normalize_persian_text(text: str) -> str:
    """Normalize Persian text by handling common character variations"""
    # Normalize Persian/Arabic characters that have variants
    normalizations = {
        'ي': 'ی',  # Arabic yeh to Persian yeh
        'ك': 'ک',  # Arabic kaf to Persian kaf  
        'ۀ': 'ه',  # Persian heh with hamza to regular heh (optional)
        'ء': 'ٔ',  # Hamza to hamza above (optional)
    }
    
    for old_char, new_char in normalizations.items():
        text = text.replace(old_char, new_char)
    
    return text

# Existing functions for other languages (Hebrew, Urdu, etc.)
def wrap_latin_segments_hebrew(text: str) -> str:
    """Wrap Latin text segments in Hebrew context with LuaTeX direction markers"""
    def repl(m):
        # Use LuaTeX direction primitives instead of bidi package commands
        return rf"\textdir TLT {{\eng{{{m.group(0)}}}}}\textdir TRT "
    
    # Split on already wrapped blocks
    parts = re.split(r'(\\(?:eng2?|textdir)\s*\w*\s*\{.*?\})', text, flags=re.S)
    for i in range(0, len(parts), 2):  # only wrap unwrapped parts
        parts[i] = LATIN_TOKEN_RE.sub(repl, parts[i])
    return ''.join(parts)

def wrap_hebrew_segments(text: str) -> str:
    """Wrap Hebrew text segments properly for LuaTeX"""
    if is_hebrew_text(text):
        # For primarily Hebrew text, wrap Latin segments
        return wrap_latin_segments_hebrew(text)
    else:
        # For primarily Latin text, use standard wrapping
        return wrap_latin_segments(text)

def escape_everything_except_hebrew_eng(text: str) -> str:
    """Escape LaTeX except for inside Hebrew font commands and \\eng{...}"""
    # Match Hebrew font commands and \eng{...} blocks and textdir commands
    parts = re.split(r'(\\(?:hebrewfont|eng2?|textdir)\s*\w*\s*\{.*?\})', text)
    
    for i in range(0, len(parts), 2):  # Only escape non-command parts
        parts[i] = escape_latex(parts[i])
    
    return ''.join(parts)

def wrap_latin_segments_urdu(text: str) -> str:
    """Wrap Latin text segments in Urdu context with LuaTeX direction markers"""
    def repl(m):
        # Use LuaTeX direction primitives for Urdu context
        return rf"\textdir TLT {{\eng{{{m.group(0)}}}}}\textdir TRT "
    
    # Split on already wrapped blocks
    parts = re.split(r'(\\(?:eng2?|textdir)\s*\w*\s*\{.*?\})', text, flags=re.S)
    for i in range(0, len(parts), 2):  # only wrap unwrapped parts
        parts[i] = LATIN_TOKEN_RE.sub(repl, parts[i])
    return ''.join(parts)

def wrap_urdu_segments(text: str) -> str:
    """Wrap Urdu text segments properly for LuaTeX"""
    if is_urdu_text(text):
        # For primarily Urdu text, wrap Latin segments
        return wrap_latin_segments_urdu(text)
    else:
        # For primarily Latin text, use standard wrapping
        return wrap_latin_segments(text)

def escape_everything_except_urdu_eng(text: str) -> str:
    """Escape LaTeX except for inside Urdu font commands and \\eng{...}"""
    # Match Urdu font commands and \eng{...} blocks and textdir commands
    parts = re.split(r'(\\(?:urdufont|arabicfont|eng2?|textdir)\s*\w*\s*\{.*?\})', text)
    
    for i in range(0, len(parts), 2):  # Only escape non-command parts
        parts[i] = escape_latex(parts[i])
    
    return ''.join(parts)

# Other utility functions
def _wrap_latin_segments(text: str) -> str:
    # Skip LaTeX commands (e.g., \textbf{...}, \section, etc.)
    def latex_command_replacer(match):
        return match.group(0)  # Don't touch commands

    def replacer(match):
        segment = match.group(0)
        if re.search(r'[A-Za-z]', segment):  # Ensure real Latin content
            return rf'\eng{{{segment.strip()}}}'
        return segment

    # Protect LaTeX commands first
    protected_text = re.sub(r'\\[a-zA-Z]+\*?(?:\[[^\]]*\])?(?:\{[^}]*\})*', latex_command_replacer, text)

    # Now wrap Latin segments, including words with punctuation or digits
    return re.sub(r'(?<!\\)([A-Za-z0-9][A-Za-z0-9_ .,:;!?/\-\'"()&%$@]*)', replacer, protected_text)

def _escape_all_except_eng_blocks(text: str) -> str:
    # Split into parts, keeping \eng{...}
    parts = re.split(r'(\\eng2\{.*?\})', text)

    escaped_parts = []
    for part in parts:
        if part.startswith(r'\eng2{'):
            escaped_parts.append(part)  # don't escape
        else:
            escaped_parts.append(escape_latex(part))  # escape safely
    return ''.join(escaped_parts)

def _wrap_latin_segments_1(text: str) -> str:
    def replacer(match):
        return rf"\eng{{{match.group(0)}}}"
    return re.sub(r'(?<!\\)[A-Za-z0-9_]{2,}', replacer, text)

# Urdu-specific helper functions
def format_urdu_numbers(text: str) -> str:
    """Convert Latin numbers to Urdu context where appropriate"""
    # This could be expanded to handle Urdu numerals if needed
    number_pattern = re.compile(r'\b\d+\b')
    
    def number_repl(match):
        return rf"\urdunumbers{{{match.group(0)}}}"
    
    return number_pattern.sub(number_repl, text)

def handle_urdu_punctuation(text: str) -> str:
    """Handle Urdu-specific punctuation spacing"""
    # Add appropriate spacing around Urdu punctuation
    text = re.sub(r'([۔؍؎؏؞؟])', r' \1 ', text)  # Urdu punctuation
    text = re.sub(r'\s+', ' ', text)  # Clean up multiple spaces
    return text.strip()