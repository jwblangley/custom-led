import os
import socket
import sys
import logging
import argparse

from pprint import pformat

from protopy import led_pb2

IP = "127.0.0.1"
PORT = 8000

UDP_SIZE = 1472

logging.basicConfig(
    level=os.environ.get("LOG_LEVEL", "info").upper(),
    stream=sys.stdout,
    format="%(asctime)s.%(msecs)03d %(filename)s:%(lineno)d %(levelname)s %(message)s",
    datefmt="%Y-%d-%j %H:%M:%S",
)


class LEDManager:
    def __init__(self, num_leds):
        self.num_leds = num_leds
        self.clear()

    def clear(self):
        logging.info("Clearing LEDs")
        self.leds = [(0, 0, 0)] * self.num_leds

    def set(self, set_leds: led_pb2.SetLEDs):
        logging.info("Setting LEDs")

        if len(set_leds.pixels) > self.num_leds:
            logging.error(
                f"Request to set more LEDs than configured. request={len(set_leds.pixels)}, configured={self.num_leds}"
            )
            return

        for i, p in enumerate(set_leds.pixels):
            self.leds[i] = (p.red, p.green, p.blue)
        logging.debug(pformat(self.leds))


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Test LED server")
    parser.add_argument(
        "-n", "--num-leds", help="Number of LEDs configured", required=True, type=int
    )
    args = parser.parse_args()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((IP, PORT))
    logging.info(f"Listening on {IP}:{PORT}")

    led_manager = LEDManager(args.num_leds)

    try:
        while True:
            data, addr = sock.recvfrom(UDP_SIZE)

            message = led_pb2.CustomLEDMessage()
            message.ParseFromString(data)

            match message.WhichOneof("choice"):
                case "set_leds":
                    led_manager.set(message.set_leds)
                case "clear":
                    led_manager.clear()
    except KeyboardInterrupt:
        logging.info("Shutting down")
