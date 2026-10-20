
import argparse
import subprocess

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

    if args.command == "run":
        try:
            result = subprocess.run(
                ["python", args.file],
                capture_output=True,
                text=True,
                timeout=30,
                check=False,
            )

            if result.stdout:
                print(result.stdout, end="")

            if result.returncode != 0:
                print("Program failed:")

                try:
                    parsed_error = parse_traceback(result.stderr)
                    located_error = locate_error(parsed_error)

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

                except (ValueError, IndexError, FileNotFoundError) as error:
                    print("DebugMate couldn't analyze the traceback.")
                    print(f"Details: {error}")
                    print(result.stderr)

                except Exception as error:
                    print("DebugMate's AI analysis failed.")
                    print(f"Details: {error}")
                    print(result.stderr)

            else:
                print("Program completed successfully.")

        except subprocess.TimeoutExpired:
            print("Error: Program exceeded the 30-second timeout.")

        except FileNotFoundError:
            print("Error: Python executable or file could not be found.")


if __name__ == "__main__":
    main()
