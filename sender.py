import cv2
import socket
import struct

video_path = 'example.mp4'
cap = cv2.VideoCapture(video_path)

# Create a socket for sending data
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = '192.168.1.3'  # Replace with receiver's IP address
port = 12345  # Port number

# Connect to the receiver
client_socket.connect((host_ip, port))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Compress the frame using JPEG
    ret, buffer = cv2.imencode('.jpg', frame)

    # Convert to bytes and get the size
    data = buffer.tobytes()
    size = len(data)

    # Send the size of the frame first
    client_socket.sendall(struct.pack(">L", size))

    # Then send the actual frame
    client_socket.sendall(data)

cap.release()
client_socket.close()

