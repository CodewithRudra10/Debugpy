from dataclasses import dataclass
from .parser import ParsedError
from .locator import LocatedError

@dataclass
class Identifier:
    suggested_fix: str
    error_type : str
    error_cause : str

def analyze_error(
    parsed_error: ParsedError,
    located_error: LocatedError
) -> Identifier:
    pass

    error_type = parsed_error.error_type


    if error_type == "IndexError":
        cause = (
            "The code is trying to access an index "
            "that does not exist in the sequence."
        )

        suggested_fix = (
            "Check the sequence length and make sure "
            "the index is within the valid range. "
            "For a sequence of length n, valid positive "
            "indices range from 0 to n - 1."
        )

    else:
        cause = "The cause of this error is not supported yet."
        suggested_fix = (
            "Review the traceback and source code "
            "to identify the problem."
        )

    return Identifier(
        error_type=error_type,
        error_cause=cause,
        suggested_fix=suggested_fix
    )


from debugmate.core.analyzer import analyze_error
from debugmate.core.parser import ParsedError
from debugmate.core.locator import LocatedError

parsed = ParsedError(
    error_type="IndexError",
    message="list index out of range",
    file="app.py",
    line=4
)

located = LocatedError(
    file="app.py",
    line=4,
    source="print(numbers[5])"
)

result = analyze_error(parsed, located)

print("Error Type:", result.error_type)
print("Error Cause:", result.cause)
print("Suggested Fix:", result.suggested_fix)