import logging
from collections import UserString

import numpy as np

import abaqus_parser

LOGGER = abaqus_parser.LOGGER.getChild(__name__)  # type: logging.Logger


def write_comment_line(io, line):
    io.write(str(line) + "\n")


def write_keyword_header(io, line):
    header = ", ".join([line["keyword"]] + [
        f"{key}" if value is None else f"{key}={value}"
        for key, value in line["parameters"].items()
    ])
    while len(header) > 256:
        split_at = header[:256].rfind(",") + 1

        if split_at == 0 or split_at > 256:
            LOGGER.error("Line exceeds the maximum width of 256 chars: \n"
                         "" + line)
            break

        io.write(header[:split_at] + "\n")
        header = header[split_at:]

    io.write(header + "\n")


def write_data_line(io, sub_line):
    io.write(", ".join([
        "" if entry is None else str(entry)
        for entry in sub_line
    ]) + f"{',' if len(sub_line) == 1 else ''}\n")


def to_string(entry):
    if isinstance(entry, str):
        return entry
    elif isinstance(entry, (int, np.integer)):
        return f"{entry:d}"
    elif isinstance(entry, (float, np.floating)):
        return f"{entry:.16g}"
    elif isinstance(entry, UserString):
        return str(entry)
    else:
        return str(entry)
