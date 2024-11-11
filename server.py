import socket
import cv2
import pickle
import struct

# Socket setup
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 9999))
server_socket.listen(5)
print("Server listening on port 9999")

# Accept a client connection
client_socket, addr = server_socket.accept()
print('Connected to:', addr)

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # Serialize frame using pickle
    data = pickle.dumps(frame)
    
    # Send frame size and frame data
    client_socket.sendall(struct.pack("L", len(data)) + data)

cap.release()
client_socket.close()
server_socket.close()
