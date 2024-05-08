import argparse
from typing import List, Tuple

from shell_osc.client import run_client
from shell_osc.server import run_server

SERVER_MODE = "serve"
CLIENT_MODE = "send"


def parse_args() -> Tuple[argparse.Namespace, List[str]]:
    parser = argparse.ArgumentParser(prog="shell-osc")
    parser.add_argument("mode", choices=[SERVER_MODE, CLIENT_MODE],
                        help="Mode to run (serve or send)")
    return parser.parse_known_args()


def main():
    args, unknown_args = parse_args()

    mode: str = args.mode
    if mode == SERVER_MODE:
        run_server(unknown_args)
    else:
        run_client(unknown_args)


if __name__ == "__main__":
    main()
