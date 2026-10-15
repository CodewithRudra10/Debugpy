
# import os
# from google import genai

# api_key = os.getenv("GEMINI_API_KEY")

# if not api_key:
#     raise ValueError("GEMINI_API_KEY is not set.")

# client = genai.Client(api_key=api_key)

# for model in client.models.list():
#     if "generateContent" in (model.supported_actions or []):
#         print(model.name)


from debugmate.providers.gemini import GeminiProvider

provider = GeminiProvider(model="gemini-2.5-flash-lite")

result = provider.analyze(
    error_type="IndexError",
    error_message="list index out of range",
    source_code="numbers = [10, 20, 30]\nprint(numbers[5])",
    instructions=(
        "Explain why this error occurs and suggest a safe fix. "
        "Do not execute the code."
    ),
)

print("Error type:", result.error_type)
print("Cause:", result.cause)
print("Suggested fix:", result.suggested_fix)
print("Explanation:", result.explanation)
