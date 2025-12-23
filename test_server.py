import socket

# Define the IP address and port
IP = "127.0.0.1"  # Localhost
PORT = 5005

# 1. Create a socket (AF_INET = IPv4, SOCK_DGRAM = UDP)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 2. Bind the socket to the address and port
sock.bind((IP, PORT))

print(f"UDP server listening on {IP}:{PORT}")

while True:
    # 3. Receive data (buffer size is 1024 bytes)
    data, addr = sock.recvfrom(1024)

    print(f"Received message: {data.decode()} from {addr}")

    # 4. Optional: Send a response back to the client
    response = b"Message received!"
    sock.sendto(response, addr)
