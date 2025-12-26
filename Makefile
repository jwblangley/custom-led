.PHONY: python-proto clean compile upload monitor

BOARD = esp32:esp32:esp32
BAUD = 115200
USB_PORT = /dev/ttyUSB0
ARDUINO_DIR = ./arduino

proto_python: proto/*.proto
	@mkdir -p ./proto_python
	protoc -I=proto --python_out=./proto_python ./proto/*.proto
	@touch ./proto_python/__init__.py

compile: arduino/*.ino
	arduino-cli compile --fqbn $(BOARD) $(ARDUINO_DIR)

compile-debug: arduino/*.ino
	arduino-cli compile --fqbn $(BOARD) --build-property build.extra_flags="-DCORE_DEBUG_LEVEL=5" $(ARDUINO_DIR)

upload:
	arduino-cli upload -p $(USB_PORT) --fqbn $(BOARD) $(ARDUINO_DIR)

monitor:
	picocom $(USB_PORT) -b $(BAUD) --imap lfcrlf

