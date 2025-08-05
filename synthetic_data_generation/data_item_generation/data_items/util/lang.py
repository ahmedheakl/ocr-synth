
import re
from pylatex.utils import escape_latex
from pylatex import Command
from pylatex.utils import NoEscape

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


def is_latin_text(text: str) -> bool:
    # Heuristic: if >50% characters are Latin letters or numbers
    latin_chars = re.findall(r"[A-Za-z0-9]", text)
    return len(latin_chars) / max(len(text), 1) > 0.5


def wrap_latin_segments(txt: str) -> str:
    """Wrap every Latin token in \eng{…}, unless already wrapped."""
    def repl(m):
        return rf"\eng{{{m.group(0)}}}"

    chunks = re.split(r'(\\eng\{.*?\})', txt)  # protect existing
    for i in range(0, len(chunks), 2):         # only outside blocks
        chunks[i] = LATIN_TOKEN_RE.sub(repl, chunks[i])
    return ''.join(chunks)

# def escape_everything_except_eng(txt: str) -> str:
#     """Escape LaTeX specials, but leave existing \eng{…} untouched."""
#     pieces = ENG_BLOCK_RE.split(txt)
#     for i, p in enumerate(pieces):
#         if i % 2 == 0:                       # not an \eng{…} block
#             pieces[i] = escape_latex(p, backslash=True)  # choose your own flags
#     return "".join(pieces)

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