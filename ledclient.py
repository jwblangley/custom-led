import socket
import logging

from dataclasses import dataclass

from proto_python import led_pb2

UDP_SIZE = 1472

CONFIG_FILE = "led_config.json"
NUM_LEDS = 50


@dataclass
class LEDColor:
    red: int
    green: int
    blue: int


class LEDClient:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def set_leds(self, leds: list[LEDColor]):
        if len(leds) > NUM_LEDS:
            raise ValueError(f"A maximum of {NUM_LEDS} is supported")
        request = led_pb2.CustomLEDMessage()
        pixels = request.set_leds.pixels
        for led in leds:
            pixels.add(red=led.red, green=led.green, blue=led.blue)

        self._send(request)

    def clear(self):
        request = led_pb2.CustomLEDMessage()
        request.clear.SetInParent()
        self._send(request)

    def _send(self, message: led_pb2.CustomLEDMessage):
        logging.debug(f"Sending {message.WhichOneof('choice')}")
        request_bytes = message.SerializeToString()
        logging.debug(f"{len(request_bytes)=}")
        if len(request_bytes) > UDP_SIZE:
            logging.warning(
                f"Sending a request_bytes that exceeds a single UDP packet. {len(request_bytes)=}"
            )
        self.sock.sendto(request_bytes, (self.ip, self.port))
