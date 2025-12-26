.PHONY: python-proto clean compile upload monitor nanopb proto-arduino

BOARD = esp32:esp32:esp32
BAUD = 115200
USB_PORT = /dev/ttyUSB0
NANOPB_DIR = ./nanopb
ARDUINO_DIR = ./arduino
PROTO_DIR = ./proto

proto_python: proto/*.proto
	@mkdir -p ./proto_python
	protoc -I=proto --python_out=./proto_python $(PROTO_DIR)/*.proto
	@touch ./proto_python/__init__.py

nanopb:
	test -d $(NANOPB_DIR) || git clone https://github.com/nanopb/nanopb.git $(NANOPB_DIR)

proto-arduino: nanopb
	mkdir --parents $(ARDUINO_DIR)/proto
	protoc -I=proto --plugin=protoc-gen-nanopb=$(NANOPB_DIR)/generator/protoc-gen-nanopb --nanopb_out=$(ARDUINO_DIR)/proto $(PROTO_DIR)/*.proto
	cp $(NANOPB_DIR)/pb_common.c $(ARDUINO_DIR)/proto/pb_common.c
	cp $(NANOPB_DIR)/pb_common.h $(ARDUINO_DIR)/proto/pb_common.h
	cp $(NANOPB_DIR)/pb_decode.c $(ARDUINO_DIR)/proto/pb_decode.c
	cp $(NANOPB_DIR)/pb_decode.h $(ARDUINO_DIR)/proto/pb_decode.h
	cp $(NANOPB_DIR)/pb_encode.c $(ARDUINO_DIR)/proto/pb_encode.c
	cp $(NANOPB_DIR)/pb_encode.h $(ARDUINO_DIR)/proto/pb_encode.h
	cp $(NANOPB_DIR)/pb.h $(ARDUINO_DIR)/proto/pb.h

compile: arduino/*.ino proto-arduino
	arduino-cli compile --fqbn $(BOARD) $(ARDUINO_DIR) --build-property build.extra_flags="-I$(ARDUINO_DIR)/proto"

upload:
	arduino-cli upload -p $(USB_PORT) --fqbn $(BOARD) $(ARDUINO_DIR)

monitor:
	picocom $(USB_PORT) -b $(BAUD) --imap lfcrlf

