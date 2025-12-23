import socket
import logging
import sys
import os

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


def send(message: led_pb2.CustomLEDMessage):
    logging.debug(f"Sending {message.WhichOneof('choice')}")
    request_bytes = request.SerializeToString()
    if len(request_bytes) > UDP_SIZE:
        logging.warning(
            f"Sending a request_bytes that exceeds a single UDP packet. {len(request_bytes)=}"
        )
    sock.sendto(request_bytes, (IP, PORT))


if __name__ == "__main__":
    logging.info("test")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    request = led_pb2.CustomLEDMessage()
    pixels = request.set_leds.pixels
    color = pixels.add()
    color.red = 255
    color.green = 0
    color.blue = 0

    send(request)
