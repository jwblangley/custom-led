import logging
import sys
import os
import argparse
import fileinput
import time

from ledclient import LEDClient, LEDColor

logging.basicConfig(
    level=os.environ.get("LOG_LEVEL", "info").upper(),
    stream=sys.stdout,
    format="%(asctime)s.%(msecs)03d %(filename)s:%(lineno)d %(levelname)s %(message)s",
    datefmt="%Y-%d-%j %H:%M:%S",
)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LED location selector")
    parser.add_argument("ip", type=str, help="IP address of server")
    parser.add_argument("port", type=int, help="Server port")
    parser.add_argument("--rotate", action="store_true")
    parser.add_argument(
        "file",
        metavar="FILE",
        nargs="?",
        help="file to read, otherwise read from stdin",
    )
    args = parser.parse_args()

    led_client = LEDClient(args.ip, args.port)

    to_set = []

    for line in fileinput.input(
        files=[] if args.file is None else args.file, encoding="utf-8"
    ):
        match line.strip().split(","):
            case [red, green, blue]:
                to_set.append(LEDColor(int(red), int(green), int(blue)))
            case _:
                logging.error(f"Unexpected line format. {line=}")

    led_client.set_leds(to_set)

    if args.rotate and len(to_set) > 1:
        while True:
            time.sleep(0.03)
            to_set = to_set[1:] + [to_set[0]]
            led_client.set_leds(to_set)
