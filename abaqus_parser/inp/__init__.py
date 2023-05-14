from typing import Union, Sequence
from io import StringIO
import logging
from collections import abc

import abaqus_parser
from abaqus_parser.inp import util
from abaqus_parser.inp import _parser
from abaqus_parser.inp import _lexer

LOGGER = abaqus_parser.LOGGER.getChild(__name__)  # type: logging.Logger
INP_DATA = Sequence[Union[str, abc.Mapping]]


def read_from_file(file_path: str):
    with open(file_path, "r") as inp_file:
        return read(inp_file)


def read_from_string(s: str):
    return read(StringIO(s))


def read(io) -> INP_DATA:
    lex = _lexer.lexer.clone()

    def token_generator():
        read_bytes = 3_500
        print_interval = 100_000
        last_print_interval = 0
        line_no = -1

        lines = io.readlines(read_bytes)
        while len(lines) > 0:
            line_no += len(lines)
            lines = [line.strip() for line in lines]
            lines = "\n".join(filter(None, lines)) + "\n"

            if lines != "\n":
                lex.input(lines)
                token = lex.token()
                while token is not None:
                    yield token
                    token = lex.token()

            if line_no // print_interval > last_print_interval:
                LOGGER.info(f"parse abaqus input line {line_no:>8_d}")
                last_print_interval = line_no // print_interval

            lines = io.readlines(read_bytes)

        return None

    def token_function_factory():
        b = token_generator()

        def token_function():
            return next(b, None)

        return token_function

    return _parser.parser.parse(lexer=lex, tokenfunc=token_function_factory())


def write_to_file(file_path: str, inp_data: INP_DATA):
    with open(file_path, "w") as inp_file:
        write(inp_file, inp_data)


def write_to_string(inp_data: INP_DATA):
    s = StringIO()
    write(s, inp_data)
    return s.getvalue()


def write(io, inp_data: INP_DATA):
    if isinstance(io, str):
        io = open(io, "w")

    for line in inp_data:
        if isinstance(line, abc.Mapping):
            # keyword block
            util.write_keyword_header(io, line)

            for sub_line in line["data"]:
                if sub_line[:2] == "**":
                    # comment line
                    util.write_comment_line(io, sub_line)
                else:
                    # data line
                    util.write_data_line(io, sub_line)
        else:
            # comment line
            util.write_comment_line(io, line)
