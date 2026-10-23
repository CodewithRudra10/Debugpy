
import re
from dataclasses import dataclass


@dataclass
class ParsedError:
    error_type: str
    message: str
    file: str
    line: int


def parse_traceback(traceback_text: str) -> ParsedError:
    """Extract the error type, message, file, and line from a Python traceback."""

    if not isinstance(traceback_text, str) or not traceback_text.strip():
        raise ValueError("Traceback must be a non-empty string.")

    lines = traceback_text.strip().splitlines()

    # The final non-empty line normally contains the exception.
    error_line = lines[-1].strip()

    # Support exception names such as ValueError and package.CustomError.
    error_match = re.match(
        r"^([A-Za-z_][\w.]*)\s*(?::\s*(.*))?$",
        error_line,
    )

    if not error_match:
        raise ValueError("Could not identify the exception in the traceback.")

    error_type = error_match.group(1)
    message = error_match.group(2) or ""

    # Find the last traceback frame, which identifies the relevant source line.
    frame_pattern = re.compile(
        r'^\s*File "(.+)", line (\d+)(?:, in .*)?$'
    )

    for line in reversed(lines[:-1]):
        frame_match = frame_pattern.match(line)
        if frame_match:
            return ParsedError(
                error_type=error_type,
                message=message,
                file=frame_match.group(1),
                line=int(frame_match.group(2)),
            )

    raise ValueError("Could not locate a source file and line in the traceback.")
