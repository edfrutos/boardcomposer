"""CLI entry to run the optional HTTP adapter (EP-003)."""

from __future__ import annotations

import argparse
import sys

from boardcomposer.api.http import create_app
from boardcomposer.api.http.auth import ENV_API_KEY, configured_api_key


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="boardcomposer-serve",
        description=(
            "Run the optional BoardComposer HTTP adapter (Flask) over api.v1. "
            f"Set {ENV_API_KEY} to require X-API-Key / Bearer auth."
        ),
    )
    parser.add_argument("--host", default="127.0.0.1", help="Bind host")
    parser.add_argument("--port", type=int, default=8080, help="Bind port")
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Flask debug mode (local only)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return 0 if exc.code is None else int(exc.code)

    if configured_api_key() is None:
        print(
            f"warning: {ENV_API_KEY} unset — HTTP adapter accepts unauthenticated "
            "requests (dev only)",
            file=sys.stderr,
        )

    app = create_app()
    # threaded=True keeps a stuck solve from blocking health forever in pilots.
    app.run(host=args.host, port=args.port, debug=args.debug, threaded=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
