import argparse
import subprocess
import sys
from pathlib import Path


def main():
    """CLI entry point for runt-hq"""

    parser = argparse.ArgumentParser(description="Runt HQ API server")
    parser.add_argument(
        "--dev",
        action="store_true",
        default=False,
        help="Run in development mode with auto-reload",
    )
    parser.add_argument(
        "args", nargs="*", help="Additional arguments to pass to fastapi"
    )

    parsed_args = parser.parse_args()

    main_py_path = Path(__file__).parent / "main.py"

    if parsed_args.dev:
        cmd = ["fastapi", "dev", str(main_py_path)]
    else:
        cmd = ["fastapi", "serve", str(main_py_path)]

    cmd.extend(parsed_args.args)

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        sys.exit(e.returncode)
    except FileNotFoundError:
        print(
            "Error: fastapi command not found. Make sure fastapi[standard] is installed."
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
