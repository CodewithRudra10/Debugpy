# DebugMate

**Teach the error, not just the fix.**

DebugMate is an AI-powered Python debugging assistant designed to help learners understand why their programs fail. It runs a Python file, identifies errors from tracebacks, locates the relevant source line, and uses Google's Gemini API to explain the problem and suggest a fix.

## Features

- Runs Python files from the command line.
- Identifies error types and messages from Python tracebacks.
- Locates the relevant source file and line number.
- Provides an AI-generated explanation, possible cause, and suggested fix.
- Handles missing files, missing API keys, and analysis failures with error messages.
- Includes a timeout for programs that run too long.

## Requirements

- Python version compatible with the project's code and installed dependencies.
- A Google Gemini API key.
- Internet access for Gemini-powered analysis.

## Installation

1. Clone or download this repository.
2. Open a terminal in the project directory.
3. Create and activate a virtual environment:

   **Windows (PowerShell):**

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

4. Install dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

## Configure your Gemini API key

Obtain an API key through Google's official AI developer platform.

Set the key in your current PowerShell session:

```powershell
$env:GEMINI_API_KEY = "YOUR_API_KEY"
```

Replace `YOUR_API_KEY` with your own key. Never commit API keys to GitHub or share them publicly.

The key set this way applies to the current terminal session. Set it again in a new session when needed.

## Usage

Display available commands:

```powershell
python -m debugmate.interface.cli --help
```

Display the version:

```powershell
python -m debugmate.interface.cli --version
```

Run and analyze a Python file:

```powershell
python -m debugmate.interface.cli run app.py
```

DebugMate prints the program's standard output and, when an error occurs, attempts to analyze the traceback and request a Gemini diagnosis.

## Example diagnosis

A diagnosis may include:

- **Error type:** `IndexError`
- **Cause:** The code tries to access a list element that does not exist.
- **Suggested fix:** Check the list length or use a valid index.
- **Explanation:** Python lists use zero-based indexing.

AI-generated diagnoses may be incomplete or incorrect. Review suggestions and understand them before changing your code.

## Safety and limitations

**Important:** DebugMate executes the Python file you provide. Python programs can read, modify, or delete files, access the network, and perform other actions with your permissions. Only run code you trust.

The execution timeout is not a security sandbox and does not make untrusted code safe.

DebugMate relies on Python traceback parsing and an external AI service. It may not correctly analyze every error or traceback format. Gemini-powered analysis requires a valid API key, network access, and a supported model configuration. Suggested fixes are not automatically applied.

## Project status

DebugMate v0.1.0 is an early release. Feedback, bug reports, and contributions are welcome.

## Dependencies

The required Python package is listed in [`requirements.txt`](requirements.txt).

## License

See the `LICENSE` file for the project's license terms.


