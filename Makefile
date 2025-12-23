.PHONY: python-proto clean

python-proto:
	@mkdir -p ./protopy
	protoc -I=proto --python_out=./protopy ./proto/*.proto
	@touch ./protopy/__init__.py

clean:
	rm -rf ./protopy/*_pb2.py
