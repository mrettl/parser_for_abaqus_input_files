import ply.yacc as yacc

from abq_parser.inp._lexer import tokens

precedence = [
    ["left", "START_WITH_COMMENT"],
    ["left"] + list(tokens),
]


def p_document_empty(p):
    """document : empty"""
    p[0] = list()


def p_document_comment(p):
    """document : comment_line document  %prec START_WITH_COMMENT"""
    p[0] = [p[1]]
    p[0].extend(p[2])


def p_document_keyword_block(p):
    """document : document keyword_block"""
    p[0] = p[1]
    p[0].append(p[2])


def p_keyword_block(p):
    """keyword_block : keyword_header data_lines"""
    p[0] = p[1]
    p[0]["data"] = p[2]


def p_keyword_header(p):
    """keyword_header : KEYWORD parameter_list NEW_LINE"""
    p[0] = dict(keyword=p[1], parameters=p[2])


def p_parameter_list_empty(p):
    """parameter_list : empty"""
    p[0] = dict()


def p_parameter_list_parameter(p):
    """parameter_list : parameter_list COMMA parameter"""
    p[0] = p[1]
    p[0].update(p[3])


def p_parameter_list_continuation_line(p):
    """parameter_list : parameter_list COMMA NEW_LINE parameter"""
    p[0] = p[1]
    p[0].update(p[4])


def p_parameter_flag(p):
    """parameter : STRING"""
    p[0] = {str(p[1]).strip().upper(): None}


def p_parameter_assignment(p):
    """parameter : STRING ASSIGNMENT entry"""
    p[0] = {str(p[1]).strip().upper(): p[3]}


def p_data_lines_empty(p):
    """data_lines : empty"""
    p[0] = list()


def p_data_lines_data_line(p):
    """data_lines : data_lines data_line """
    p[0] = p[1]
    p[0].append(p[2])


def p_data_lines_comment_line(p):
    """data_lines : data_lines comment_line"""
    p[0] = p[1]
    p[0].append(p[2])


def p_data_lines_optimized(p):
    """data_lines : data_lines EFFICIENT_DATA_LINES"""
    p[0] = p[1]
    p[0].extend(p[2])


def p_comment_line(p):
    """comment_line : COMMENT NEW_LINE"""
    p[0] = p[1]


def p_data_line_single_entry(p):
    """data_line : entry COMMA NEW_LINE
                 | entry NEW_LINE"""
    p[0] = [p[1]]


def p_data_line_single_entry_empty(p):
    """data_line : COMMA NEW_LINE"""
    p[0] = [None]


def p_data_line(p):
    """data_line : entry_list NEW_LINE"""
    p[0] = p[1]


def p_entry_list_start_1(p):
    """entry_list : entry COMMA entry"""
    p[0] = [p[1], p[3]]


def p_entry_list_start_2(p):
    """entry_list : COMMA entry"""
    p[0] = [None, p[2]]


def p_entry_list_start_3(p):
    """entry_list : entry COMMA COMMA entry
                  | entry COMMA COMMA empty"""
    p[0] = [p[1], None, p[4]]


def p_entry_list_start_4(p):
    """entry_list : COMMA COMMA entry
                  | COMMA COMMA empty"""
    p[0] = [None, None, p[3]]


def p_entry_sequence_empty(p):
    """entry_list : entry_list COMMA empty"""
    p[0] = p[1]
    p[0].append(None)


def p_entry_sequence(p):
    """entry_list : entry_list COMMA entry"""
    p[0] = p[1]
    p[0].append(p[3])


def p_entry_quoted(p):
    """entry : QUOTED"""
    p[0] = str(p[1]).strip()


def p_entry_string(p):
    """entry : STRING"""
    p[0] = str(p[1]).strip().upper()


def p_entry_integer(p):
    """entry : INTEGER"""
    p[0] = int(p[1])


def p_entry_float(p):
    """entry : FLOAT"""
    p[0] = float(str(p[1]).upper().replace("D", "E"))


def p_entry_text(p):
    """entry : STRING INTEGER
             | STRING FLOAT
             | INTEGER STRING
             | FLOAT STRING
             | INTEGER INTEGER
             | INTEGER FLOAT
             | FLOAT FLOAT
             | FLOAT INTEGER"""
    p[0] = (str(p[1]) + str(p[2])).upper()


def p_empty(p):
    """empty : """
    pass


def p_error(p):
    if p is None:
        print("Make sure the file ends with exactly one blank line")
    else:
        print(f"error: {p}")


parser = yacc.yacc(
    start="document",
    debug=False,
    optimize=True,
    tabmodule="_parsetab"
)
