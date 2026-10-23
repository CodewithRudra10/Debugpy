
import os
from dataclasses import dataclass
from pathlib import Path

from .parser import ParsedError


@dataclass
class LocatedError:
    file: str
    line: int
    source: str


def locate_error(parsed_error: ParsedError) -> LocatedError:
    file_path = Path(parsed_error.file)

    # Resolve relative paths from the current working directory.
    # Windows paths such as "\locator.py" are root-relative rather
    # than fully absolute, so resolve them from the current directory.
    if os.name == "nt" and file_path.root and not file_path.drive:
        file_path = Path.cwd() / str(file_path).lstrip("\\/")
    elif not file_path.is_absolute():
        file_path = Path.cwd() / file_path

    file_path = file_path.resolve()

    if not file_path.is_file():
        raise FileNotFoundError(
            f"Source file not found: {file_path}"
        )

    with file_path.open("r", encoding="utf-8") as source_file:
        lines = source_file.readlines()

    if parsed_error.line < 1 or parsed_error.line > len(lines):
        raise IndexError(
            f"Line {parsed_error.line} is outside the file's "
            f"line range (1-{len(lines)})."
        )

    source = lines[parsed_error.line - 1]

    return LocatedError(
        file=str(file_path),
        line=parsed_error.line,
        source=source,
    )
