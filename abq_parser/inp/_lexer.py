import ply.lex as lex
import re
import json

tokens = (
    "EFFICIENT_DATA_LINES",
    "COMMENT",
    "KEYWORD",
    "COMMA",
    "ASSIGNMENT",
    "QUOTED",
    "INTEGER",
    "FLOAT",
    "STRING",
    "NEW_LINE",
)

s = r"[\ \t]*"


@lex.TOKEN(
    r"^(" + (
            s + r"[\+\-]?\d+(\.\d+)?(E[\+\-]?\d+)?"
            + "(" + (
                s + r","
                + s + r"[\+\-]?\d+(\.\d+)?(E[\+\-]?\d+)?"
            ) + ")+"
    ) + s + r"\n)+")
def t_EFFICIENT_DATA_LINES(t):
    t.value = json.loads("[[" + t.value[:-1].replace("\n", "],[") + "]]")
    return t


@lex.TOKEN(r"^\*\*.*$")
def t_COMMENT(t):
    return t


@lex.TOKEN(r"^\*[A-Z][A-Z\d\ \t]*(?=,|$)")
def t_KEYWORD(t):
    t.value = str(t.value).strip().upper()
    return t


@lex.TOKEN(s + r",")
def t_COMMA(t):
    return t


@lex.TOKEN(s + r"=")
def t_ASSIGNMENT(t):
    return t


@lex.TOKEN(s + r"(\"[^\"]*\"|'[^']*')")
def t_QUOTED(t):
    return t


@lex.TOKEN(s + r"(?<![\.\d\+\-])[\+\-]?\d+(?![\.ED\d])")
def t_INTEGER(t):
    return t


@lex.TOKEN(s + r"[\+\-]?(\d+(\.\d*)?|\.\d+)([ED][\+\-]?\d+)?")
def t_FLOAT(t):
    return t


@lex.TOKEN(s + r"\w[^=,\n]*")
def t_STRING(t):
    return t


@lex.TOKEN(s + r"\n+" + s)
def t_NEW_LINE(t):
    t.lexer.lineno += 1
    return t


def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lineno} at lexpos {t.lexpos}")
    t.lexer.skip(1)


lexer = lex.lex(
    debug=False,
    optimize=True,
    reflags=re.VERBOSE | re.IGNORECASE | re.MULTILINE,
    lextab="_lextab"
)
