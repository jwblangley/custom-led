import logging
import sys
import os
import argparse
import time
import cv2
import json
import math

from ledclient import LEDClient, LEDColor

logging.basicConfig(
    level=os.environ.get("LOG_LEVEL", "info").upper(),
    stream=sys.stdout,
    format="%(asctime)s.%(msecs)03d %(filename)s:%(lineno)d %(levelname)s %(message)s",
    datefmt="%Y-%d-%j %H:%M:%S",
)


def bbox(coords):
    x_min = math.inf
    x_max = -math.inf
    y_min = math.inf
    y_max = -math.inf

    for x, y in coords:
        x_min = min(x_min, x)
        x_max = max(x_max, x)
        y_min = min(y_min, y)
        y_max = max(y_max, y)

    return ((x_min, y_min), (x_max, y_max))


def map_coords(in_bbox, out_maxes, in_xy, scale):
    x_ratio = in_bbox[1][0] * scale / out_maxes[0]
    y_ratio = in_bbox[1][1] * scale / out_maxes[1]

    logging.debug(f"{x_ratio=}")
    logging.debug(f"{y_ratio=}")

    if x_ratio > 1 or y_ratio > 1:
        raise ValueError("Scale is too large for video")

    x_pad = (out_maxes[0] - (in_bbox[1][0] - in_bbox[0][0]) * scale) / 2
    y_pad = (out_maxes[1] - (in_bbox[1][1] - in_bbox[0][1]) * scale) / 2

    ret_x = x_pad + scale * (in_xy[0] - in_bbox[0][0])
    ret_y = y_pad + scale * (in_xy[1] - in_bbox[0][1])

    assert ret_x <= out_maxes[0]
    assert ret_y <= out_maxes[1]

    return int(ret_x), int(ret_y)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LED location selector")
    parser.add_argument("ip", type=str, help="IP address of server")
    parser.add_argument("port", type=int, help="Server port")
    parser.add_argument("video", type=str, help="Path to video file")
    parser.add_argument(
        "--scale", type=float, help="Scale bounding box", default=1.0, required=False
    )
    args = parser.parse_args()

    led_client = LEDClient(args.ip, args.port)

    led_config = json.load(open("led_config.json"))
    led_bbox = bbox(led_config)
    logging.info(f"{led_bbox=}")

    cap = cv2.VideoCapture(args.video)
    if not cap.isOpened():
        logging.error(f"Failed to open {args.video_file}")
        sys.exit(1)

    fps = cap.get(cv2.CAP_PROP_FPS)
    logging.info(f"{fps=}")

    while True:
        start_t = time.perf_counter()
        ret, frame = cap.read()
        if not ret:
            break

        frame_size = frame.shape[:2]
        logging.debug(f"{frame_size=}")
        leds = [
            frame[*map_coords(led_bbox, frame_size, (x, y), args.scale)].tolist()
            for x, y in led_config
        ]
        leds = [LEDColor(r, g, b) for b, g, r in leds]

        led_client.set_leds(leds)
        time.sleep(max((1 / fps) - (time.perf_counter() - start_t), 0))
