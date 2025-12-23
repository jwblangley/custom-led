import socket
import logging

from protopy import led_pb2

IP = "127.0.0.1"
PORT = 5005
UDP_SIZE = 1472


class LEDClient:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send(self, message: led_pb2.CustomLEDMessage):
        logging.debug(f"Sending {message.WhichOneof('choice')}")
        request_bytes = message.SerializeToString()
        if len(request_bytes) > UDP_SIZE:
            logging.warning(
                f"Sending a request_bytes that exceeds a single UDP packet. {len(request_bytes)=}"
            )
        self.sock.sendto(request_bytes, (IP, PORT))
