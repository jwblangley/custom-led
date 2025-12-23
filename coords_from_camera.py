import argparse
import cv2
import sys

from queue import SimpleQueue

NAMED_WINDOW = "LED Selector: Live Preview"

TEXT_SIZE = 0.5
TEXT_OFFSET = 10
TEXT_THICKNESS = 1

SELECTED_RADIUS = 5
SELECTED_THICKNESS = 2
SELECTED_COLOR = (0, 0, 255)  # BGR

selected_leds = []
event_queue = SimpleQueue()


def record_click(event, x, y, flags, param):
    global event_queue
    if event == cv2.EVENT_LBUTTONDOWN:
        event_queue.put((x, y))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LED location selector")
    parser.add_argument("num_leds", type=int, help="Number of LEDs to locate")
    parser.add_argument(
        "-vc",
        "--video-capture",
        type=int,
        default=0,
        help="Index of video capture device",
    )
    args = parser.parse_args()

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        sys.exit(2)

    cv2.namedWindow(NAMED_WINDOW)
    cv2.setMouseCallback(NAMED_WINDOW, record_click)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        while not event_queue.empty():
            selected_leds.append(event_queue.get())

        for i, (x, y) in enumerate(selected_leds):
            cv2.circle(
                frame, (x, y), SELECTED_RADIUS, SELECTED_COLOR, SELECTED_THICKNESS
            )
            cv2.putText(
                frame,
                f"{i + 1}: ({x}, {y})",
                (x + TEXT_OFFSET, y - TEXT_OFFSET),
                cv2.FONT_HERSHEY_SIMPLEX,
                TEXT_SIZE,
                SELECTED_COLOR,
                TEXT_THICKNESS,
            )

        cv2.imshow(NAMED_WINDOW, frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
        if len(selected_leds) == args.num_leds:
            cv2.imshow(NAMED_WINDOW, frame)
            cv2.waitKey(0)
            break

    if len(selected_leds) != args.num_leds:
        print("Incorrect number of LEDs selected. Aborting")
        sys.exit(1)

    cap.release()
    cv2.destroyAllWindows()

    print(selected_leds)
