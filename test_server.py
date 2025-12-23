import os
import socket
import sys
import logging

from pprint import pformat

from protopy import led_pb2

IP = "127.0.0.1"
PORT = 5005

UDP_SIZE = 1472

logging.basicConfig(
    level=os.environ.get("LOG_LEVEL", "info").upper(),
    stream=sys.stdout,
    format="%(asctime)s.%(msecs)03d %(filename)s:%(lineno)d %(levelname)s %(message)s",
    datefmt="%Y-%d-%j %H:%M:%S",
)


class LEDManager:
    def __init__(self):
        pass

    def set(self, set_leds: led_pb2.SetLEDs):
        logging.info("Setting LEDs")
        leds = [(p.red, p.green, p.blue) for p in set_leds.pixels]
        logging.debug(pformat(leds))


if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((IP, PORT))
    logging.info(f"Listening on {IP}:{PORT}")

    led_manager = LEDManager()

    try:
        while True:
            data, addr = sock.recvfrom(UDP_SIZE)

            message = led_pb2.CustomLEDMessage()
            message.ParseFromString(data)

            match message.WhichOneof("choice"):
                case "set_leds":
                    led_manager.set(message.set_leds)
    except KeyboardInterrupt:
        logging.info("Shutting down")
