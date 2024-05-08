import argparse
import os
import subprocess
from functools import partial
from typing import Any, List

from pythonosc import osc_server
from pythonosc.dispatcher import Dispatcher


def run_shell_command(command: str, address: str, *args: Any):
    arg_string = ", ".join([str(a) for a in args])
    print(f"> received {address} ({arg_string})")

    # insert osc variables (currently only for unix-shell)
    shell_osc_env_args = {f"OSC_{i}": str(v) for i, v in enumerate(args)}

    env = os.environ.copy()
    env.update(shell_osc_env_args)

    subprocess.Popen(command, env=env, shell=True)


def parse_args(unknown_args: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="shell-osc")

    parser.add_argument("-i", "--ip", default="0.0.0.0",
                        help="The ip to listen on for shell OSC commands")
    parser.add_argument("-p", "--port", type=int, default=16000,
                        help="Receiver port for shell OSC commands.")

    parser.add_argument("-m", "--map",
                        nargs=2, metavar=("address", "command"),
                        action="append", required=True,
                        help="OSC address, shell command")
    return parser.parse_args(unknown_args)


def run_server(unknown_args: List[str]):
    args = parse_args(unknown_args)

    osc_ip = str(args.ip)
    osc_port = int(args.port)

    # setup osc mapping
    dispatcher = Dispatcher()

    for address, command in args.map:
        print(f"Mapping '{address}' to '{command}'")
        dispatcher.map(address, partial(run_shell_command, command))

    server = osc_server.ThreadingOSCUDPServer((args.ip, args.port), dispatcher)
    print(f"Shell-OSC server running on {osc_ip}:{osc_port}...")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        exit(0)
