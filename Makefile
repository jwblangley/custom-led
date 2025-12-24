.PHONY: python-proto clean

proto_python: proto/*.proto
	@mkdir -p ./proto_python
	protoc -I=proto --python_out=./proto_python ./proto/*.proto
	@touch ./proto_python/__init__.py

clean:
	rm -rf ./proto_python/*_pb2.py
