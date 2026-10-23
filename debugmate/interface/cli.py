
import argparse
import subprocess
import sys

from debugmate.core.parser import parse_traceback
from debugmate.core.locator import locate_error
from debugmate.core.analyzer import analyze_error
from debugmate.providers import GeminiProvider


def main():
    parser = argparse.ArgumentParser(
        prog="debugmate",
        description="DebugMate - AI-powered Python debugging assistant",
    )

    parser.add_argument(
        "--version",
        action="version",
        version="DebugMate 0.1.0",
    )

    subparsers = parser.add_subparsers(dest="command")

    run_parser = subparsers.add_parser(
        "run",
        help="Run a Python file and analyze errors",
    )

    run_parser.add_argument(
        "file",
        help="Path to the Python file to run",
    )

    args = parser.parse_args()

    if args.command != "run":
        parser.print_help()
        return

    try:
        result = subprocess.run(
            [sys.executable, args.file],
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )

        if result.stdout:
            print(result.stdout, end="")

        if result.returncode == 0:
            print("Program completed successfully.")
            return

        print("Program failed:")

        stderr = result.stderr or ""

        if (
            "can't open file" in stderr.lower()
            or "no such file or directory" in stderr.lower()
        ):
            print("Error: The specified Python file could not be found.")
            print(stderr.strip())
            return

        try:
            parsed_error = parse_traceback(stderr)
            located_error = locate_error(parsed_error)

        except (ValueError, IndexError, FileNotFoundError) as error:
            print("DebugMate couldn't analyze the traceback.")
            print(f"Details: {error}")

            if stderr:
                print(stderr)

            return

        try:
            provider = GeminiProvider(
                model="gemini-3.5-flash-lite"
            )

            diagnosis = analyze_error(
                parsed_error=parsed_error,
                located_error=located_error,
                provider=provider,
            )

            print("\n--- DebugMate Diagnosis ---")
            print(f"Error type: {diagnosis.error_type}")
            print(f"Cause: {diagnosis.cause}")
            print(f"Suggested fix: {diagnosis.suggested_fix}")
            print(f"Explanation: {diagnosis.explanation}")

        except Exception as error:
            print("DebugMate's AI analysis failed.")
            print(f"Details: {error}")

            if stderr:
                print(stderr)

    except subprocess.TimeoutExpired:
        print("Error: Program exceeded the 30-second timeout.")

    except FileNotFoundError:
        print("Error: Python executable or file could not be found.")


if __name__ == "__main__":
    main()
