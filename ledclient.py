import math
import socket
import logging

from dataclasses import dataclass

from proto_python import led_pb2

UDP_SIZE = 1472

CONFIG_FILE = "led_config.json"


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

    @staticmethod
    def normalise_bbox(locations: list[tuple[int, int]]):
        padding = 0.1

        min_x = math.inf
        max_x = -math.inf
        min_y = math.inf
        max_y = -math.inf

        for x, y in locations:
            min_x = min(min_x, x)
            max_x = max(max_x, x)
            min_y = min(min_y, y)
            max_y = max(max_y, y)

        def _norm(val, min_v, max_v):
            range_v = max_v - min_v
            result = padding + (1.0 - 2 * padding) * (val - min_v) / range_v
            assert padding <= result <= 1.0 - padding
            return result

        return [(_norm(x, min_x, max_x), _norm(y, min_y, max_y)) for x, y in locations]
