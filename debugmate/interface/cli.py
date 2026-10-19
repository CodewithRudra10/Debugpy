
import subprocess
import argparse


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
                print(result.stderr)

            else:
                print("Program completed successfully.")

        except subprocess.TimeoutExpired:
            print("Error: Program exceeded the 30-second timeout.")

        except FileNotFoundError:
            print("Error: Python executable or file could not be found.")


if __name__ == "__main__":
    main()
