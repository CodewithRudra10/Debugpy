from debugmate.core.analyzer import analyze_error
from debugmate.core.parser import ParsedError
from debugmate.core.locator import LocatedError
from debugmate.providers.gemini import GeminiProvider

parsed = ParsedError(
    error_type="IndexError",
    message="list index out of range",
    file="app.py",
    line=4,
)

located = LocatedError(
    file="app.py",
    line=4,
    source="print(numbers[5])",
)

provider = GeminiProvider(model="gemini-3.5-flash-lite")

result = analyze_error(parsed, located, provider)

print("Error Type:", result.error_type)
print("Cause:", result.cause)
print("Suggested Fix:", result.suggested_fix)
print("Explanation:", result.explanation)