from debugmate.core.parser import ParsedError
from debugmate.core.locator import LocatedError
from debugmate.providers.base import AIProvider, AnalysisResult

def analyze_error(
    parsed_error: ParsedError,
    located_error: LocatedError,
    provider: AIProvider,
) -> AnalysisResult:


    error_type = parsed_error.error_type
    error_message = parsed_error.message
    source_code = located_error.source

    instructions = (
        "Explain why this error occurred and suggest a safe fix. "
        "Use the provided source code and error message. "
        "Do not execute the code or claim that the fix was tested."
    )

    result = provider.analyze(
        error_type=error_type,
        error_message=error_message,
        source_code=source_code,
        instructions=instructions,
    )

    return result