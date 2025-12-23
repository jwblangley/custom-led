import socket

IP = "127.0.0.1"
PORT = 5005
MESSAGE = b"Hello, UDP Server!"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Send data
sock.sendto(MESSAGE, (IP, PORT))

# Receive response
data, server = sock.recvfrom(1024)
print(f"Server replied: {data.decode()}")
