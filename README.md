# Custom LED

A project to control WS2811 holiday lights with an ESP32 using protobuf over UDP

## Features

* Using a camera, determine the 2D projection of your lights
* Using the mapped projection, play videos on the array of lights

## Running

### Client

The python scripts require a virtual environment and the protobuf schema.

```bash
python3.13 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
make proto_python
```

Each of the scripts uses `argparse` so you can query how to use them with `--help`.

## Microcontroller

This project is set up to use an ESP32 development board configured with GPIO16 for the data pin for the LEDs.

Never connect your computer to the ESP32 board over USB when external power is still being supplied.
If you are using capacitors, ensure they are also discharged.

1. Follow <https://docs.arduino.cc/arduino-cli/getting-started> to get started - the board type is `esp32:esp32`
1. Install FastLED plugin
    ```bash
    arduino-cli lib update-index
    arduino-cli install "FastLED"
    ```
1. Run `make compile` to compile the arduino code
1. Run `make upload` to upload the compiled binary to the esp32 board. You may need to configure `USB_PORT` in the `Makefile` - this can be found using `arduino-cli board list`
1. To monitor the Serial output over USB, run `make monitor`
