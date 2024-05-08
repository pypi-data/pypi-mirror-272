import argparse
import logging
from typing import List, Any, Callable, Dict, Optional

from pythonosc import udp_client

ConverterMethod = Callable[[str], Any]

DATA_TYPE_CONVERTERS: Dict[str, ConverterMethod] = {
    "f": float,
    "i": int,
    "b": bool,
    "s": str
}


def parse_args(unknown_args: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="shell-osc")

    parser.add_argument("address", type=str, help="OSC address to send data to.")
    parser.add_argument("data", nargs="*", help="Data to send with the message.")
    parser.add_argument("-t", "--types", type=str, default=None,
                        help="Set the datatype of the arguments to be sent (instead of inferred).")

    parser.add_argument("-i", "--ip", default="255.255.255.255",
                        help="The ip to listen on for shell OSC commands")
    parser.add_argument("-p", "--port", type=int, default=16000,
                        help="Receiver port for shell OSC commands.")

    return parser.parse_args(unknown_args)


def convert_data(value: str, data_type_converter: Optional[ConverterMethod]) -> Any:
    if data_type_converter is not None:
        return data_type_converter(value)

    # check if is int
    try:
        return int(value)
    except ValueError:
        pass

    try:
        return float(value)
    except ValueError:
        pass

    # check bool
    if value.lower() == "true":
        return True
    elif value.lower() == "false":
        return False

    # it's a string
    return value


def run_client(unknown_args: List[str]):
    args = parse_args(unknown_args)

    address = str(args.address)
    osc_ip = str(args.ip)
    osc_port = int(args.port)
    string_args: List[str] = args.data

    converters = [None] * len(string_args)
    if args.types is not None:
        types = str(args.types).strip()

        if len(types) == len(string_args):
            converters = [DATA_TYPE_CONVERTERS[t] for t in types]
        else:
            logging.error(f"Types supplied '{types}' are not enough for the arguments count {len(string_args)}.")
            return

    data = [convert_data(d, c) for d, c in zip(string_args, converters)]

    client = udp_client.SimpleUDPClient(osc_ip, osc_port, allow_broadcast=True)
    client.send_message(address, data)

    str_data = ", ".join([str(d) for d in data])
    print(f"> OSC Message: {address} ({str_data})")

    exit(0)
