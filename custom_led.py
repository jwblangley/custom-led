import logging
import sys
import os

from ledclient import LEDClient
from protopy import led_pb2


logging.basicConfig(
    level=os.environ.get("LOG_LEVEL", "info").upper(),
    stream=sys.stdout,
    format="%(asctime)s.%(msecs)03d %(filename)s:%(lineno)d %(levelname)s %(message)s",
    datefmt="%Y-%d-%j %H:%M:%S",
)


if __name__ == "__main__":
    led_client = LEDClient()

    request = led_pb2.CustomLEDMessage()
    pixels = request.set_leds.pixels
    color = pixels.add()
    color.red = 255
    color.green = 0
    color.blue = 0

    led_client.send(request)
