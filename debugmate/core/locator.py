import os
from dataclasses import dataclass

from .parser import ParsedError


@dataclass
class LocatedError:
    file: str
    line: int
    source: str


def locate_error(parsed_error: ParsedError) -> LocatedError:
    file_path = parsed_error.file

    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"Source file not found: {os.path.abspath(file_path)}"
        )

    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    if parsed_error.line < 1 or parsed_error.line > len(lines):
        raise IndexError(
            f"Line {parsed_error.line} is outside the file's "
            f"line range (1-{len(lines)})."
        )

    source = lines[parsed_error.line - 1]

    return LocatedError(
        file=file_path,
        line=parsed_error.line,
        source=source
    )

