import logging
import sys
import os

from ledclient import LEDClient, LEDColor

IP = "127.0.0.1"
PORT = 8000

logging.basicConfig(
    level=os.environ.get("LOG_LEVEL", "info").upper(),
    stream=sys.stdout,
    format="%(asctime)s.%(msecs)03d %(filename)s:%(lineno)d %(levelname)s %(message)s",
    datefmt="%Y-%d-%j %H:%M:%S",
)


if __name__ == "__main__":
    led_client = LEDClient(IP, PORT)

    leds = [LEDColor(255, 0, 128)]
    led_client.set_leds(leds)
